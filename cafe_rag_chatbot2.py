# cafe_kiosk_chatbot.py

import os
import readline
from typing import Optional, List, Dict, Tuple
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from cafe_menu import CAFE_DATA

DB_PATH = "vector_db"
DB_FAISS_PATH = os.path.join(DB_PATH, "faiss_index")

class OrderItem:
    """주문 항목"""
    def __init__(self, menu_id: str, menu_name: str, size: str, price: int, quantity: int = 1):
        self.menu_id = menu_id
        self.menu_name = menu_name
        self.size = size
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        if self.size:
            return f"{self.menu_name} ({self.size}) x{self.quantity} - {self.price * self.quantity:,}원"
        else:
            return f"{self.menu_name} x{self.quantity} - {self.price * self.quantity:,}원"

class OrderState:
    """주문 상태 관리"""
    def __init__(self):
        # 주문 단계
        self.stage = 'browsing'  # browsing, size_selection, quantity_selection, additional_menu, serving_type, packaging_tumbler, packaging_straw, packaging_carrier, payment, completed
        
        # 장바구니
        self.cart = []  # List[OrderItem]
        
        # 임시 선택 메뉴 (사이즈/수량 선택 대기)
        self.pending_menu = None  # {'menu_id': str, 'menu_name': str, 'prices': dict, 'subcategory': str}
        
        # 메뉴 탐색 상태
        self.browsing_results = []
        self.browsing_query = ""
        
        # 서빙 정보
        self.serving_type = None  # 'dine_in' or 'takeout'
        self.use_tumbler = None
        self.need_straw = None
        self.need_carrier = None
        
        # 결제 정보
        self.payment_method = None  # 'card', 'cash', 'support', 'coupon'
        
        # 대화 히스토리
        self.conversation_history = []
    
    def add_to_history(self, role: str, content: str):
        """대화 기록 추가"""
        self.conversation_history.append({"role": role, "content": content})
        # 최근 10턴만 유지
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def get_cart_summary(self) -> str:
        """장바구니 요약"""
        if not self.cart:
            return "장바구니가 비어있습니다."
        
        lines = ["[현재 장바구니]"]
        subtotal = 0
        for i, item in enumerate(self.cart, 1):
            lines.append(f"{i}. {item}")
            subtotal += item.price * item.quantity
        
        # 텀블러 할인 계산
        discount = 0
        if self.use_tumbler:
            discount = 300
            lines.append(f"\n🌱 텀블러 할인: -300원")
        
        total = subtotal - discount
        lines.append(f"💰 합계: {total:,}원")
        return "\n".join(lines)
    
    def get_total_price(self) -> int:
        """총 금액 (할인 적용)"""
        subtotal = sum(item.price * item.quantity for item in self.cart)
        discount = 300 if self.use_tumbler else 0
        return subtotal - discount
    
    def reset(self):
        """주문 초기화"""
        self.__init__()

