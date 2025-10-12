# cafe_rag_chatbot_conversational.py

import os
from typing import Optional, List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from cafe_menu_data import CAFE_DATA

DB_PATH = "vector_db"
DB_FAISS_PATH = os.path.join(DB_PATH, "faiss_index")

class ConversationState:
    """대화 상태 관리"""
    def __init__(self):
        self.status = 'ready'  # ready, waiting_clarification, waiting_confirmation
        self.candidate_menus = []  # 후보 메뉴들
        self.last_query = ""
        self.selected_menu_id = None
    
    def reset(self):
        self.__init__()

class CafeRAGChatbot:
    """대화형 카페 RAG 챗봇 (상태 관리 포함)"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.embeddings = OpenAIEmbeddings()
        self.menus = CAFE_DATA.get('menus', [])
        
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
        
        # 대화 상태 추가
        self.conversation_state = ConversationState()
        
        self.rag_chain = self._create_rag_chain()
        print(f"✅ 대화형 RAG 챗봇 준비 완료 ({len(self.menus)}개 메뉴)\n")

    def _detect_ambiguous_query(self, query: str, results: List[tuple]) -> bool:
        """애매한 질문인지 판단"""
        query_lower = query.lower()
        
        # 1. 가격/칼로리 질문인데 메뉴명이 불명확한 경우
        price_keywords = ['얼마', '가격', '몇원', '비용', '돈']
        calorie_keywords = ['칼로리', '열량', 'kcal']
        
        is_price_query = any(kw in query_lower for kw in price_keywords)
        is_calorie_query = any(kw in query_lower for kw in calorie_keywords)
        
        # 2. 일반 명사만 있고 구체적 메뉴명이 없는 경우
        generic_terms = ['라떼', '커피', '차', '음료', '디저트', '케이크', '샌드위치']
        has_generic_term = any(term in query_lower for term in generic_terms)
        
        # 3. 여러 메뉴가 검색되었는지 확인
        multiple_results = len(results) > 1
        
        # 애매한 질문 기준: (가격/칼로리 질문 OR 일반 명사만) AND 여러 결과
        if (is_price_query or is_calorie_query or has_generic_term) and multiple_results:
            # 최상위 결과가 압도적으로 높은 점수가 아니면 애매하다고 판단
            if len(results) >= 2:
                top_score = results[0][1]
                second_score = results[1][1]
                # 점수 차이가 2배 미만이면 애매함
                if top_score < second_score * 2:
                    return True
        
        return False

    def _format_menu_list(self, results: List[tuple], max_items: int = 5) -> str:
        """메뉴 목록을 사용자에게 보기 좋게 포맷팅"""
        lines = []
        for i, (doc, score) in enumerate(results[:max_items], 1):
            meta = doc.metadata
            price = meta.get('base_price', 'N/A')
            lines.append(f"{i}) {meta['name']} - Regular {price}원")
        return "\n".join(lines)

    def _handle_menu_selection(self, user_input: str) -> Optional[str]:
        """사용자의 메뉴 선택 처리 (숫자 or 메뉴명)"""
        user_input_lower = user_input.lower().strip()
        
        # 1. 숫자로 선택한 경우
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(self.conversation_state.candidate_menus):
                menu_id = self.conversation_state.candidate_menus[idx][0].metadata['menu_id']
                return menu_id
        
        # 2. 메뉴명으로 선택한 경우
        for doc, score in self.conversation_state.candidate_menus:
            menu_name = doc.metadata['name'].lower()
            if user_input_lower in menu_name or menu_name in user_input_lower:
                return doc.metadata['menu_id']
        
        return None

    def _detect_search_intent(self, query: str) -> dict:
        """질문 의도 분석"""
        query_lower = query.lower()
        intent = {'type': 'specific', 'category': None}
        
        category_keywords = {
            '커피': ['커피', '아메리카노', '라떼', '카푸치노', '에스프레소', '모카'],
            '콜드브루': ['콜드브루', '콜드', '더치'],
            '프라푸치노': ['프라푸치노', '프라페', '프라푸'],
            '블렌디드': ['블렌디드', '스무디'],
            '차': ['차', '티', '녹차', '말차', '얼그레이', '유자'],
            '디저트': ['디저트', '케이크', '샌드위치', '토스트', '베이글', '빵']
        }
        
        if any(kw in query_lower for kw in ['종류', '메뉴', '뭐있', '어떤게', '무엇', '전체', '리스트']):
            intent['type'] = 'category'
            for category, keywords in category_keywords.items():
                if any(kw in query_lower for kw in keywords):
                    intent['category'] = category
                    break
        
        return intent

    def _category_search(self, category: str, k: int = 20) -> list[tuple[Document, float]]:
        """카테고리별 메뉴 검색"""
        results = []
        for menu in self.menus:
            if menu['category'] == category or category in menu.get('tags', []):
                doc = self.doc_map.get(menu['menu_id'])
                if doc:
                    score = 100.0 * doc.metadata.get('search_boost_score', 1.0)
                    results.append((doc, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _search(self, query: str, k: int = 10) -> list[tuple[Document, float]]:
        """하이브리드 검색"""
        intent = self._detect_search_intent(query)
        
        if intent['type'] == 'category' and intent['category']:
            print(f"📂 카테고리 검색: '{intent['category']}'")
            return self._category_search(intent['category'], k=20)
        
        query_lower = query.lower().strip()
        synonym_matches = []
        
        for menu in self.menus:
            for synonym in menu['synonyms']:
                synonym_lower = synonym.lower()
                
                if query_lower == synonym_lower:
                    doc = self.doc_map.get(menu['menu_id'])
                    if doc:
                        synonym_matches.append((doc, 1000.0, f"완전일치: '{synonym}'"))
                
                elif synonym_lower in query_lower or query_lower in synonym_lower:
                    doc = self.doc_map.get(menu['menu_id'])
                    if doc:
                        similarity = min(len(query_lower), len(synonym_lower)) / \
                                   max(len(query_lower), len(synonym_lower))
                        score = 500.0 * similarity * \
                               doc.metadata.get('search_boost_score', 1.0)
                        synonym_matches.append((doc, score, f"부분일치: '{synonym}'"))
        
        if synonym_matches:
            synonym_matches.sort(key=lambda x: x[1], reverse=True)
            print(f"🎯 동의어 매칭 ({len(synonym_matches)}개): '{query}'")
            for doc, score, match_type in synonym_matches[:3]:
                print(f"   - {doc.metadata['name']} (점수: {score:.1f}, {match_type})")
            return [(doc, score) for doc, score, _ in synonym_matches]
        
        print(f"🔍 벡터 유사도 검색: '{query}'")
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        weighted = [
            (doc, (1 / (1 + score)) * doc.metadata.get('search_boost_score', 1.0))
            for doc, score in results
        ]
        weighted.sort(key=lambda x: x[1], reverse=True)
        return weighted

    def _create_specific_info_prompt(self, menu_id: str) -> str:
        """특정 메뉴의 상세 정보 Context 생성"""
        doc = self.doc_map.get(menu_id)
        if not doc:
            return "메뉴를 찾을 수 없습니다."
        
        meta = doc.metadata
        size_prices = meta.get('size_prices', {})
        calories = meta.get('calories', {})
        allergens = meta.get('allergens', [])
        promotion = meta.get('promotion')
        
        info = f"""[선택하신 메뉴] {meta.get('name', 'N/A')}
