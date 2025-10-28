"""
RAG 시스템을 위한 FAISS 벡터 DB 구축 스크립트

이 스크립트는 cafe_menu.py의 JSON 데이터를 읽어서
메타데이터 필터링이 가능한 FAISS 벡터 DB를 구축합니다.

주요 특징:
- 기존 메타데이터를 원본 구조 그대로 보존 (리스트는 리스트, 딕셔너리는 딕셔너리)
- page_content: 검색용 텍스트
- metadata: 필터링을 위한 구조화된 데이터
- type 필드로 데이터 타입 구분 (option, service, loyalty_program, store_info)
"""

import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

# cafe_menu.py에서 데이터 불러오기
from cafe_menu import CAFE_DATA

# 벡터 DB 저장 경로 설정
DB_PATH = "vector_db"
DB_FAISS_PATH = os.path.join(DB_PATH, "faiss_index")


def create_menu_documents(menus: list) -> List[Document]:
    """
    메뉴 데이터를 Document 객체 리스트로 변환
    
    사고 과정:
    1. page_content: 검색될 가능성이 높은 텍스트 필드 결합 (name, category, description, tags, etc.)
    2. metadata: 모든 필드를 원본 구조 그대로 저장
    3. 리스트/딕셔너리 평탄화 절대 금지
    
    Args:
        menus: 메뉴 데이터 리스트
        
    Returns:
        Document 객체 리스트
    """
    documents = []
    
    for menu in menus:
        # page_content: 검색용 텍스트 (자연어 형태)
        page_content = f"""
메뉴명: {menu['name']}
카테고리: {menu['category']}
설명: {menu['description']}
태그: {', '.join(menu['tags'])}
추천 키워드: {', '.join(menu['recommendation_keywords'])}
동의어: {', '.join(menu['synonyms'])}
""".strip()
        
        # metadata: 모든 필드를 원본 구조 그대로 저장
        # 리스트는 리스트로, 딕셔너리는 딕셔너리로 유지
        metadata = {
            "menu_id": menu["menu_id"],
            "name": menu["name"],
            "category": menu["category"],
            "description": menu["description"],
            "base_price": menu["base_price"],
            "price_note": menu["price_note"],
            "size_prices": menu["size_prices"],  # 딕셔너리 그대로
            "caffeine": menu["caffeine"],  # 딕셔너리 그대로
            "calories": menu["calories"],  # 딕셔너리 그대로
            "allergens": menu["allergens"],  # 리스트 그대로
            "temperature": menu["temperature"],  # 리스트 그대로
            "tags": menu["tags"],  # 리스트 그대로
            "recommendation_keywords": menu["recommendation_keywords"],  # 리스트 그대로
            "synonyms": menu["synonyms"],  # 리스트 그대로
            "search_boost_score": menu["search_boost_score"]
        }
        
        # subcategory가 있는 경우만 추가
        if "subcategory" in menu:
            metadata["subcategory"] = menu["subcategory"]
        
        # promotion이 있는 경우만 추가
        if "promotion" in menu:
            metadata["promotion"] = menu["promotion"]  # 딕셔너리 그대로
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
    
    return documents


def create_option_documents(options: list) -> List[Document]:
    """
    옵션 데이터를 Document 객체 리스트로 변환
    
    사고 과정:
    1. 메뉴와 구분하기 위해 type='option' 추가
    2. 리스트 필드(applicable_categories, synonyms, syrup_types)는 그대로 유지
    3. 필드 존재 여부 확인 후 추가 (applicable_menus, applicable_condition 등)
    
    Args:
        options: 옵션 데이터 리스트
        
    Returns:
        Document 객체 리스트
    """
    documents = []
    
    for option in options:
        # page_content: 검색용 텍스트
        page_content = f"""
옵션명: {option['name']}
설명: {option['description']}
가격: +{option['price']}원
동의어: {', '.join(option['synonyms'])}
""".strip()
        
        # metadata: 기본 필드 + type='option'
        metadata = {
            "type": "option",  # 메뉴와 구분
            "option_id": option["option_id"],
            "name": option["name"],
            "description": option["description"],
            "price": option["price"],
            "applicable_categories": option["applicable_categories"],  # 리스트 그대로
            "synonyms": option["synonyms"]  # 리스트 그대로
        }
        
        # applicable_menus가 있는 경우만 추가
        if "applicable_menus" in option:
            metadata["applicable_menus"] = option["applicable_menus"]
        
        # applicable_condition이 있는 경우만 추가
        if "applicable_condition" in option:
            metadata["applicable_condition"] = option["applicable_condition"]
        
        # syrup_types가 있는 경우만 추가
        if "syrup_types" in option:
            metadata["syrup_types"] = option["syrup_types"]  # 리스트 그대로
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
    
    return documents