class CafeKioskChatbot:
    """카페 키오스크 챗봇 - 대화 히스토리 & 주문 프로세스"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        self.embeddings = OpenAIEmbeddings()
        self.menus = CAFE_DATA.get('menus', [])
        self.store_info = CAFE_DATA.get('store_info', {})
        
        if not os.path.exists(DB_FAISS_PATH):
            raise FileNotFoundError(f"벡터 DB를 찾을 수 없습니다: {DB_FAISS_PATH}")
        
        print(f"📂 벡터 DB 로드 중...")
        self.vectorstore = FAISS.load_local(
            folder_path=DB_FAISS_PATH,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        self.doc_map = {
            doc.metadata['menu_id']: doc 
            for doc in self.vectorstore.docstore._dict.values()
        }
        
        self.order_state = OrderState()
        
        print(f"✅ 카페 키오스크 챗봇 준비 완료 ({len(self.menus)}개 메뉴)\n")

    # ==================== 메뉴 검색 ====================
    
    def _search_menu(self, query: str) -> List[Tuple[Document, float]]:
        """메뉴 검색 (동의어 우선)"""
        # 동의어 검색
        synonym_results = self._synonym_search(query)
        if synonym_results and len(synonym_results) <= 3:
            return synonym_results
        
        # 벡터 검색
        results = self.vectorstore.similarity_search_with_score(query, k=10)
        weighted = [
            (doc, (1 / (1 + score)) * doc.metadata.get('search_boost_score', 1.0))
            for doc, score in results
        ]
        weighted.sort(key=lambda x: x[1], reverse=True)
        
        return weighted

    def _synonym_search(self, query: str) -> List[Tuple[Document, float]]:
        """동의어 검색"""
        query_lower = query.lower().strip()
        matches = []
        
        for menu in self.menus:
            for synonym in menu['synonyms']:
                synonym_lower = synonym.lower()
                
                if query_lower == synonym_lower or synonym_lower in query_lower:
                    doc = self.doc_map.get(menu['menu_id'])
                    if doc:
                        score = 1000.0 if query_lower == synonym_lower else 500.0
                        matches.append((doc, score))
        
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _get_menu_info(self, menu_id: str) -> Optional[dict]:
        """메뉴 상세 정보"""
        for menu in self.menus:
            if menu['menu_id'] == menu_id:
                return menu
        return None

    # ==================== 대화 처리 ====================
    
    def ask(self, user_input: str) -> str:
        """메인 대화 처리"""
        
        # 대화 기록 추가
        self.order_state.add_to_history("user", user_input)
        
        # 명령어 처리
        if user_input.lower() in ['취소', '리셋', '처음부터']:
            self.order_state.reset()
            return "주문이 취소되었습니다. 다시 시작해주세요! 😊"
        
        if user_input.lower() in ['장바구니', '카트']:
            return self.order_state.get_cart_summary()
        
        # 단계별 처리
        response = self._process_by_stage(user_input)
        
        # 대화 기록 추가
        self.order_state.add_to_history("assistant", response)
        
        return response

    def _process_by_stage(self, user_input: str) -> str:
        """단계별 처리"""
        
        stage = self.order_state.stage
        
        # 1. 메뉴 탐색 중
        if stage == 'browsing':
            return self._handle_browsing(user_input)
        
        # 2. 사이즈 선택 중
        elif stage == 'size_selection':
            return self._handle_size_selection(user_input)
        
        # 2-1. 수량 선택 중 (케이크/샌드위치)
        elif stage == 'quantity_selection':
            return self._handle_quantity_selection(user_input)
        
        # 3. 추가 메뉴 확인
        elif stage == 'additional_menu':
            return self._handle_additional_menu(user_input)
        
        # 4. 포장/매장 선택
        elif stage == 'serving_type':
            return self._handle_serving_type(user_input)
        
        # 5-1. 포장 세부사항 - 텀블러
        elif stage == 'packaging_tumbler':
            return self._handle_packaging_tumbler(user_input)
        
        # 5-2. 포장 세부사항 - 빨대
        elif stage == 'packaging_straw':
            return self._handle_packaging_straw(user_input)
        
        # 5-3. 포장 세부사항 - 캐리어
        elif stage == 'packaging_carrier':
            return self._handle_packaging_carrier(user_input)
        
        # 6. 결제 방식
        elif stage == 'payment':
            return self._handle_payment(user_input)
        
        return "알 수 없는 상태입니다."

    # ==================== 매장 정보 질문 처리 ====================
    
    def _detect_store_info_question(self, user_input: str) -> Optional[str]:
        """매장 정보 질문 감지 및 답변"""
        user_lower = user_input.lower().strip()
        
        # 1. 화장실 위치
        if any(keyword in user_lower for keyword in ['화장실', '화장', '휴게실', '변기', 'toilet', 'restroom']):
            return self.store_info['facilities']['restroom']['location']
        
        # 2. 와이파이
        if any(keyword in user_lower for keyword in ['와이파이', '와파', 'wifi', 'wi-fi', '인터넷', '비번', '비밀번호', '무선']):
            wifi = self.store_info['wifi']
            return f"💻 와이파이 정보\n- 네트워크: {wifi['ssid']}\n- 비밀번호: {wifi['password']}\n\n자유롭게 이용하세요!"
        
        # 3. 영업시간
        if any(keyword in user_lower for keyword in ['영업시간', '몇시', '언제', '시간', '영업', '오픈', 'open', '닫', 'close', '문여', '문닫']):
            hours = self.store_info['hours']
            return f"🕐 영업시간\n{hours['description']}\n{hours['holiday']}\n\n편하게 방문하세요!"
        
        # 4. 주차
        if any(keyword in user_lower for keyword in ['주차', '차', '주차장', 'parking', '파킹']):
            parking = self.store_info['facilities']['parking']
            if parking['available']:
                return f"🚗 {parking['description']}"
            return "죄송합니다. 주차 공간이 없습니다."
        
        # 5. 콘센트/충전
        if any(keyword in user_lower for keyword in ['콘센트', '충전', '전기', '플러그', 'socket', '노트북']):
            socket = self.store_info['facilities']['socket']
            if socket['available']:
                return f"🔌 {socket['description']}"
            return "죄송합니다. 콘센트 제공이 어렵습니다."
        
        # 6. 연락처
        if any(keyword in user_lower for keyword in ['전화', '연락', '번호', '전번', 'phone', '문의']):
            contact = self.store_info['contact']
            return f"📞 매장 연락처\n- 전화: {contact['phone']}\n- 인스타그램: {contact['instagram']}"
        
        # 7. 재치있는 답변 (알바생 번호)
        if any(keyword in user_lower for keyword in ['알바', '아르바이트', '직원', '언니', '오빠', '누나', '형', '이쁜', '예쁜', '잘생긴', '귀여운']):
            if any(keyword in user_lower for keyword in ['번호', '전화', '연락', '카톡', '인스타']):
                funny_responses = [
                    "😅 저희는 로봇이라 번호가 없어요... 대신 메뉴 추천은 자신 있습니다!",
                    "🤖 AI 직원이라 프라이버시는 철저히 지켜집니다! 대신 맛있는 커피 한 잔 어떠세요?",
                    "😂 제 번호는 010-1234-ROBOT인데... 연결이 안 될 거예요! 주문하시겠어요?",
                    "💚 마음은 감사하지만, 저는 커피에만 관심있는 AI랍니다! 음료 추천해드릴까요?"
                ]
                import random
                return random.choice(funny_responses)
        
        # 8. 욕설/비속어 감지
        if any(keyword in user_lower for keyword in ['ㅅㅂ', '시발', 'ㅈㄴ', 'ㄲㅈ']):
            return "😊 정중한 언어 사용 부탁드립니다. 맛있는 음료로 기분 전환하시는 건 어떠세요?"
        
        return None
    
    # ==================== 1. 메뉴 탐색 ====================
    
    def _handle_browsing(self, user_input: str) -> str:
        """메뉴 탐색 단계"""
        
        # 매장 정보 질문 우선 처리
        store_info_response = self._detect_store_info_question(user_input)
        if store_info_response:
            return store_info_response
        
        # LLM으로 의도 파악 (대화 히스토리 포함)
        intent = self._analyze_intent(user_input)
        
        # 주문 의도
        if intent['type'] == 'order':
            return self._process_order_request(user_input, intent)
        
        # 메뉴 검색 의도
        elif intent['type'] == 'search':
            results = self._search_menu(user_input)
            
            if not results:
                return "죄송합니다. 해당하는 메뉴를 찾을 수 없습니다. 다시 말씀해주시겠어요?"
            
            # 메뉴 목록 저장
            self.order_state.browsing_results = results
            self.order_state.browsing_query = user_input
            
            # 결과가 1개면 바로 사이즈 선택
            if len(results) == 1:
                menu_info = self._get_menu_info(results[0][0].metadata['menu_id'])
                return self._start_size_selection(menu_info)
            
            # 여러 개면 목록 표시
            return self._format_menu_list(results[:5])
        
        # 일반 질문
        else:
            return self._answer_with_rag(user_input)

    def _analyze_intent(self, user_input: str) -> dict:
        """의도 분석 (LLM 활용)"""
        
        # 대화 히스토리 포함
        history_text = self._format_conversation_history()
        
        prompt = f"""당신은 카페 키오스크 AI입니다. 사용자 입력의 의도를 파악하세요.

