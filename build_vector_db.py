# build_vector_db.py

import os
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# --- 데이터 및 설정 ---
# cafe_menu_data.py에서 메뉴 데이터를 불러옵니다.
from cafe_menu_data import CAFE_DATA

DB_PATH = "vector_db"
DB_FAISS_PATH = os.path.join(DB_PATH, "faiss_index")

def _create_documents(menus: list[dict]) -> list[Document]:
    """메뉴 데이터로부터 LangChain Document 리스트를 생성합니다."""
    documents = []
    for menu in menus:
        page_content = f"""
메뉴명: {menu['name']}
카테고리: {menu['category']}
설명: {menu['description']}
태그: {', '.join(menu['tags'])}
추천 키워드: {', '.join(menu['recommendation_keywords'])}
동의어: {', '.join(menu['synonyms'])}
"""
        # Document 생성을 위해 필요한 모든 메타데이터를 포함시킵니다.
        metadata = {k: v for k, v in menu.items()}
        
        doc = Document(page_content=page_content.strip(), metadata=metadata)
        documents.append(doc)
    return documents

def build_and_save_vector_db():
    """
    메뉴 데이터로부터 FAISS 벡터 DB를 구축하고 로컬 파일 시스템에 저장합니다.
    """
    print("🚀 벡터 DB 구축을 시작합니다...")

    menus = CAFE_DATA.get('menus', [])
    if not menus:
        print("❗️ 메뉴 데이터가 없습니다. cafe_menu_data.py 파일을 확인하세요.")
        return

    # 1. Document 객체 생성
    documents = _create_documents(menus)
    print(f"📄 총 {len(documents)}개의 메뉴를 Document로 변환했습니다.")

    # 2. OpenAI 임베딩 모델 초기화
    embeddings = OpenAIEmbeddings()

    # 3. FAISS 벡터 DB 구축
    print("🧠 FAISS 벡터 DB를 구축 중입니다. (API 호출 발생)")
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    # 4. 로컬에 저장
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    vectorstore.save_local(DB_FAISS_PATH)
    print(f"✅ 벡터 DB 구축 완료! 저장 경로: {DB_FAISS_PATH}")

if __name__ == "__main__":
    build_and_save_vector_db()