def create_service_documents(services: list) -> List[Document]:
    """
    포장/서비스 데이터를 Document 객체 리스트로 변환
    
    사고 과정:
    1. price가 음수인 경우(할인)도 그대로 유지
    2. type 필드가 있는 경우 그대로 저장
    
    Args:
        services: 포장/서비스 데이터 리스트
        
    Returns:
        Document 객체 리스트
    """
    documents = []
    
    for service in services:
        # price 표시 (음수면 "할인", 양수면 "추가")
        price_text = f"-{abs(service['price'])}원 (할인)" if service['price'] < 0 else f"+{service['price']}원"
        
        # page_content: 검색용 텍스트
        page_content = f"""
서비스명: {service['name']}
설명: {service['description']}
가격: {price_text}
""".strip()
        
        # metadata: 모든 필드 그대로
        metadata = {
            "service_id": service["service_id"],
            "name": service["name"],
            "description": service["description"],
            "price": service["price"],  # 음수 그대로
            "applicable_menus": service["applicable_menus"]
        }
        
        # type이 있는 경우만 추가
        if "type" in service:
            metadata["type"] = service["type"]
        
        doc = Document(page_content=page_content, metadata=metadata)
        documents.append(doc)
    
    return documents


def create_loyalty_program_document(loyalty: dict) -> Document:
    """
    적립 프로그램 데이터를 Document 객체로 변환
    
    사고 과정:
    1. 딕셔너리를 하나의 Document로 변환
    2. type='loyalty_program' 추가
    3. 검색을 위해 동의어 추가
    
    Args:
        loyalty: 적립 프로그램 데이터
        
    Returns:
        Document 객체
    """
    # page_content: 검색용 텍스트 + 동의어
    page_content = f"""
적립 프로그램: {loyalty['name']}
설명: {loyalty['description']}
혜택: {loyalty['reward']}
동의어: 도장, 적립, 스탬프, 쿠폰, 할인, 무료음료, 포인트, 리워드
""".strip()
    
    # metadata: 모든 필드 + type='loyalty_program'
    metadata = {
        "type": "loyalty_program",
        "name": loyalty["name"],
        "description": loyalty["description"],
        "stamp_condition": loyalty["stamp_condition"],
        "reward": loyalty["reward"],
        "stamp_required": loyalty["stamp_required"],
        "free_item": loyalty["free_item"]
    }
    
    return Document(page_content=page_content, metadata=metadata)