[대화 기록]
{history_text}

[현재 사용자 입력]
{user_input}

다음 중 하나로 분류하세요:
1. "order" - 주문하려는 의도 (예: "아메리카노 1잔", "자허블이랑 아아 포장")
2. "search" - 메뉴를 찾는 의도 (예: "케이크 종류", "얼마야")
3. "question" - 일반 질문 (예: "추천해줘", "이거 칼로리")

JSON 형식으로만 답하세요:
{{"type": "order|search|question", "menus": ["메뉴1", "메뉴2"], "details": "추가정보"}}
"""
        
        try:
            response = self.llm.invoke(prompt)
            import json
            intent = json.loads(response.content)
            return intent
        except:
            # 파싱 실패 시 기본값
            return {"type": "search", "menus": [], "details": ""}

    def _format_conversation_history(self) -> str:
        """대화 히스토리 포맷팅"""
        if not self.order_state.conversation_history:
            return "(없음)"
        
        lines = []
        for msg in self.order_state.conversation_history[-6:]:  # 최근 3턴
            role = "고객" if msg['role'] == 'user' else "챗봇"
            lines.append(f"{role}: {msg['content']}")
        
        return "\n".join(lines)

    def _process_order_request(self, user_input: str, intent: dict) -> str:
        """주문 요청 처리"""
        
        # 메뉴 추출
        mentioned_menus = intent.get('menus', [])
        
        if not mentioned_menus:
            # LLM으로 메뉴 추출 재시도
            mentioned_menus = self._extract_menus_from_text(user_input)
        
        if not mentioned_menus:
            return "어떤 메뉴를 주문하시겠어요? 메뉴 이름을 말씀해주세요."
        
        # 첫 번째 메뉴 검색
        results = self._search_menu(mentioned_menus[0])
        
        if not results:
            return f"'{mentioned_menus[0]}'를 찾을 수 없습니다. 다른 메뉴를 말씀해주세요."
        
        # 가장 일치하는 메뉴
        menu_info = self._get_menu_info(results[0][0].metadata['menu_id'])
        
        # 나머지 메뉴는 임시 저장 (TODO)
        # 일단 첫 메뉴만 처리
        
        return self._start_size_selection(menu_info)

    def _extract_menus_from_text(self, text: str) -> List[str]:
        """텍스트에서 메뉴 이름 추출"""
        found = []
        text_lower = text.lower()
        
        for menu in self.menus:
            for synonym in menu['synonyms']:
                if synonym.lower() in text_lower:
                    found.append(menu['name'])
                    break
        
        return found

    def _start_size_selection(self, menu_info: dict) -> str:
        """사이즈/수량 선택 시작"""
        
        subcategory = menu_info.get('subcategory', '')
        
        # 케이크 또는 샌드위치인 경우 → 수량 선택
        if subcategory in ['케이크', '샌드위치']:
            self.order_state.stage = 'quantity_selection'
            self.order_state.pending_menu = {
                'menu_id': menu_info['menu_id'],
                'menu_name': menu_info['name'],
                'prices': menu_info['size_prices'],
                'subcategory': subcategory
            }
            
            base_price = menu_info['base_price']
            return f"""✅ {menu_info['name']} 선택하셨습니다!

