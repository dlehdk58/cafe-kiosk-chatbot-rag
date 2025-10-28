"""
하이브리드 카페 주문 챗봇
"""

import os
from typing import Optional, List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
        return f"{self.menu_name} x{self.quantity} - {self.price * self.quantity:,}원"


class OrderState:
    """주문 상태 관리 (간소화 버전)"""
    def __init__(self):
        self.cart = []  # 주문 내역
        self.stage = 'browsing'  # browsing, confirm, serving, payment, done
        self.pending_item = None  # 임시 선택 메뉴
        self.serving_type = None  # dine_in / takeout
        self.payment_method = None
        self.conversation_history = []
    
    def add_to_cart(self, item: OrderItem):
        """장바구니에 추가"""
        self.cart.append(item)
    
    def get_cart_summary(self) -> str:
        """장바구니 요약"""
        if not self.cart:
            return "장바구니가 비어있습니다."
        
        lines = ["📋 현재 주문 내역:"]
        total = 0
        for i, item in enumerate(self.cart, 1):
            lines.append(f"{i}. {item}")
            total += item.price * item.quantity
        
        lines.append(f"\n💰 합계: {total:,}원")
        return "\n".join(lines)
    
    def get_total(self) -> int:
        """총 금액"""
        return sum(item.price * item.quantity for item in self.cart)
    
    def reset(self):
        """초기화"""
        self.__init__()