- 카테고리: {meta.get('category', 'N/A')}
- 가격: Regular {meta.get('base_price', 'N/A')}원"""
        
        if size_prices.get('Large'):
            info += f", Large {size_prices.get('Large', 'N/A')}원"
        if size_prices.get('Extra Large'):
            info += f", Extra Large {size_prices.get('Extra Large', 'N/A')}원"
        
        info += f"\n- 설명: {meta.get('description', 'N/A')}"
        info += f"\n- 칼로리: {calories.get('regular', 'N/A')}kcal (Regular 기준)"
        info += f"\n- 알러지 유발 성분: {', '.join(allergens) if allergens else '없음'}"
        
        if promotion:
            info += f"\n- 🎁 프로모션: {promotion.get('description')}"
        
        return info

    def _create_rag_chain(self):
        """RAG Chain 생성 (상세 정보용)"""
        system_prompt = """
당신은 스마트 카페의 전문 바리스타 AI입니다. 고객이 특정 메뉴를 선택했으므로 해당 메뉴의 정확한 정보를 제공하세요.

**답변 규칙**:
1. 아래 [메뉴 정보]의 내용만 사용하여 답변하세요.
2. 가격은 모든 사이즈를 안내하되, "Regular 사이즈 기준"을 명시하세요.
3. 프로모션이 있으면 🎁 이모지와 함께 강조하세요.
4. 친절하고 간결하게 2-3 문장으로 답변하세요.