가격: {base_price:,}원

몇 개 주문하시겠어요? 
💡 숫자로 말씀해주세요 (예: 1, 2, 3...)"""
        
        # 일반 메뉴 → 사이즈 선택
        else:
            self.order_state.stage = 'size_selection'
            self.order_state.pending_menu = {
                'menu_id': menu_info['menu_id'],
                'menu_name': menu_info['name'],
                'prices': menu_info['size_prices'],
                'subcategory': subcategory
            }
            
            # 사이즈 옵션
            prices = menu_info['size_prices']
            size_options = []
            
            if 'Regular' in prices:
                size_options.append(f"레귤러(R) {prices['Regular']:,}원")
            if 'Large' in prices:
                size_options.append(f"라지(L) {prices['Large']:,}원")
            if 'Extra Large' in prices:
                size_options.append(f"엑스트라라지(XL) {prices['Extra Large']:,}원")
            
            return f"""✅ {menu_info['name']} 선택하셨습니다!

사이즈를 골라주세요:
{chr(10).join(f'{i+1}. {opt}' for i, opt in enumerate(size_options))}

💡 숫자나 사이즈 이름(R/L/XL)을 말씀해주세요."""

    def _format_menu_list(self, results: List[Tuple]) -> str:
        """메뉴 목록 포맷"""
        lines = ["어떤 메뉴를 주문하시겠어요?\n"]
        
        for i, (doc, score) in enumerate(results, 1):
            meta = doc.metadata
            price = meta.get('base_price', 'N/A')
            lines.append(f"{i}. {meta['name']} - Regular {price:,}원")
        
        lines.append("\n💡 숫자나 메뉴 이름을 말씀해주세요.")
        return "\n".join(lines)

    # ==================== 2. 사이즈 선택 ====================
    
    def _handle_size_selection(self, user_input: str) -> str:
        """사이즈 선택 처리"""
        
        pending = self.order_state.pending_menu
        prices = pending['prices']
        
        # 사이즈 파싱
        size = self._parse_size(user_input, list(prices.keys()))
        
        if not size:
            return "죄송합니다. 사이즈를 다시 말씀해주세요. (레귤러/R, 라지/L, 엑스트라라지/XL)"
        
        # 장바구니에 추가
        item = OrderItem(
            menu_id=pending['menu_id'],
            menu_name=pending['menu_name'],
            size=size,
            price=prices[size],
            quantity=1
        )
        
        self.order_state.cart.append(item)
        self.order_state.pending_menu = None
        
        # 다음 단계: 추가 메뉴 확인
        self.order_state.stage = 'additional_menu'
        
        return f"""✅ {item.menu_name} ({size}) {item.price:,}원이 담겼습니다!

