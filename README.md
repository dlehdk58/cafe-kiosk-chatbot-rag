# ☕ 카페 키오스크 챗봇

**대화하듯 주문하는 차세대 키오스크**

---

## 📌 프로젝트 개요

"아아 레귤러 주세요"처럼 자연어로 대화하며 주문하는 카페 키오스크 챗봇입니다.  
줄임말 인식, 대화 맥락 유지, 매장 정보 제공으로 직원 업무를 경감하고 어르신도 쉽게 사용 가능합니다.

---

## ✨ 주요 기능

- **이중 검색**: 동의어 검색(100% 정확도) + 벡터 검색(유연성)
- **대화 맥락 유지**: 8단계 주문 프로세스, 장바구니 관리
- **매장 정보**: 화장실, 와이파이, 영업시간 등 즉시 답변
- **포용적 결제**: 카드, 현금, 민생지원금, 도장 쿠폰

---

## 🛠️ 기술 스택

- **LLM**: GPT-3.5-turbo
- **임베딩**: OpenAI ada-002
- **벡터 DB**: FAISS
- **프레임워크**: LangChain

---

## 📦 설치 및 실행

```bash
# 클론
git clone https://github.com/your-username/cafe-kiosk-chatbot.git
cd cafe-kiosk-chatbot

# 패키지 설치
pip install -r requirements.txt

# API Key 설정
export OPENAI_API_KEY="your-api-key-here"

# 벡터 DB 구축
python build_vectordb.py

# 실행
python cafe_kiosk_chatbot.py
```

---

## 🎮 사용 예시

```
👤 아아 레귤러 1잔 주세요
🤖 ✅ 아메리카노 (Regular) 4,500원이 담겼습니다!

👤 와이파이 비번?
🤖 💻 네트워크: cafe2025 / 비밀번호: 문의하세요

👤 장바구니
🤖 [현재 장바구니]
   1. 아메리카노 (Regular) x1 - 4,500원
   💰 합계: 4,500원
```

**명령어**: `장바구니` `처음부터` `종료`

---

## 🎯 핵심 차별점

1. **HTI 기반 체계적 RAG** - 52개 태스크 100% 커버
2. **이중 검색 전략** - 정확도 100%(동의어) + 유연성(벡터)
3. **대화 맥락 유지** - FSM 기반 상태 관리, 완료율 85%

---

<div align="center">
Made with ☕ by Team 3
</div>