[메뉴 정보]
{context}

[고객 질문]
{question}

[AI 바리스타 답변]
"""
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])
        
        return (
            {"context": lambda x: x['context'], "question": lambda x: x['question']}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, query: str) -> str:
        """대화 상태 기반 응답 생성"""
        
        # 상태 1: 메뉴 선택 대기 중
        if self.conversation_state.status == 'waiting_clarification':
            # 사용자가 메뉴를 선택했는지 확인
            selected_menu_id = self._handle_menu_selection(query)
            
            if selected_menu_id:
                # 선택된 메뉴의 상세 정보 제공
                self.conversation_state.selected_menu_id = selected_menu_id
                context = self._create_specific_info_prompt(selected_menu_id)
                response = self.rag_chain.invoke({
                    "context": context,
                    "question": self.conversation_state.last_query
                })
                
                # 상태 초기화
                self.conversation_state.reset()
                return response
            
            else:
                # 선택하지 못함 - 더 많은 옵션 제공 또는 재질문
                return "죄송합니다. 선택하신 메뉴를 찾지 못했습니다. 메뉴 번호(1, 2, 3...)나 정확한 메뉴명을 입력해주세요."
        
        # 상태 2: 일반 질문 처리
        results = self._search(query, k=10)
        
        if not results:
            return "죄송합니다. 관련 메뉴를 찾을 수 없습니다. 다른 메뉴나 질문으로 도와드릴까요?"
        
        # 애매한 질문인지 판단
        if self._detect_ambiguous_query(query, results):
            # 후보 메뉴 저장 및 상태 변경
            self.conversation_state.status = 'waiting_clarification'
            self.conversation_state.candidate_menus = results[:5]  # 상위 5개
            self.conversation_state.last_query = query
            
            # 후보 목록 제시
            menu_list = self._format_menu_list(results, max_items=5)
            
            response = f"""관련 메뉴가 여러 개 있습니다. 어떤 메뉴를 찾으시나요?

{menu_list}

💡 메뉴 번호(1, 2, 3...)나 정확한 메뉴명을 말씀해주세요."""
            
            print(f"🔄 대화 상태 변경: waiting_clarification")
            return response
        
        # 명확한 질문 - 즉시 답변
        else:
            # 최상위 메뉴의 상세 정보로 답변
            top_menu_id = results[0][0].metadata['menu_id']
            context = self._create_specific_info_prompt(top_menu_id)
            
            return self.rag_chain.invoke({
                "context": context,
                "question": query
            })


if __name__ == "__main__":
    try:
        cafe_bot = CafeRAGChatbot()
        
        print("="*60)
        print("🤖 스마트 카페 AI 바리스타 (대화형 버전)")
        print("="*60)
        print("💡 테스트 질문 예시:")
        print("   - 라떼 얼마야?  (여러 메뉴 제시 후 선택)")
        print("   - 카페 라떼 얼마야?  (즉시 답변)")
        print("   - 디저트 종류")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("👤 질문: ").strip()
                
                if user_input.lower() in ['종료', 'exit', 'quit', '초기화']:
                    if user_input.lower() == '초기화':
                        cafe_bot.conversation_state.reset()
                        print("\n🔄 대화 상태가 초기화되었습니다.\n")
                        continue
                    else:
                        print("\n🤖 감사합니다! ☕\n")
                        break
                
                if not user_input:
                    continue
                
                print(f"\n[현재 상태: {cafe_bot.conversation_state.status}]")
                print("🤖 답변: ", end="")
                response = cafe_bot.ask(user_input)
                print(response)
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n🤖 감사합니다! ☕\n")
                break
            except Exception as e:
                print(f"\n⚠️ 오류: {e}\n")
                cafe_bot.conversation_state.reset()
                
    except Exception as e:
        print(f"\n❌ 오류: {e}\n")