{self.order_state.get_cart_summary()}

다른 메뉴도 추가하시겠어요? (예/아니요)"""
    
    # ==================== 2-1. 수량 선택 (케이크/샌드위치) ====================
    
    def _handle_quantity_selection(self, user_input: str) -> str:
        """수량 선택 처리 (케이크/샌드위치)"""
        
        pending = self.order_state.pending_menu
        
        # 수량 파싱
        quantity = self._parse_quantity(user_input)
        
        if not quantity or quantity <= 0:
            return "죄송합니다. 수량을 다시 말씀해주세요. (예: 1, 2, 3...)"
        
        if quantity > 10:
            return "한 번에 최대 10개까지만 주문 가능합니다. 다시 말씀해주세요."
        
        # 가격은 Regular(base_price) 사용
        price = pending['prices'].get('Regular', pending['prices'][list(pending['prices'].keys())[0]])
        
        # 장바구니에 추가
        item = OrderItem(
            menu_id=pending['menu_id'],
            menu_name=pending['menu_name'],
            size=None,  # 케이크/샌드위치는 사이즈 없음
            price=price,
            quantity=quantity
        )
        
        self.order_state.cart.append(item)
        self.order_state.pending_menu = None
        
        # 다음 단계: 추가 메뉴 확인
        self.order_state.stage = 'additional_menu'
        
        return f"""✅ {item.menu_name} {quantity}개 {item.price * quantity:,}원이 담겼습니다!

{self.order_state.get_cart_summary()}