def create_store_info_documents(store_info: dict) -> List[Document]:
    """
    매장 정보 데이터를 Document 객체 리스트로 변환
    
    사고 과정:
    1. 중첩 구조를 별도 Document로 분리 (hours, wifi, facilities.*, contact)
    2. 각 Document에 type='store_info', category 추가
    3. metadata['data']에 원본 딕셔너리 그대로 저장
    
    Args:
        store_info: 매장 정보 데이터
        
    Returns:
        Document 객체 리스트
    """
    documents = []
    
    # 1. hours Document
    if "hours" in store_info:
        hours = store_info["hours"]
        page_content = f"""
매장 정보: 영업시간
설명: {hours['description']}
동의어: 영업시간, 운영시간, 오픈, 시간, 몇시, 언제, 닫는시간, 여는시간
""".strip()
        metadata = {
            "type": "store_info",
            "category": "hours",
            "data": hours  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    # 2. wifi Document
    if "wifi" in store_info:
        wifi = store_info["wifi"]
        page_content = f"""
매장 정보: 와이파이
SSID: {wifi['ssid']}
비밀번호: {wifi['password']}
동의어: 와이파이, wifi, 무선인터넷, 인터넷, 비번, 비밀번호, 패스워드
""".strip()
        metadata = {
            "type": "store_info",
            "category": "wifi",
            "data": wifi  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    # 3. facilities.restroom Document
    if "facilities" in store_info and "restroom" in store_info["facilities"]:
        restroom = store_info["facilities"]["restroom"]
        page_content = f"""
매장 정보: 화장실
위치: {restroom['location']}
동의어: 화장실, toilet, restroom, 변기, 화장실위치, 휴게실
""".strip()
        metadata = {
            "type": "store_info",
            "category": "restroom",
            "data": restroom  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    # 4. facilities.parking Document
    if "facilities" in store_info and "parking" in store_info["facilities"]:
        parking = store_info["facilities"]["parking"]
        available_text = "예" if parking['available'] else "아니오"
        page_content = f"""
매장 정보: 주차
이용 가능: {available_text}
설명: {parking['description']}
동의어: 주차, 주차장, 차, 주차공간, 파킹, parking, 주차가능
""".strip()
        metadata = {
            "type": "store_info",
            "category": "parking",
            "data": parking  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    # 5. facilities.socket Document
    if "facilities" in store_info and "socket" in store_info["facilities"]:
        socket = store_info["facilities"]["socket"]
        available_text = "예" if socket['available'] else "아니오"
        page_content = f"""
매장 정보: 콘센트
이용 가능: {available_text}
설명: {socket['description']}
동의어: 콘센트, 충전, 플러그, 전원, 멀티탭, socket, 노트북, 충전가능
""".strip()
        metadata = {
            "type": "store_info",
            "category": "socket",
            "data": socket  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    # 6. contact Document
    if "contact" in store_info:
        contact = store_info["contact"]
        page_content = f"""
매장 정보: 연락처
전화번호: {contact['phone']}
인스타그램: {contact['instagram']}
동의어: 연락처, 전화번호, 전화, 문의, 인스타그램, 인스타, SNS
""".strip()
        metadata = {
            "type": "store_info",
            "category": "contact",
            "data": contact  # 원본 딕셔너리 그대로
        }
        documents.append(Document(page_content=page_content, metadata=metadata))
    
    return documents


def build_vector_db():
    """
    cafe_menu.py의 모든 데이터를 Document로 변환하고 FAISS 벡터 DB 구축
    
    처리 순서:
    1. menus → create_menu_documents()
    2. options → create_option_documents()
    3. packaging_and_services → create_service_documents()
    4. loyalty_program → create_loyalty_program_document()
    5. store_info → create_store_info_documents()
    6. 모든 Document를 하나의 리스트로 결합
    7. FAISS 벡터 DB 구축 및 저장
    """
    print("🚀 벡터 DB 구축을 시작합니다...\n")
    
    all_documents = []
    
    # 1. 메뉴 Document 생성
    menus = CAFE_DATA.get('menus', [])
    if menus:
        menu_docs = create_menu_documents(menus)
        all_documents.extend(menu_docs)
        print(f"✅ 메뉴: {len(menu_docs)}개 Document 생성")
    
    # 2. 옵션 Document 생성
    options = CAFE_DATA.get('options', [])
    if options:
        option_docs = create_option_documents(options)
        all_documents.extend(option_docs)
        print(f"✅ 옵션: {len(option_docs)}개 Document 생성")
    
    # 3. 포장/서비스 Document 생성
    services = CAFE_DATA.get('packaging_and_services', [])
    if services:
        service_docs = create_service_documents(services)
        all_documents.extend(service_docs)
        print(f"✅ 포장/서비스: {len(service_docs)}개 Document 생성")
    
    # 4. 적립 프로그램 Document 생성
    loyalty = CAFE_DATA.get('loyalty_program', {})
    if loyalty:
        loyalty_doc = create_loyalty_program_document(loyalty)
        all_documents.append(loyalty_doc)
        print(f"✅ 적립 프로그램: 1개 Document 생성")
    
    # 5. 매장 정보 Document 생성
    store_info = CAFE_DATA.get('store_info', {})
    if store_info:
        store_docs = create_store_info_documents(store_info)
        all_documents.extend(store_docs)
        print(f"✅ 매장 정보: {len(store_docs)}개 Document 생성")
    
    print(f"\n📊 총 {len(all_documents)}개의 Document 생성 완료\n")
    
    # 6. OpenAI 임베딩 모델 초기화
    print("🧠 OpenAI Embeddings 초기화 중...")
    embeddings = OpenAIEmbeddings()
    
    # 7. FAISS 벡터 DB 구축
    print("🔨 FAISS 벡터 DB 구축 중... (API 호출 발생)")
    vectorstore = FAISS.from_documents(
        documents=all_documents,
        embedding=embeddings
    )
    
    # 8. 벡터 DB 저장
    if not os.path.exists(DB_PATH):
        os.makedirs(DB_PATH)
    
    vectorstore.save_local(DB_FAISS_PATH)
    print(f"\n✅ 벡터 DB 구축 완료!")
    print(f"📁 저장 경로: {DB_FAISS_PATH}")
    print(f"📄 저장된 Document 개수: {len(all_documents)}개")
    
    # 9. Document 타입별 개수 요약
    print("\n📊 Document 타입별 요약:")
    menu_count = len([d for d in all_documents if 'menu_id' in d.metadata])
    option_count = len([d for d in all_documents if d.metadata.get('type') == 'option'])
    service_count = len([d for d in all_documents if 'service_id' in d.metadata])
    loyalty_count = len([d for d in all_documents if d.metadata.get('type') == 'loyalty_program'])
    store_count = len([d for d in all_documents if d.metadata.get('type') == 'store_info'])
    
    print(f"  - 메뉴: {menu_count}개")
    print(f"  - 옵션: {option_count}개")
    print(f"  - 포장/서비스: {service_count}개")
    print(f"  - 적립 프로그램: {loyalty_count}개")
    print(f"  - 매장 정보: {store_count}개")


if __name__ == "__main__":
    build_vector_db()