class HybridCafeChatbot:
    """
    하이브리드 카페 챗봇
    
    핵심 메서드:
    - ask(): 사용자 입력 처리
    - _analyze_intent(): LLM으로 의도 파악
    - _generate_response(): LLM으로 자연스러운 응답 생성
    """
    
    def __init__(self):
        # LLM 초기화
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
        self.embeddings = OpenAIEmbeddings()
        
        # 데이터 로드
        self.menus = CAFE_DATA.get('menus', [])
        self.store_info = CAFE_DATA.get('store_info', {})
        
        # 벡터 DB 로드
        if not os.path.exists(DB_FAISS_PATH):
            raise FileNotFoundError(f"벡터 DB를 찾을 수 없습니다: {DB_FAISS_PATH}")
        
        print(f"📂 벡터 DB 로드 중...")
        self.vectorstore = FAISS.load_local(
            folder_path=DB_FAISS_PATH,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        # 주문 상태
        self.order_state = OrderState()
        
        print(f"✅ 하이브리드 챗봇 준비 완료! ({len(self.menus)}개 메뉴)\n")
    
    # ==================== 메인 로직 ====================
    
    def ask(self, user_input: str) -> str:
        """
        메인 대화 처리
        
        흐름:
        1. 명령어 체크 (취소, 장바구니 등)
        2. LLM으로 의도 파악
        3. 의도에 따라 처리
        4. LLM으로 자연스러운 응답 생성
        """
        
        # 대화 기록
        self.order_state.conversation_history.append({"role": "user", "content": user_input})
        
        # 명령어 처리
        if user_input.lower() in ['취소', '리셋', '처음부터']:
            self.order_state.reset()
            return "주문이 취소되었습니다. 다시 시작해주세요! 😊"
        
        if user_input.lower() in ['장바구니', '카트', '주문내역']:
            return self.order_state.get_cart_summary()
        
        # LLM으로 의도 파악
        intent = self._analyze_intent(user_input)
        
        # 의도에 따라 처리
        response = self._handle_intent(user_input, intent)
        
        # 대화 기록
        self.order_state.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    # ==================== 의도 파악 (LLM) ====================
    
    def _analyze_intent(self, user_input: str) -> dict:
        """
        LLM으로 사용자 의도 파악
        
        Returns:
            {
                "type": "order" / "question" / "confirm" / "cancel",
                "menu_name": "아메리카노",
                "size": "Large",
                "quantity": 1,
                "details": "추가 정보"
            }
        """
        
        # 현재 상태 컨텍스트
        stage = self.order_state.stage
        cart_summary = self.order_state.get_cart_summary()
        
        # LLM 프롬프트
        prompt = f"""당신은 카페 주문 의도를 파악하는 AI입니다.

현재 상태: {stage}
현재 주문: {cart_summary}

사용자 입력: "{user_input}"

사용자의 의도를 파악하여 JSON으로 답하세요:

의도 타입:
- "order": 메뉴 주문 (예: "아메리카노 1잔", "콜드브루 라지")
- "question": 질문 (예: "추천해줘", "화장실 어디?", "가격 얼마?")
- "confirm_yes": 긍정 확인 (예: "ㅇ","네", "예", "응", "그래")
- "confirm_no": 부정 확인 (예: "ㄴ","아니", "아니요", "괜찮아")
- "serving": 매장/포장 선택 (예: "포장", "매장", "테이크아웃")
- "payment": 결제 방식 (예: "카드", "현금","민생지원금","적립도장")

JSON 형식 (필수):
{{
    "type": "order|question|confirm_yes|confirm_no|serving|payment",
    "menu_name": "메뉴명 (있으면)",
    "size": "Regular|Large|Extra Large (있으면)",
    "quantity": 1,
    "details": "기타 정보"
}}

JSON만 출력하세요:"""
        
        try:
            response = self.llm.invoke(prompt)
            import json
            intent = json.loads(response.content)
            return intent
        except:
            # 파싱 실패시 기본값
            return {"type": "question", "menu_name": None, "details": user_input}
    
    # ==================== 의도 처리 ====================
    
    def _handle_intent(self, user_input: str, intent: dict) -> str:
        """의도에 따라 처리하고 응답 생성"""
        
        intent_type = intent.get("type", "question")
        
        # 1. 주문 의도
        if intent_type == "order":
            return self._handle_order(user_input, intent)
        
        # 2. 긍정 확인 (추가 주문, 포장 등)
        elif intent_type == "confirm_yes":
            return self._handle_confirm_yes(user_input)
        
        # 3. 부정 확인
        elif intent_type == "confirm_no":
            return self._handle_confirm_no(user_input)
        
        # 4. 매장/포장 선택
        elif intent_type == "serving":
            return self._handle_serving(user_input, intent)
        
        # 5. 결제 방식
        elif intent_type == "payment":
            return self._handle_payment(user_input, intent)
        
        # 6. 일반 질문 → RAG
        else:
            return self._handle_question(user_input)
    
    # ==================== 주문 처리 ====================
    
    def _handle_order(self, user_input: str, intent: dict) -> str:
        """주문 처리"""
        
        menu_name = intent.get("menu_name")
        
        if not menu_name:
            # LLM으로 메뉴 추출 재시도
            menu_name = self._extract_menu_name(user_input)
        
        if not menu_name:
            return self._generate_response(
                user_input, 
                "menu_not_found",
                "어떤 메뉴를 주문하시겠어요? 메뉴명을 말씀해주세요."
            )
        
        # 메뉴 검색
        menu_info = self._find_menu(menu_name)
        
        if not menu_info:
            return self._generate_response(
                user_input,
                "menu_not_found", 
                f"'{menu_name}' 메뉴를 찾을 수 없습니다. 다른 메뉴를 말씀해주시겠어요?"
            )
        
        # 사이즈 파악
        size = intent.get("size") or self._extract_size(user_input)
        
        if not size:
            # 사이즈 질문
            self.order_state.pending_item = menu_info
            self.order_state.stage = 'size_selection'
            
            available_sizes = list(menu_info['size_prices'].keys())
            size_options = ", ".join(available_sizes)
            
            return self._generate_response(
                user_input,
                "ask_size",
                f"{menu_info['name']}의 사이즈를 선택해주세요. ({size_options})"
            )
        
        # 수량 파악
        quantity = intent.get("quantity", 1)
        
        # 주문 추가
        price = menu_info['size_prices'].get(size, menu_info['base_price'])
        item = OrderItem(
            menu_id=menu_info['menu_id'],
            menu_name=menu_info['name'],
            size=size,
            price=price,
            quantity=quantity
        )
        
        self.order_state.add_to_cart(item)
        self.order_state.stage = 'confirm'
        
        # 응답 생성
        cart_summary = self.order_state.get_cart_summary()
        
        return self._generate_response(
            user_input,
            "order_added",
            f"{item}가 담겼습니다!\n\n{cart_summary}\n\n다른 메뉴도 추가하시겠어요?"
        )
    
    def _handle_confirm_yes(self, user_input: str) -> str:
        """긍정 확인 처리"""
        
        stage = self.order_state.stage
        
        # 추가 주문
        if stage == 'confirm':
            self.order_state.stage = 'browsing'
            return self._generate_response(
                user_input,
                "add_more",
                "추가하실 메뉴를 말씀해주세요!"
            )
        
        # 기본 응답
        return self._generate_response(user_input, "confirm_yes", "네, 알겠습니다!")
    
    def _handle_confirm_no(self, user_input: str) -> str:
        """부정 확인 처리"""
        
        stage = self.order_state.stage
        
        # 주문 완료 후 → 매장/포장 선택
        if stage == 'confirm':
            self.order_state.stage = 'serving'
            return self._generate_response(
                user_input,
                "ask_serving",
                "매장에서 드시겠어요, 포장하시겠어요?"
            )
        
        # 기본 응답
        return self._generate_response(user_input, "confirm_no", "알겠습니다!")
    
    def _handle_serving(self, user_input: str, intent: dict) -> str:
        """매장/포장 선택"""
        
        details = intent.get("details", "").lower()
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['포장', '테이크아웃', 'takeout', '가져']):
            self.order_state.serving_type = 'takeout'
            serving_text = "포장"
        else:
            self.order_state.serving_type = 'dine_in'
            serving_text = "매장"
        
        self.order_state.stage = 'payment'
        
        cart_summary = self.order_state.get_cart_summary()
        
        return self._generate_response(
            user_input,
            "ask_payment",
            f"{serving_text}으로 준비하겠습니다!\n\n{cart_summary}\n\n결제 방법을 선택해주세요. (카드/현금/민생지원금)"
        )
    
    def _handle_payment(self, user_input: str, intent: dict) -> str:
        """결제 처리"""
        
        user_lower = user_input.lower()
        
        if '카드' in user_lower or 'card' in user_lower:
            payment = "카드"
        elif '현금' in user_lower or 'cash' in user_lower:
            payment = "현금"
        elif '민생' in user_lower or '지원' in user_lower:
            payment = "민생지원금"
        else:
            payment = "카드"
        
        self.order_state.payment_method = payment
        self.order_state.stage = 'done'
        
        # 최종 주문 요약
        cart_summary = self.order_state.get_cart_summary()
        serving_text = "포장" if self.order_state.serving_type == 'takeout' else "매장"
        
        final_summary = f"""🎉 주문이 완료되었습니다!

{cart_summary}

📋 주문 정보:
- 서빙: {serving_text}
- 결제: {payment}

☕ 음료 곧 준비해드리겠습니다!
주문해주셔서 감사합니다~ 😊

💡 새로운 주문: '처음부터'"""
        
        return final_summary
    
    # ==================== 일반 질문 (RAG) ====================
    
    def _handle_question(self, user_input: str) -> str:
        """일반 질문 → RAG로 답변"""
        
        # 벡터 검색
        results = self.vectorstore.similarity_search(user_input, k=3)
        
        if not results:
            return "죄송합니다. 관련 정보를 찾을 수 없습니다. 다시 질문해주시겠어요?"
        
        # 컨텍스트 생성
        context = "\n\n".join([doc.page_content for doc in results])
        
        # LLM으로 답변 생성
        response = self._generate_response(user_input, "rag_answer", None, context)
        
        return response
    
    # ==================== LLM 응답 생성 ====================
    
    def _generate_response(self, user_input: str, response_type: str, 
                          default_response: str = None, context: str = None) -> str:
        """
        LLM으로 자연스러운 응답 생성
        
        Args:
            user_input: 사용자 입력
            response_type: 응답 타입 (order_added, ask_size, rag_answer 등)
            default_response: 기본 응답 (LLM 실패시 사용)
            context: RAG 컨텍스트 (있으면)
        """
        
        # 대화 히스토리
        history = "\n".join([
            f"{'고객' if msg['role'] == 'user' else '직원'}: {msg['content']}"
            for msg in self.order_state.conversation_history[-4:]
        ])
        
        # 현재 상태
        cart = self.order_state.get_cart_summary()
        
        # LLM 프롬프트
        prompt = f"""당신은 친절한 카페 직원입니다.

[대화 기록]
{history}

[현재 주문]
{cart}

[상황]
응답 타입: {response_type}
고객 말: "{user_input}"
{f'메뉴 정보: {context}' if context else ''}

위 상황에 맞게 친절하고 자연스럽게 응답하세요. (2-3문장, 이모지 사용 OK)
기본 응답 참고: {default_response if default_response else ''}

응답:"""
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except:
            # LLM 실패시 기본 응답
            return default_response or "죄송합니다. 다시 말씀해주시겠어요?"
    
    # ==================== 헬퍼 함수 ====================
    
    def _find_menu(self, menu_name: str) -> Optional[dict]:
        """메뉴 찾기"""
        menu_name_lower = menu_name.lower().strip()
        
        for menu in self.menus:
            # 이름 매칭
            if menu_name_lower in menu['name'].lower():
                return menu
            
            # 동의어 매칭
            for synonym in menu.get('synonyms', []):
                if menu_name_lower in synonym.lower() or synonym.lower() in menu_name_lower:
                    return menu
        
        return None
    
    def _extract_menu_name(self, text: str) -> Optional[str]:
        """텍스트에서 메뉴명 추출"""
        text_lower = text.lower()
        
        for menu in self.menus:
            for synonym in menu.get('synonyms', []):
                if synonym.lower() in text_lower:
                    return menu['name']
        
        return None
    
    def _extract_size(self, text: str) -> Optional[str]:
        """텍스트에서 사이즈 추출"""
        text_lower = text.lower()
        
        size_map = {
            'regular': 'Regular', 'r': 'Regular', '레귤러': 'Regular', '레굴': 'Regular',
            'large': 'Large', 'l': 'Large', '라지': 'Large',
            'extra large': 'Extra Large', 'xl': 'Extra Large', '엑스트라라지': 'Extra Large'
        }
        
        for key, value in size_map.items():
            if key in text_lower:
                return value
        
        return None


# ==================== 메인 실행 ====================

if __name__ == "__main__":
    try:
        chatbot = HybridCafeChatbot()
        
        print("=" * 60)
        print("🤖 스마트 카페 하이브리드 챗봇")
        print("=" * 60)
        print("✨ 특징:")
        print("   💬 자연스러운 대화 (LLM)")
        print("   ✅ 정확한 주문 처리 (코드)")
        print("   🔍 메뉴 정보 검색 (RAG)")
        print("=" * 60)
        print("\n💡 명령어: '장바구니', '처음부터', '종료'\n")
        
        while True:
            try:
                user_input = input("👤 고객: ").strip()
                
                if user_input.lower() in ['종료', 'exit', 'quit']:
                    print("\n🤖 직원: 감사합니다! 좋은 하루 되세요~ ☕\n")
                    break
                
                if not user_input:
                    continue
                
                response = chatbot.ask(user_input)
                print(f"\n🤖 직원: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 직원: 감사합니다! 좋은 하루 되세요~ ☕\n")
                break
            except Exception as e:
                print(f"\n⚠️ 오류: {e}\n")
                
    except Exception as e:
        print(f"\n❌ 초기화 오류: {e}\n")
        import traceback
        traceback.print_exc()