다른 메뉴도 추가하시겠어요? (예/아니요)"""

    def _parse_size(self, user_input: str, available_sizes: List[str]) -> Optional[str]:
        """사이즈 파싱"""
        user_lower = user_input.lower().strip()
        
        # 매핑
        size_map = {
            'regular': 'Regular', 'r': 'Regular', '레귤러': 'Regular', '레귤': 'Regular', '1': 'Regular',
            'large': 'Large', 'l': 'Large', '라지': 'Large', '라': 'Large', '2': 'Large',
            'extra large': 'Extra Large', 'xl': 'Extra Large', '엑스트라라지': 'Extra Large', 
            '엑라': 'Extra Large', 'extra': 'Extra Large', '3': 'Extra Large'
        }
        
        for key, value in size_map.items():
            if key in user_lower and value in available_sizes:
                return value
        
        return None
    
    def _parse_quantity(self, user_input: str) -> Optional[int]:
        """수량 파싱"""
        import re
        
        user_input = user_input.strip()
        
        # 숫자만 추출
        numbers = re.findall(r'\d+', user_input)
        
        if numbers:
            return int(numbers[0])
        
        # 한글 숫자 매핑
        korean_numbers = {
            '한': 1, '하나': 1, '일': 1,
            '두': 2, '둘': 2, '이': 2,
            '세': 3, '셋': 3, '삼': 3,
            '네': 4, '넷': 4, '사': 4,
            '다섯': 5, '오': 5,
            '여섯': 6, '육': 6,
            '일곱': 7, '칠': 7,
            '여덟': 8, '팔': 8,
            '아홉': 9, '구': 9,
            '열': 10, '십': 10
        }
        
        for korean, num in korean_numbers.items():
            if korean in user_input:
                return num
        
        return None

    # ==================== 3. 추가 메뉴 ====================
    
    def _handle_additional_menu(self, user_input: str) -> str:
        """추가 메뉴 처리"""
        
        user_lower = user_input.lower().strip()
        
        # 긍정
        if any(word in user_lower for word in ['예', '네', '응', '어', '그래', 'yes', 'y', 'ㅇ']):
            self.order_state.stage = 'browsing'
            return "추가하실 메뉴를 말씀해주세요! 😊"
        
        # 부정
        elif any(word in user_lower for word in ['아니', '노', '안', 'no', 'n', '없어', '그만','ㄴ']):
            self.order_state.stage = 'serving_type'
            return "매장에서 드시겠어요, 포장하시겠어요? 🏪📦"
        
        # 애매한 답변 → 메뉴로 해석
        else:
            self.order_state.stage = 'browsing'
            return self._handle_browsing(user_input)

    # ==================== 4. 포장/매장 ====================
    
    def _handle_serving_type(self, user_input: str) -> str:
        """포장/매장 선택"""
        
        user_lower = user_input.lower().strip()
        
        # 포장
        if any(word in user_lower for word in ['포장', '테이크아웃', 'takeout', '가져', '싸']):
            self.order_state.serving_type = 'takeout'
            self.order_state.stage = 'packaging_tumbler'
            return """포장 도와드릴게요! 📦

개인 텀블러 사용하시나요? (예/아니요)
💡 텀블러 사용 시 300원 할인!"""
        
        # 매장
        elif any(word in user_lower for word in ['매장', '여기', '안', '먹고', 'here', '홀']):
            self.order_state.serving_type = 'dine_in'
            self.order_state.stage = 'payment'
            return f"""매장에서 드시는군요! 🏪

{self.order_state.get_cart_summary()}

결제 방법을 선택해주세요:
1. 카드
2. 현금
3. 민생지원금
4. 도장 쿠폰 (10개 모으면 레귤러 음료 1잔 무료!)

