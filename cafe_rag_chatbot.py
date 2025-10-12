# cafe_rag_chatbot.py

import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 데이터 및 설정 ---
from cafe_menu_data import CAFE_DATA

DB_PATH = "vector_db"
DB_FAISS_PATH = os.path.join(DB_PATH, "faiss_index")

class CafeRAGChatbot:
    """카페 키오스크 RAG 챗봇 시스템 (운영용)"""

    def __init__(self):
        """초기화 시, 미리 구축된 벡터 DB를 로드합니다."""
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1)
        self.embeddings = OpenAIEmbeddings()
        
        # 1. 원본 메뉴 데이터 로드
        self.menus = CAFE_DATA.get('menus', [])
        
        # 2. 미리 만들어진 FAISS 벡터 DB 로드
        if not os.path.exists(DB_FAISS_PATH):
            raise FileNotFoundError(f"벡터 DB 파일을 찾을 수 없습니다. 먼저 build_vector_db.py를 실행하세요. 경로: {DB_FAISS_PATH}")
        
        print(f"📂 로컬 벡터 DB 로드 중: {DB_FAISS_PATH}")
        self.vectorstore = FAISS.load_local(
            folder_path=DB_FAISS_PATH,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )
        print("✅ 벡터 DB 로드 완료!")
        
        # [최적화] 동의어 검색 성능을 위해 menu_id-Document 맵 미리 생성
        self.doc_map = {doc.metadata['menu_id']: doc for doc in self.vectorstore.docstore._dict.values()}

        # 3. RAG Chain 생성
        self.rag_chain = self._create_rag_chain()
        
        print(f"🤖 카페 RAG 챗봇이 준비되었습니다. ({len(self.menus)}개 메뉴)")

    def _search(self, query: str, k: int = 5) -> list[tuple[Document, float]]:
        """동의어 직접 매칭과 벡터 검색을 결합한 하이브리드 검색"""
        query_lower = query.lower()
        
        # 1. 동의어 직접 매칭 (더 효율적인 방식으로 개선)
        for menu in self.menus:
            if any(synonym.lower() in query_lower for synonym in menu['synonyms']):
                matched_doc = self.doc_map.get(menu['menu_id'])
                if matched_doc:
                    print(f"🎯 동의어 직접 매칭: '{query}' -> '{menu['name']}'")
                    # 직접 매칭 시 매우 높은 점수 부여
                    return [(matched_doc, 100.0 * matched_doc.metadata.get('search_boost_score', 1.0))]

        # 2. 벡터 유사도 검색
        print(f"🔍 벡터 유사도 검색 수행: '{query}'")
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        # 3. Boost 점수 가중치 적용
        weighted = [
            (doc, (1 / (1 + score)) * doc.metadata.get('search_boost_score', 1.0))
            for doc, score in results
        ]
        weighted.sort(key=lambda x: x[1], reverse=True)
        return weighted

    def _format_context(self, results: list[tuple[Document, float]], max_results: int = 3) -> str:
        """검색 결과를 LLM에 전달할 Context 문자열로 포맷팅"""
        if not results:
            return "관련 메뉴를 찾을 수 없습니다."
            
        parts = []
        for i, (doc, score) in enumerate(results[:max_results], 1):
            meta = doc.metadata
            size_prices = meta.get('size_prices', {})
            calories = meta.get('calories', {})
            allergens = meta.get('allergens', [])
            promotion = meta.get('promotion')

            info = f"""
[메뉴 {i}] {meta.get('name', 'N/A')} (검색 점수: {score:.2f})
- 가격: Regular {meta.get('base_price', 'N/A')}원, Large {size_prices.get('Large', 'N/A')}원
- 칼로리: {calories.get('regular', 'N/A')}kcal (Regular 기준)
- 알러지: {', '.join(allergens) if allergens else '없음'}"""
            
            if promotion:
                info += f"\n- 프로모션: {promotion.get('description', '내용 없음')}"
            parts.append(info.strip())
            
        return "\n\n---\n\n".join(parts)

    def _create_rag_chain(self):
        """LangChain Expression Language (LCEL)를 사용하여 RAG Chain 생성"""
        system_prompt = """
당신은 스마트 카페의 전문 바리스타 AI입니다. 고객의 질문에 아래 규칙에 따라 정확하고 친절하게 답변하세요.

**규칙**:
1. 제공된 [검색된 메뉴 정보]만을 사용하여 답변해야 합니다. 정보에 없는 내용은 절대로 추측하거나 지어내지 마세요.
2. 가격, 칼로리 정보는 반드시 "Regular 사이즈 기준"이라고 명시하세요.
3. 고객의 질문 의도를 파악하여, 가장 관련성 높은 메뉴 1~2개를 중심으로 설명하세요.
4. 답변은 항상 부드럽고 친절한 존댓말을 사용하며, 2-3 문장으로 간결하게 핵심만 전달하세요.
5. 프로모션 정보가 있다면, 놓치지 말고 꼭 안내하여 고객에게 혜택을 주세요.
6. 관련된 메뉴를 찾지 못했다면, "죄송하지만 문의하신 내용과 정확히 일치하는 메뉴를 찾기 어렵습니다. 다른 주문을 도와드릴까요?" 라고만 답변하세요.

[검색된 메뉴 정보]
{context}

[고객 질문]
{question}

[AI 바리스타 답변]
"""
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])
        
        return (
            {
                "context": lambda x: self._format_context(self._search(x['question'])),
                "question": lambda x: x['question']
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def ask(self, query: str) -> str:
        """챗봇에게 질문하고 답변을 받습니다."""
        return self.rag_chain.invoke({"question": query})

if __name__ == "__main__":
    try:
        cafe_bot = CafeRAGChatbot()
        
        print("\n" + "="*60)
        print("☕️🍰 스마트 카페 AI 바리스타에 오신 것을 환영합니다!")
        print("="*60)
        print("💡 메뉴, 가격, 추천 등 무엇이든 물어보세요.")
        print("💡 종료하려면 '종료', 'exit', 'quit' 를 입력하세요.")
        print("="*60 + "\n")
        
        while True:
            try:
                # 사용자 입력 받기
                user_input = input("👤 질문: ").strip()
                
                # 종료 명령어 체크
                if user_input.lower() in ['종료', 'exit', 'quit', '나가기', '그만']:
                    print("\n👩🏻‍🍳 이용해 주셔서 감사합니다. 좋은 하루 보내세요! ☕\n")
                    break
                
                # 빈 입력 체크
                if not user_input:
                    print("👩🏻‍🍳 질문을 입력해주세요.\n")
                    continue
                
                # 챗봇 응답 생성
                print("\n👩🏻‍🍳 답변: ", end="")
                response = cafe_bot.ask(user_input)
                print(response)
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👩🏻‍🍳 이용해 주셔서 감사합니다. 좋은 하루 보내세요! ☕\n")
                break
            except Exception as e:
                print(f"\n⚠️ 오류가 발생했습니다: {e}\n")
                continue

    except FileNotFoundError as e:
        print(f"\n❌ 오류: {e}")
        print("💡 먼저 'python build_vector_db.py'를 실행하여 벡터 DB를 생성해주세요.\n")
    except Exception as e:
        print(f"\n❌ 알 수 없는 오류가 발생했습니다: {e}\n")