💡 번호나 결제 방법을 말씀해주세요."""
        
        else:
            return "매장에서 드실지, 포장하실지 말씀해주세요! 🏪📦"

    # ==================== 5. 포장 세부사항 (단계별) ====================
    
    def _handle_packaging_tumbler(self, user_input: str) -> str:
        """포장 세부사항 1단계: 텀블러"""
        
        user_lower = user_input.lower().strip()
        
        # 긍정
        if any(word in user_lower for word in ['예','ㅇ', '네', '응', '어', '그래', 'yes', 'y', '사용', '써']):
            self.order_state.use_tumbler = True
            response_text = "✅ 텀블러 사용으로 처리하겠습니다. 🌱 (300원 할인 적용!)"
        # 부정
        elif any(word in user_lower for word in ['아니', '노', '안', 'no', 'n', '없어', '안써','ㄴ']):
            self.order_state.use_tumbler = False
            response_text = "✅ 일회용 컵으로 준비하겠습니다."
        else:
            return "텀블러를 사용하시나요? '예' 또는 '아니요'로 답해주세요. 💡 텀블러 사용 시 300원 할인!"
        
        # 다음 단계: 빨대
        self.order_state.stage = 'packaging_straw'
        return f"""{response_text}

빨대 필요하세요? (예/아니요)"""
    
    def _handle_packaging_straw(self, user_input: str) -> str:
        """포장 세부사항 2단계: 빨대"""
        
        user_lower = user_input.lower().strip()
        
        # 긍정
        if any(word in user_lower for word in ['예','ㅇ', '네', '응', '어', '그래', 'yes', 'y', '필요', '주세요']):
            self.order_state.need_straw = True
            response_text = "✅ 빨대 챙겨드리겠습니다."
        # 부정
        elif any(word in user_lower for word in ['아니', '노', '안', 'no', 'n', '없어', '괜찮', '필요없','ㄴ']):
            self.order_state.need_straw = False
            response_text = "✅ 빨대는 빼고 준비하겠습니다."
        else:
            return "빨대가 필요하신가요? '예' 또는 '아니요'로 답해주세요."
        
        # 다음 단계: 캐리어
        self.order_state.stage = 'packaging_carrier'
        return f"""{response_text}

음료 캐리어(홀더) 필요하세요? (예/아니요)"""
    
    def _handle_packaging_carrier(self, user_input: str) -> str:
        """포장 세부사항 3단계: 캐리어"""
        
        user_lower = user_input.lower().strip()
        
        # 긍정
        if any(word in user_lower for word in ['예','ㅇ', '네', '응', '어', '그래', 'yes', 'y', '필요', '주세요']):
            self.order_state.need_carrier = True
            response_text = "✅ 캐리어 준비해드리겠습니다."
        # 부정
        elif any(word in user_lower for word in ['아니', '노', '안', 'no', 'n', '없어', '괜찮', '필요없','ㄴ']):
            self.order_state.need_carrier = False
            response_text = "✅ 캐리어는 빼고 준비하겠습니다."
        else:
            return "캐리어가 필요하신가요? '예' 또는 '아니요'로 답해주세요."
        
        # 다음 단계: 결제
        self.order_state.stage = 'payment'
        
        summary = f"""{response_text}

📋 포장 옵션 정리:
- 개인 텀블러: {'사용' if self.order_state.use_tumbler else '미사용'}
- 빨대: {'필요' if self.order_state.need_straw else '불필요'}
- 음료 캐리어: {'필요' if self.order_state.need_carrier else '불필요'}

{self.order_state.get_cart_summary()}

결제 방법을 선택해주세요:
1. 카드
2. 현금
3. 민생지원금
4. 도장 쿠폰 (10개 모으면 레귤러 음료 1잔 무료!)

💡 번호나 결제 방법을 말씀해주세요."""
        
        return summary

    # ==================== 6. 결제 ====================
    
    def _handle_payment(self, user_input: str) -> str:
        """결제 처리"""
        
        user_lower = user_input.lower().strip()
        
        # 결제 방법 파싱
        if any(word in user_lower for word in ['카드', 'card', '1']):
            payment = '카드'
        elif any(word in user_lower for word in ['현금', 'cash', '2']):
            payment = '현금'
        elif any(word in user_lower for word in ['민생', 'support', '지원', '3']):
            payment = '민생지원금'
        elif any(word in user_lower for word in ['도장', '쿠폰', 'coupon', '4']):
            payment = '도장 쿠폰'
        else:
            return "결제 방법을 다시 말씀해주세요. (카드/현금/민생지원금/도장쿠폰)"
        
        self.order_state.payment_method = payment
        self.order_state.stage = 'completed'
        
        # 최종 주문 요약
        summary = f"""🎉 주문이 완료되었습니다!

{self.order_state.get_cart_summary()}

📋 주문 정보:
- 서빙 방식: {'포장 📦' if self.order_state.serving_type == 'takeout' else '매장 🏪'}
"""
        
        if self.order_state.serving_type == 'takeout':
            summary += f"""- 개인 텀블러: {'사용' if self.order_state.use_tumbler else '미사용'}
- 빨대: {'필요' if self.order_state.need_straw else '불필요'}
- 음료 캐리어: {'필요' if self.order_state.need_carrier else '불필요'}
"""
        
        summary += f"""- 결제 방법: {payment}

☕ 음료 곧 준비해드리겠습니다!
주문해주셔서 감사합니다~ 😊

💡 새로운 주문을 하시려면 '처음부터'라고 말씀해주세요."""
        
        return summary

    # ==================== RAG 답변 ====================
    
    def _answer_with_rag(self, query: str) -> str:
        """RAG로 일반 질문 답변"""
        
        # 대화 히스토리 컨텍스트
        history_text = self._format_conversation_history()
        
        # 현재 장바구니 컨텍스트
        cart_text = self.order_state.get_cart_summary() if self.order_state.cart else ""
        
        # 관련 메뉴 검색
        results = self._search_menu(query)
        
        if not results:
            return "죄송합니다. 관련 정보를 찾을 수 없습니다."
        
        # 상위 3개 메뉴 정보
        context_parts = []
        for doc, score in results[:3]:
            meta = doc.metadata
            context_parts.append(f"""
[{meta['name']}]
- 가격: Regular {meta.get('base_price')}원
- 설명: {meta.get('description')}
- 칼로리: {meta.get('calories', {}).get('regular')}kcal
""")
        
        context = "\n".join(context_parts)
        
        # LLM 프롬프트
        prompt = f"""당신은 친절한 카페 키오스크 AI입니다.

[대화 기록]
{history_text}

[현재 장바구니]
{cart_text}

[메뉴 정보]
{context}

[고객 질문]
{query}

위 정보를 바탕으로 친절하고 간결하게 답변하세요. (2-3문장)
대화 기록과 장바구니를 참고하여 맥락에 맞게 답변하세요.
"""
        
        response = self.llm.invoke(prompt)
        return response.content


if __name__ == "__main__":
    try:
        chatbot = CafeKioskChatbot()
        
        print("="*60)
        print("🤖 스마트 카페 키오스크 챗봇")
        print("="*60)
        print("✨ 기능:")
        print("   📝 단계별 주문 프로세스")
        print("   💬 대화 히스토리 기억")
        print("   🛒 장바구니 관리")
        print("   📦 포장/매장 옵션")
        print("   💳 다양한 결제 방식")
        print("="*60)
        print("\n💡 명령어: '장바구니', '처음부터', '종료'\n")
        
        while True:
            try:
                user_input = input("👤 질문: ").strip()
                
                if user_input.lower() in ['종료', 'exit', 'quit']:
                    print("\n🤖 감사합니다! 안녕히 가세요~ ☕\n")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n[현재 단계: {chatbot.order_state.stage}]")
                response = chatbot.ask(user_input)
                print(f"🤖 {response}")
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 감사합니다! 안녕히 가세요~ ☕\n")
                break
            except Exception as e:
                print(f"\n⚠️ 오류: {e}\n")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"\n❌ 초기화 오류: {e}\n")
        import traceback
        traceback.print_exc()