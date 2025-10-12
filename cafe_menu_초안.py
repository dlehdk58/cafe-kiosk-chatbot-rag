#==================커피메뉴==================
{
  "menus": [
    {
      "menu_id": "C001",
      "name": "아메리카노",
      "category": "커피",
      "description": "진한 에스프레소에 뜨거운 물을 더한 클래식 커피. 커피 본연의 맛을 즐길 수 있습니다.",
      "base_price": 4500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 4500,
        "Large": 5000,
        "Extra Large": 6000
      },
      "caffeine": {
        "level": "고",
        "amount": "150mg (Regular 기준)"
      },
      "calories": {
        "regular": 10,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "진한", "클래식", "쓴맛", "저칼로리",
        "강한", "순수", "기본", "블랙",
        "뜨거운", "차가운",
        "잠깨는", "각성", "집중",
        "아침용", "오전", "점심후",
        "인기", "베스트", "1위"
      ],
      "recommendation_keywords": [
        "진한 커피", "강한 커피", "쓴 커피", "쌉싸름한",
        "에스프레소", "블랙 커피", "블랙",
        "저칼로리", "다이어트", "칼로리 낮은", "살안찌는",
        "잠깨는", "졸릴때", "각성", "집중", "공부",
        "시험기간", "밤샘", "야근", "피곤할때",
        "기본", "클래식", "심플한", "순수한",
        "아침", "오전", "점심후", "식후",
        "인기", "베스트", "가장 많이 찾는", "유명한"
      ],
      "synonyms": [
        "아메리카노",
        "아아", "아이아", "아이스아메리카노", "ice americano", "iced americano",
        "뜨아", "뜨거운 아메리카노", "hot americano",
        "아메", "아메리카노커피",
        "americano", "Americano", "아메리까노"
      ],
      "search_boost_score": 1.5,
      "promotion": {
        "type": "combo",
        "description": "샌드위치 메뉴와 함께 주문 시 아메리카노 Regular 500원 할인",
        "discount_amount": 500,
        "condition": "카테고리가 '디저트'이면서 이름에 '샌드위치' 또는 '토스트' 포함된 메뉴와 동시 주문"
      }
    },
    {
      "menu_id": "C002",
      "name": "카페 라떼",
      "category": "커피",
      "description": "에스프레소와 부드러운 스팀 우유의 조화. 고소하고 부드러운 맛이 특징입니다.",
      "base_price": 5000,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5000,
        "Large": 5500,
        "Extra Large": 6500
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 220,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "부드러운", "고소한", "우유", "마일드",
        "크리미", "밸런스", "중간맛",
        "뜨거운", "차가운",
        "대중적", "무난한", "인기",
        "아침", "브런치", "오후", "디저트용"
      ],
      "recommendation_keywords": [
        "부드러운", "고소한", "마일드한", "순한",
        "우유", "우유커피", "밀크커피",
        "쓰지않은", "안쓴", "달달한", "고소한맛",
        "커피처음", "커피입문", "초보자",
        "무난한", "대중적인", "인기있는",
        "아침", "브런치", "오후", "간식",
        "카페", "라떼", "latte"
      ],
      "synonyms": [
        "카페 라떼", "카페라떼",
        "라떼", "라테",
        "아라", "아이스라떼", "ice latte", "iced latte",
        "뜨라", "뜨거운라떼", "hot latte",
        "라떼커피", "밀크커피",
        "latte", "Latte", "cafe latte"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "C003",
      "name": "카페 모카",
      "category": "커피",
      "description": "초콜릿과 에스프레소의 달콤쌉싸름한 만남. 달콤한 초콜릿 향과 커피의 조화가 일품입니다.",
      "base_price": 5500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5500,
        "Large": 6000,
        "Extra Large": 7000
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 290,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "대두"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "달콤한", "초콜릿", "부드러운",
        "쌉싸름한", "디저트같은", "달달한",
        "뜨거운", "차가운",
        "오후", "간식", "디저트",
        "인기", "여성인기"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "초콜릿",
        "초코", "쌉싸름한", "달콤쌉싸름",
        "디저트같은", "디저트", "간식",
        "쓰지않은", "부드러운", "마일드",
        "초콜릿좋아", "초코좋아", "달거좋아",
        "오후", "티타임", "여유", "휴식"
      ],
      "synonyms": [
        "카페 모카", "카페모카",
        "모카", "모까",
        "아모", "아이스모카", "ice mocha", "iced mocha",
        "뜨모", "뜨거운모카", "hot mocha",
        "초코라떼", "초콜릿라떼", "초코커피",
        "mocha", "Mocha", "cafe mocha"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "C004",
      "name": "카푸치노",
      "category": "커피",
      "description": "에스프레소, 스팀 우유, 풍성한 거품의 3단 조화. 우유 거품의 부드러운 식감이 특징입니다.",
      "base_price": 5000,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5000,
        "Large": 5500,
        "Extra Large": 6500
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 120,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "부드러운", "거품", "고소한",
        "풍성한", "크리미", "폼",
        "뜨거운", "차가운",
        "클래식", "전통", "유럽풍",
        "아침", "브런치", "오전"
      ],
      "recommendation_keywords": [
        "거품", "폼", "풍성한", "부드러운",
        "고소한", "크리미", "우유거품",
        "클래식", "전통", "정통",
        "유럽", "이탈리안", "커피전문점",
        "라떼보다진한", "우유적은", "커피맛강한",
        "아침", "브런치", "오전"
      ],
      "synonyms": [
        "카푸치노", "까푸치노",
        "카푸", "까푸",
        "아카", "아이스카푸치노", "ice cappuccino", "iced cappuccino",
        "뜨카", "뜨거운카푸치노", "hot cappuccino",
        "cappuccino", "Cappuccino", "카푸치노커피"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "C005",
      "name": "카라멜 마키아또",
      "category": "커피",
      "description": "달콤한 카라멜과 에스프레소의 환상 궁합. 카라멜 드리즐이 더해진 부드러운 라떼입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 6400,
        "Extra Large": 7400
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 250,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "달콤한", "카라멜", "부드러운",
        "달달한", "시럽", "드리즐",
        "뜨거운", "차가운",
        "인기", "베스트", "시그니처",
        "오후", "간식", "디저트", "여성인기"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "카라멜",
        "캬라멜", "달콤쌉싸름", "시럽",
        "부드러운", "마일드", "고소한",
        "디저트같은", "간식", "달거좋아",
        "인기", "시그니처", "특별한",
        "오후", "티타임", "여유"
      ],
      "synonyms": [
        "카라멜 마키아또", "카라멜마키아또",
        "마키아또", "마끼아또", "마끼야또",
        "카라멜", "캬라멜",
        "아카마", "아이스카라멜마키아또", "ice caramel macchiato",
        "뜨카마", "뜨거운카라멜마키아또", "hot caramel macchiato",
        "macchiato", "Macchiato", "caramel macchiato"
      ],
      "search_boost_score": 1.4
    },
    {
      "menu_id": "C006",
      "name": "플랫 화이트",
      "category": "커피",
      "description": "벨벳처럼 부드러운 마이크로폼과 진한 에스프레소. 호주식 프리미엄 커피입니다.",
      "base_price": 5600,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5600,
        "Large": 6100,
        "Extra Large": 7100
      },
      "caffeine": {
        "level": "고",
        "amount": "130mg (Regular 기준)"
      },
      "calories": {
        "regular": 160,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "진한", "부드러운", "고급",
        "마이크로폼", "크리미", "벨벳",
        "뜨거운", "차가운",
        "프리미엄", "호주식", "전문점",
        "아침", "오전", "집중"
      ],
      "recommendation_keywords": [
        "진한", "진한커피", "강한커피",
        "부드러운", "크리미", "벨벳같은",
        "고급", "프리미엄", "특별한",
        "호주", "뉴질랜드", "전문점",
        "라떼보다진한", "우유적은", "커피맛살아있는",
        "아침", "오전", "집중", "잠깨는"
      ],
      "synonyms": [
        "플랫 화이트", "플랫화이트",
        "플화", "플랫",
        "아플", "아이스플랫화이트", "ice flat white",
        "뜨플", "뜨거운플랫화이트", "hot flat white",
        "flat white", "Flat White", "flatwhite"
      ],
      "search_boost_score": 1.0
    },
    {
      "menu_id": "C007",
      "name": "돌체 라떼",
      "category": "커피",
      "description": "달콤한 돌체 시럽이 어우러진 부드러운 라떼. 은은한 단맛이 매력적입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 6400,
        "Extra Large": 7400
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 270,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "달콤한", "부드러운", "시럽",
        "달달한", "은은한", "마일드",
        "뜨거운", "차가운",
        "인기", "여성인기",
        "오후", "간식", "디저트"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "은은한",
        "부드러운", "마일드", "순한",
        "시럽", "시럽라떼", "달거좋아",
        "쓰지않은", "부드러운맛", "고소달달",
        "오후", "티타임", "여유", "간식"
      ],
      "synonyms": [
        "돌체 라떼", "돌체라떼",
        "돌체", "돌체시럽",
        "아돌", "아이스돌체라떼", "ice dolce latte",
        "뜨돌", "뜨거운돌체라떼", "hot dolce latte",
        "dolce latte", "Dolce Latte", "돌체라테"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "C008",
      "name": "화이트 초콜릿 모카",
      "category": "커피",
      "description": "화이트 초콜릿의 달콤함과 에스프레소의 조화. 부드럽고 달콤한 맛이 특징입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 6400,
        "Extra Large": 7400
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 310,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "대두"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "달콤한", "초콜릿", "화이트초콜릿",
        "부드러운", "달달한", "디저트같은",
        "뜨거운", "차가운",
        "특별한", "프리미엄",
        "오후", "간식", "디저트", "여성인기"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "화이트초콜릿",
        "초콜릿", "초코", "화초", "하얀초콜릿",
        "부드러운", "마일드", "디저트같은",
        "쓰지않은", "순한", "달거좋아",
        "특별한", "프리미엄", "고급",
        "오후", "티타임", "여유", "간식"
      ],
      "synonyms": [
        "화이트 초콜릿 모카", "화이트초콜릿모카",
        "화초모카", "화이트모카", "화모",
        "아화모", "아이스화이트초콜릿모카", "ice white chocolate mocha",
        "뜨화모", "뜨거운화이트초콜릿모카", "hot white chocolate mocha",
        "white chocolate mocha", "White Mocha", "화이트쵸콜릿모카"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "C009",
      "name": "블랙 글레이즈드 라떼",
      "category": "커피",
      "description": "흑당의 깊은 단맛과 라떼의 시그니처 메뉴. 독특한 흑당 향이 매력적입니다.",
      "base_price": 6500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6500,
        "Large": 7000,
        "Extra Large": 8000
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 320,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "달콤한", "흑당", "시그니처",
        "특별한", "독특한", "깊은단맛",
        "뜨거운", "차가운",
        "인기", "베스트", "시즌",
        "오후", "간식", "디저트", "여성인기"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "흑당",
        "흑당라떼", "깊은단맛", "진한단맛",
        "특별한", "독특한", "시그니처",
        "인기", "베스트", "유행",
        "달거좋아", "디저트같은",
        "오후", "티타임", "간식"
      ],
      "synonyms": [
        "블랙 글레이즈드 라떼", "블랙글레이즈드라떼",
        "블글라", "블랙라떼", "블글",
        "흑당라떼", "흑당", "흑당커피",
        "아블글", "아이스블랙글레이즈드라떼", "ice black glazed latte",
        "뜨블글", "뜨거운블랙글레이즈드라떼", "hot black glazed latte",
        "black glazed latte", "Black Latte"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "C010",
      "name": "에스프레소",
      "category": "커피",
      "description": "순수한 커피 본연의 맛을 느끼는 진한 한 잔. 강렬한 커피의 정수입니다.",
      "base_price": 3700,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 3700,
        "Large": 3700,
        "Extra Large": 3700
      },
      "caffeine": {
        "level": "매우고",
        "amount": "150mg (Regular 기준)"
      },
      "calories": {
        "regular": 5,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["HOT"],
      "tags": [
        "진한", "강한", "순수", "쓴맛",
        "강렬한", "진짜커피", "블랙",
        "뜨거운",
        "저칼로리", "다이어트",
        "집중", "각성", "잠깨는",
        "전문가", "마니아", "커피러버"
      ],
      "recommendation_keywords": [
        "진한", "진한커피", "강한", "강렬한",
        "쓴", "쌉싸름한", "순수한", "블랙",
        "에스프레소", "espresso", "샷",
        "저칼로리", "다이어트", "살안찌는",
        "잠깨는", "졸릴때", "각성", "집중",
        "빨리", "간단히", "짧게",
        "진짜커피", "커피본연", "커피맛",
        "전문가", "마니아", "커피러버"
      ],
      "synonyms": [
        "에스프레소",
        "에쏘", "에소", "에스",
        "샷", "커피샷",
        "espresso", "Espresso",
        "에스프레쏘", "에스프레소커피"
      ],
      "search_boost_score": 0.9
    }
  ]
}

# ==================콜드브루==================
{
  "menus": [
    {
      "menu_id": "CB001",
      "name": "콜드 브루",
      "category": "콜드브루",
      "description": "찬물로 12시간 우려낸 부드럽고 깔끔한 커피. 쓴맛은 적고 카페인은 높습니다.",
      "base_price": 4900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 4900,
        "Large": 5400,
        "Extra Large": 6400
      },
      "caffeine": {
        "level": "고",
        "amount": "200mg (Regular 기준)"
      },
      "calories": {
        "regular": 5,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["ICED"],
      "tags": [
        "시원한", "부드러운", "깔끔한",
        "저칼로리", "블랙", "순수",
        "차가운",
        "강한카페인", "잠깨는", "각성",
        "여름", "더울때", "시원",
        "인기", "베스트"
      ],
      "recommendation_keywords": [
        "시원한", "차가운", "아이스",
        "부드러운", "깔끔한", "순한",
        "쓰지않은", "부드러운맛", "마일드",
        "저칼로리", "다이어트", "살안찌는",
        "강한카페인", "카페인많은", "잠깨는",
        "졸릴때", "각성", "집중", "공부",
        "여름", "더울때", "시원한거",
        "인기", "베스트", "유명한"
      ],
      "synonyms": [
        "콜드 브루", "콜드브루",
        "콜브", "콜드",
        "cold brew", "coldbrew", "Cold Brew",
        "더치커피", "더치", "수출",
        "콜드브루커피", "콜브루"
      ],
      "search_boost_score": 1.4
    },
    {
      "menu_id": "CB002",
      "name": "돌체 콜드 브루",
      "category": "콜드브루",
      "description": "달콤한 돌체 시럽이 더해진 콜드 브루. 부드러운 단맛과 강한 카페인의 조화입니다.",
      "base_price": 6000,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6000,
        "Large": 6500,
        "Extra Large": 7500
      },
      "caffeine": {
        "level": "고",
        "amount": "200mg (Regular 기준)"
      },
      "calories": {
        "regular": 180,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "시원한", "부드러운",
        "시럽", "은은한단맛",
        "차가운",
        "강한카페인", "잠깨는",
        "여름", "시원", "인기"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "은은한",
        "시원한", "차가운", "아이스",
        "부드러운", "마일드", "순한",
        "시럽", "시럽콜드브루", "달거좋아",
        "강한카페인", "잠깨는", "졸릴때",
        "여름", "더울때", "시원한거",
        "인기", "베스트"
      ],
      "synonyms": [
        "돌체 콜드 브루", "돌체콜드브루",
        "돌체콜브", "돌콜", "돌체브루",
        "dolce cold brew", "Dolce Cold Brew",
        "돌체시럽콜드브루", "시럽콜브"
      ],
      "search_boost_score": 1.2
    },
{
      "menu_id": "CB003",
      "name": "바닐라 크림 콜드 브루",
      "category": "콜드브루",
      "description": "부드러운 바닐라 크림이 올라간 콜드 브루. 크림의 부드러움과 콜드브루의 깔끔함이 어우러집니다.",
      "base_price": 5800,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5800,
        "Large": 6300,
        "Extra Large": 7300
      },
      "caffeine": {
        "level": "고",
        "amount": "200mg (Regular 기준)"
      },
      "calories": {
        "regular": 190,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "크림", "바닐라",
        "시원한", "부드러운", "고급",
        "차가운",
        "강한카페인", "잠깨는",
        "여름", "시원", "특별한", "프리미엄"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "크림", "바닐라",
        "시원한", "차가운", "아이스",
        "부드러운", "크리미", "고급스러운",
        "특별한", "프리미엄", "시그니처",
        "강한카페인", "잠깨는", "졸릴때",
        "여름", "더울때", "시원한거",
        "인기", "베스트", "유명한"
      ],
      "synonyms": [
        "바닐라 크림 콜드 브루", "바닐라크림콜드브루",
        "바크콜", "바닐라콜브", "크림콜브",
        "vanilla cream cold brew", "Vanilla Cold Brew",
        "바닐라콜드브루", "바닐라브루"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "CB004",
      "name": "오트 콜드 브루",
      "category": "콜드브루",
      "description": "고소한 오트 밀크와 콜드 브루의 만남. 비건 옵션으로 건강하고 고소한 맛입니다.",
      "base_price": 5800,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5800,
        "Large": 6300,
        "Extra Large": 7300
      },
      "caffeine": {
        "level": "고",
        "amount": "200mg (Regular 기준)"
      },
      "calories": {
        "regular": 120,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["귀리"],
      "temperature": ["ICED"],
      "tags": [
        "고소한", "오트밀크", "비건",
        "시원한", "부드러운", "건강한",
        "차가운",
        "강한카페인", "잠깨는",
        "여름", "시원", "특별한", "트렌디"
      ],
      "recommendation_keywords": [
        "고소한", "오트", "오트밀크", "귀리",
        "비건", "식물성", "락토프리",
        "우유안됨", "우유알러지", "우유대체",
        "시원한", "차가운", "아이스",
        "건강한", "헬시", "다이어트",
        "강한카페인", "잠깨는", "졸릴때",
        "여름", "더울때", "시원한거",
        "특별한", "트렌디", "요즘"
      ],
      "synonyms": [
        "오트 콜드 브루", "오트콜드브루",
        "오트콜브", "오트브루", "귀리콜브",
        "oat cold brew", "Oat Cold Brew",
        "오트밀크콜드브루", "오트밀크브루"
      ],
      "search_boost_score": 1.1
    }
  ]
}

# ==================프라푸치노 & 블렌디드==================
{
  "menus": [
    {
      "menu_id": "F001",
      "name": "자바 칩 프라푸치노",
      "category": "프라푸치노",
      "description": "초콜릿 칩과 모카의 달콤한 블렌디드 음료. 씹는 재미가 있는 인기 메뉴입니다.",
      "base_price": 6300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6300,
        "Large": 6800,
        "Extra Large": 7800
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 440,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "대두"],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "초콜릿", "칩", "씹히는",
        "시원한", "블렌디드", "디저트같은",
        "차가운",
        "인기", "베스트", "시그니처",
        "여름", "오후", "간식", "디저트"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "초콜릿",
        "초코", "칩", "씹히는", "씹는맛",
        "시원한", "차가운", "블렌디드",
        "디저트", "디저트같은", "간식",
        "달거좋아", "초콜릿좋아",
        "인기", "베스트", "유명한", "시그니처",
        "여름", "더울때", "시원한거",
        "오후", "티타임", "간식시간"
      ],
      "synonyms": [
        "자바 칩 프라푸치노", "자바칩프라푸치노",
        "자바칩", "자칩", "자프",
        "java chip frappuccino", "Java Chip",
        "초코칩프라푸치노", "초코칩프라페"
      ],
      "search_boost_score": 1.5
    },
    {
      "menu_id": "F002",
      "name": "카라멜 프라푸치노",
      "category": "프라푸치노",
      "description": "카라멜의 달콤함이 가득한 프라푸치노. 부드러운 크림과 카라멜 드리즐이 특징입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 6400,
        "Extra Large": 7400
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 400,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "카라멜", "크림",
        "시원한", "블렌디드", "부드러운",
        "차가운",
        "인기", "베스트",
        "여름", "오후", "간식", "디저트"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "카라멜",
        "시원한", "차가운", "블렌디드",
        "부드러운", "크리미", "크림",
        "디저트", "디저트같은", "간식",
        "달거좋아", "카라멜좋아",
        "인기", "베스트", "유명한",
        "여름", "더울때", "시원한거",
        "오후", "티타임"
      ],
      "synonyms": [
        "카라멜 프라푸치노", "카라멜프라푸치노",
        "카프", "카라프", "카라멜프라페",
        "caramel frappuccino", "Caramel Frappuccino",
        "캬라멜프라푸치노"
      ],
      "search_boost_score": 1.4
    },
    {
      "menu_id": "F003",
      "name": "제주 말차 크림 프라푸치노",
      "category": "프라푸치노",
      "description": "제주 말차와 생크림의 프리미엄 블렌디드. 고급스러운 말차 향과 부드러운 크림이 조화롭습니다.",
      "base_price": 6300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6300,
        "Large": 6800,
        "Extra Large": 7800
      },
      "caffeine": {
        "level": "저",
        "amount": "30mg (Regular 기준)"
      },
      "calories": {
        "regular": 380,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "말차", "녹차", "크림", "고급",
        "시원한", "블렌디드", "부드러운",
        "차가운",
        "특별한", "프리미엄", "제주",
        "여름", "오후", "간식", "인기"
      ],
      "recommendation_keywords": [
        "말차", "녹차", "그린티", "제주",
        "고소한", "은은한", "부드러운",
        "크림", "크리미", "고급스러운",
        "시원한", "차가운", "블렌디드",
        "특별한", "프리미엄", "시그니처",
        "저카페인", "카페인적은", "카페인낮은",
        "여름", "더울때", "시원한거",
        "오후", "티타임", "여성인기"
      ],
      "synonyms": [
        "제주 말차 크림 프라푸치노", "제주말차크림프라푸치노",
        "말차프라푸치노", "말차프라페", "말프",
        "녹차프라푸치노", "녹차프라페",
        "matcha frappuccino", "Green Tea Frappuccino",
        "제주말차", "말차크림"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "F004",
      "name": "초콜릿 크림 칩 프라푸치노",
      "category": "프라푸치노",
      "description": "초콜릿 칩과 휘핑크림의 달콤한 조합. 진한 초콜릿 맛이 특징입니다.",
      "base_price": 6000,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6000,
        "Large": 6500,
        "Extra Large": 7500
      },
      "caffeine": {
        "level": "중",
        "amount": "75mg (Regular 기준)"
      },
      "calories": {
        "regular": 420,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "대두"],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "초콜릿", "칩", "크림",
        "시원한", "블렌디드", "디저트같은",
        "차가운",
        "인기", "여름", "오후", "간식"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "초콜릿",
        "초코", "칩", "씹히는", "크림",
        "시원한", "차가운", "블렌디드",
        "디저트", "디저트같은", "간식",
        "달거좋아", "초콜릿좋아",
        "여름", "더울때", "시원한거",
        "오후", "티타임"
      ],
      "synonyms": [
        "초콜릿 크림 칩 프라푸치노", "초콜릿크림칩프라푸치노",
        "초코칩프라푸치노", "초코칩", "초크프",
        "chocolate chip frappuccino", "Choco Chip",
        "초코크림칩", "초콜릿칩프라페"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "F005",
      "name": "더블 에스프레소 칩 프라푸치노",
      "category": "프라푸치노",
      "description": "진한 에스프레소 샷이 2배, 초콜릿 칩이 더해진 음료. 강한 커피 맛과 달콤함의 조화입니다.",
      "base_price": 6300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6300,
        "Large": 6800,
        "Extra Large": 7800
      },
      "caffeine": {
        "level": "고",
        "amount": "150mg (Regular 기준)"
      },
      "calories": {
        "regular": 400,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "대두"],
      "temperature": ["ICED"],
      "tags": [
        "진한", "강한", "에스프레소", "초콜릿",
        "달콤한", "칩", "씹히는",
        "시원한", "블렌디드",
        "차가운",
        "강한카페인", "잠깨는", "각성",
        "여름", "오후", "인기"
      ],
      "recommendation_keywords": [
        "진한", "진한커피", "강한", "에스프레소",
        "달콤한", "초콜릿", "칩", "씹히는",
        "시원한", "차가운", "블렌디드",
        "강한카페인", "카페인많은", "잠깨는",
        "졸릴때", "각성", "집중", "공부",
        "달면서진한", "달달하면서각성",
        "여름", "더울때", "시원한거",
        "오후", "야근", "공부"
      ],
      "synonyms": [
        "더블 에스프레소 칩 프라푸치노", "더블에스프레소칩프라푸치노",
        "더에칩", "더블에칩", "더블샷프라푸치노",
        "double espresso chip frappuccino", "Double Shot",
        "더블에스프레소", "2샷프라푸치노"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "F006",
      "name": "에스프레소 프라푸치노",
      "category": "프라푸치노",
      "description": "에스프레소의 진한 맛을 시원하게 즐기는 블렌디드. 달지 않고 커피 본연의 맛이 강합니다.",
      "base_price": 5500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5500,
        "Large": 6000,
        "Extra Large": 7000
      },
      "caffeine": {
        "level": "고",
        "amount": "150mg (Regular 기준)"
      },
      "calories": {
        "regular": 230,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "진한", "강한", "에스프레소", "쓴맛",
        "시원한", "블렌디드", "저칼로리",
        "차가운",
        "강한카페인", "잠깨는", "각성",
        "여름", "오후", "심플"
      ],
      "recommendation_keywords": [
        "진한", "진한커피", "강한", "에스프레소",
        "쓴", "쌉싸름한", "쓴맛", "안단",
        "달지않은", "안달은", "쓴거",
        "시원한", "차가운", "블렌디드",
        "저칼로리", "다이어트", "칼로리낮은",
        "강한카페인", "잠깨는", "졸릴때",
        "각성", "집중", "공부",
        "여름", "더울때", "시원한커피",
        "심플", "기본", "순수"
      ],
      "synonyms": [
        "에스프레소 프라푸치노", "에스프레소프라푸치노",
        "에프", "에스프라푸치노", "에스프라페",
        "espresso frappuccino", "Espresso Frappuccino",
        "샷프라푸치노"
      ],
      "search_boost_score": 1.0
    },
    {
      "menu_id": "B001",
      "name": "자몽 망고 코코 프라푸치노",
      "category": "블렌디드",
      "description": "자몽과 망고의 트로피컬 과일 블렌디드. 상큼하고 달콤한 과일 맛이 특징입니다.",
      "base_price": 7100,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 7100,
        "Large": 7600,
        "Extra Large": 8600
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 350,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["코코넛"],
      "temperature": ["ICED"],
      "tags": [
        "상큼한", "달콤한", "과일", "자몽", "망고",
        "열대", "트로피컬", "코코넛",
        "시원한", "블렌디드",
        "차가운",
        "카페인없음", "디카페인",
        "여름", "특별한", "프리미엄"
      ],
      "recommendation_keywords": [
        "상큼한", "새콤한", "달콤한", "과일",
        "자몽", "망고", "열대", "트로피컬",
        "코코넛", "과일음료", "과일맛",
        "시원한", "차가운", "블렌디드",
        "카페인없음", "카페인프리", "디카페인",
        "커피안마시는", "커피싫어", "논커피",
        "여름", "더울때", "시원한거",
        "특별한", "프리미엄", "고급",
        "오후", "티타임", "여성인기"
      ],
      "synonyms": [
        "자몽 망고 코코 프라푸치노", "자몽망고코코프라푸치노",
        "자망코", "자몽망고", "망고자몽",
        "grapefruit mango coco", "Tropical Frappuccino",
        "자몽망고프라페", "열대과일"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "B002",
      "name": "망고 바나나 블렌디드",
      "category": "블렌디드",
      "description": "달콤한 망고와 바나나의 과일 스무디. 부드럽고 달콤한 맛이 특징입니다.",
      "base_price": 6600,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6600,
        "Large": 7100,
        "Extra Large": 8100
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 320,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["ICED"],
      "tags": [
        "달콤한", "과일", "망고", "바나나",
        "부드러운", "스무디",
        "시원한", "블렌디드",
        "차가운",
        "카페인없음", "디카페인",
        "여름", "간식", "건강"
      ],
      "recommendation_keywords": [
        "달콤한", "달달한", "단", "과일",
        "망고", "바나나", "과일음료", "과일맛",
        "부드러운", "스무디", "블렌디드",
        "시원한", "차가운",
        "카페인없음", "카페인프리", "디카페인",
        "커피안마시는", "커피싫어", "논커피",
        "건강한", "과일로만", "자연",
        "여름", "더울때", "시원한거",
        "간식", "오후", "디저트"
      ],
      "synonyms": [
        "망고 바나나 블렌디드", "망고바나나블렌디드",
        "망바", "망고바나나", "바나나망고",
        "mango banana blended", "Mango Banana",
        "망고바나나스무디", "과일스무디"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "B003",
      "name": "딸기 딜라이트 요거트 블렌디드",
      "category": "블렌디드",
      "description": "상큼한 딸기와 요거트의 건강한 블렌디드. 새콤달콤한 맛이 특징입니다.",
      "base_price": 6300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6300,
        "Large": 6800,
        "Extra Large": 7800
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 280,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["ICED"],
      "tags": [
        "상큼한", "달콤한", "새콤한", "딸기",
        "요거트", "건강한",
        "시원한", "블렌디드",
        "차가운",
        "카페인없음", "디카페인",
        "여름", "간식", "여성인기"
      ],
      "recommendation_keywords": [
        "상큼한", "새콤한", "달콤한", "딸기",
        "요거트", "요구르트", "유산균",
        "건강한", "헬시", "다이어트",
        "시원한", "차가운", "블렌디드",
        "카페인없음", "카페인프리", "디카페인",
        "커피안마시는", "커피싫어", "논커피",
        "여름", "더울때", "시원한거",
        "간식", "오후", "여성인기"
      ],
      "synonyms": [
        "딸기 딜라이트 요거트 블렌디드", "딸기딜라이트요거트블렌디드",
        "딸요", "딸기요거트", "딸기요구르트",
        "strawberry yogurt blended", "Strawberry Delight",
        "딸기블렌디드", "딸기스무디"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "B004",
      "name": "제주 팔삭 자몽 허니 블렌디드",
      "category": "블렌디드",
      "description": "제주 자몽과 꿀의 달콤상큼한 블렌디드. 자몽의 쌉싸름함과 꿀의 단맛이 조화롭습니다.",
      "base_price": 6500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6500,
        "Large": 7000,
        "Extra Large": 8000
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 250,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["ICED"],
      "tags": [
        "상큼한", "달콤한", "자몽", "꿀",
        "제주", "쌉싸름한", "허니",
        "시원한", "블렌디드",
        "차가운",
        "카페인없음", "디카페인",
        "여름", "건강", "특별한"
      ],
      "recommendation_keywords": [
        "상큼한", "새콤한", "달콤한", "자몽",
        "꿀", "허니", "제주", "제주자몽",
        "쌉싸름한", "씁쓸달콤", "달달쌉싸름",
        "시원한", "차가운", "블렌디드",
        "카페인없음", "카페인프리", "디카페인",
        "커피안마시는", "커피싫어", "논커피",
        "건강한", "비타민", "과일",
        "여름", "더울때", "시원한거",
        "특별한", "제주산", "프리미엄"
      ],
      "synonyms": [
        "제주 팔삭 자몽 허니 블렌디드", "제주팔삭자몽허니블렌디드",
        "자허블", "자몽허니", "자몽꿀",
        "grapefruit honey blended", "Jeju Grapefruit",
        "제주자몽", "자몽블렌디드", "팔삭자몽"
      ],
      "search_boost_score": 1.1
    }
  ]
}

# ==================Tea 차 메뉴==================
{
      "menu_id": "T001",
      "name": "제주 유기농 녹차",
      "category": "차",
      "description": "제주산 유기농 녹차로 만든 깔끔한 티. 은은한 녹차 향과 깔끔한 맛이 특징입니다.",
      "base_price": 5300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5300,
        "Large": 5800,
        "Extra Large": 6800
      },
      "caffeine": {
        "level": "저",
        "amount": "30mg (Regular 기준)"
      },
      "calories": {
        "regular": 0,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "깔끔한", "은은한", "녹차", "제주",
        "건강한", "유기농", "차",
        "뜨거운", "차가운",
        "저칼로리", "다이어트", "제로칼로리",
        "저카페인", "카페인적은",
        "오후", "식후", "목편한"
      ],
      "recommendation_keywords": [
        "깔끔한", "은은한", "부드러운", "녹차",
        "제주", "유기농", "건강한",
        "차", "티", "tea", "그린티",
        "저칼로리", "다이어트", "칼로리없는", "제로칼로리",
        "저카페인", "카페인적은", "카페인낮은",
        "커피대신", "목편한", "따뜻한",
        "입가심", "식후", "오후", "저녁",
        "건강", "웰빙", "디톡스"
      ],
      "synonyms": [
        "제주 유기농 녹차", "제주유기농녹차",
        "제주녹차", "녹차", "그린티",
        "유기농녹차", "제주차",
        "green tea", "Green Tea", "Jeju Green Tea",
        "녹차티"
      ],
      "search_boost_score": 1.0
    },
    {
      "menu_id": "T002",
      "name": "자몽 허니 블랙 티",
      "category": "차",
      "description": "상큼한 자몽과 달콤한 꿀이 어우러진 홍차. 새콤달콤한 맛이 특징입니다.",
      "base_price": 5700,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5700,
        "Large": 6200,
        "Extra Large": 7200
      },
      "caffeine": {
        "level": "중",
        "amount": "50mg (Regular 기준)"
      },
      "calories": {
        "regular": 120,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "상큼한", "달콤한", "자몽", "꿀",
        "홍차", "블랙티", "과일",
        "뜨거운", "차가운",
        "저칼로리", "중간카페인",
        "오후", "티타임", "여름", "겨울"
      ],
      "recommendation_keywords": [
        "상큼한", "새콤한", "달콤한", "자몽",
        "꿀", "허니", "과일", "과일차",
        "홍차", "블랙티", "차", "티",
        "저칼로리", "다이어트", "칼로리낮은",
        "중간카페인", "커피보다약한",
        "커피대신", "목편한", "입가심",
        "오후", "티타임", "식후", "여유",
        "사계절", "여름", "겨울", "인기"
      ],
      "synonyms": [
        "자몽 허니 블랙 티", "자몽허니블랙티",
        "자허블", "자몽홍차", "자몽티",
        "자몽꿀차", "허니자몽",
        "grapefruit honey black tea", "Grapefruit Tea",
        "자몽차", "자허블티"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "T003",
      "name": "유자 민트 티",
      "category": "차",
      "description": "새콤달콤한 유자와 청량한 민트의 조화. 상쾌하고 따뜻한 차입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 6400,
        "Extra Large": 7400
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 110,
        "note": "Regular 사이즈 기준"
      },
      "allergens": [],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "상큼한", "청량한", "유자", "민트",
        "새콤달콤", "상쾌한", "허브",
        "뜨거운", "차가운",
        "저칼로리", "카페인없음", "디카페인",
        "겨울", "감기", "목", "건강"
      ],
      "recommendation_keywords": [
        "상큼한", "새콤한", "달콤한", "유자",
        "민트", "청량한", "상쾌한", "시원한",
        "허브", "허브차", "과일차",
        "저칼로리", "다이어트", "칼로리낮은",
        "카페인없음", "카페인프리", "디카페인",
        "커피안마시는", "커피싫어", "논커피",
        "목편한", "목아플때", "감기", "목",
        "겨울", "따뜻한", "건강", "차",
        "입가심", "식후", "저녁"
      ],
      "synonyms": [
        "유자 민트 티", "유자민트티",
        "유민", "유자민트", "민트유자",
        "유자차", "민트차", "유자티",
        "yuzu mint tea", "Yuzu Mint Tea",
        "유자민트허브차"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "T004",
      "name": "얼 그레이 바닐라 티 라떼",
      "category": "차",
      "description": "베르가못 향의 얼 그레이와 바닐라 우유의 조화. 향긋하고 부드러운 티 라떼입니다.",
      "base_price": 6100,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6100,
        "Large": 6600,
        "Extra Large": 7600
      },
      "caffeine": {
        "level": "중",
        "amount": "40mg (Regular 기준)"
      },
      "calories": {
        "regular": 210,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "향긋한", "부드러운", "바닐라", "얼그레이",
        "홍차", "우유", "라떼",
        "뜨거운", "차가운",
        "중간카페인", "고급", "프리미엄",
        "오후", "티타임", "여유", "특별한"
      ],
      "recommendation_keywords": [
        "향긋한", "부드러운", "고소한", "얼그레이",
        "바닐라", "홍차", "티라떼", "밀크티",
        "우유", "라떼", "크리미",
        "중간카페인", "커피보다약한", "저카페인",
        "커피대신", "목편한", "차",
        "고급", "프리미엄", "특별한", "향",
        "오후", "티타임", "여유", "브런치",
        "영국", "전통", "클래식"
      ],
      "synonyms": [
        "얼 그레이 바닐라 티 라떼", "얼그레이바닐라티라떼",
        "얼그레이", "얼그레이라떼", "얼바티",
        "earl grey vanilla tea latte", "Earl Grey Latte",
        "얼그레이티", "바닐라티라떼", "밀크티"
      ],
      "search_boost_score": 1.0
    },
    {
      "menu_id": "T005",
      "name": "제주 말차 라떼",
      "category": "차",
      "description": "제주산 말차로 만든 진한 녹차 라떼. 고소하고 진한 말차 향이 특징입니다.",
      "base_price": 6100,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6100,
        "Large": 6600,
        "Extra Large": 7600
      },
      "caffeine": {
        "level": "저",
        "amount": "30mg (Regular 기준)"
      },
      "calories": {
        "regular": 230,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유"],
      "temperature": ["HOT", "ICED"],
      "tags": [
        "고소한", "진한", "말차", "녹차",
        "제주", "우유", "라떼",
        "뜨거운", "차가운",
        "저카페인", "건강한", "고급",
        "오후", "티타임", "특별한", "여성인기"
      ],
      "recommendation_keywords": [
        "고소한", "진한", "은은한", "말차",
        "녹차", "그린티", "제주", "제주말차",
        "우유", "라떼", "밀크티", "크리미",
        "저카페인", "카페인적은", "카페인낮은",
        "커피대신", "커피보다약한", "차",
        "건강한", "헬시", "웰빙", "항산화",
        "고급", "프리미엄", "특별한",
        "오후", "티타임", "브런치", "여유",
        "여성인기", "인스타", "예쁜"
      ],
      "synonyms": [
        "제주 말차 라떼", "제주말차라떼",
        "말차라떼", "말라", "말차",
        "녹차라떼", "그린티라떼", "제주말차",
        "matcha latte", "Matcha Latte", "Green Tea Latte",
        "말차우유", "녹차우유"
      ],
      "search_boost_score": 1.2
    }
  ]
}

# ==================샌드위치, 디저트==================
{
  "menus": [
    {
      "menu_id": "D001",
      "name": "바스크 초코 치즈 케이크",
      "category": "디저트",
      "description": "진한 초콜릿과 크림치즈의 풍부한 맛. 겉은 바삭하고 속은 부드러운 프리미엄 케이크입니다.",
      "base_price": 7300,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 7300,
        "Large": 7300,
        "Extra Large": 7300
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 420,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "계란", "밀"],
      "temperature": ["HOT"],
      "tags": [
        "진한", "초콜릿", "치즈케이크", "바스크",
        "부드러운", "달콤한", "고급", "프리미엄",
        "디저트", "케이크", "간식",
        "특별한", "시그니처", "인기"
      ],
      "recommendation_keywords": [
        "진한", "진한초콜릿", "초콜릿", "초코",
        "치즈", "치즈케이크", "크림치즈",
        "바스크", "바스크치즈케이크",
        "부드러운", "촉촉한", "부드러운케이크",
        "달콤한", "달달한", "디저트",
        "고급", "프리미엄", "특별한", "시그니처",
        "케이크", "간식", "디저트", "후식",
        "인기", "베스트", "유명한",
        "초콜릿좋아", "달거좋아", "케이크좋아"
      ],
      "synonyms": [
        "바스크 초코 치즈 케이크", "바스크초코치즈케이크",
        "바스크케이크", "바스크", "초코치즈케이크",
        "basque chocolate cheesecake", "Basque Cake",
        "바스크초코", "초코바스크", "바스크치즈"
      ],
      "search_boost_score": 1.3
    },
    {
      "menu_id": "D002",
      "name": "부드러운 흑임자 롤",
      "category": "디저트",
      "description": "고소한 흑임자 크림이 가득한 롤케이크. 부드럽고 고소한 맛이 특징입니다.",
      "base_price": 7500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 7500,
        "Large": 7500,
        "Extra Large": 7500
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 380,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "계란", "밀"],
      "temperature": ["HOT"],
      "tags": [
        "고소한", "부드러운", "흑임자", "롤케이크",
        "크림", "달콤한", "특별한",
        "디저트", "케이크", "간식",
        "프리미엄", "시그니처", "인기"
      ],
      "recommendation_keywords": [
        "고소한", "고소한맛", "고소달달", "흑임자",
        "부드러운", "촉촉한", "부드러운케이크",
        "롤케이크", "롤", "크림", "크림케이크",
        "달콤한", "달달한", "은은한",
        "특별한", "프리미엄", "고급", "시그니처",
        "케이크", "간식", "디저트", "후식",
        "인기", "베스트", "유명한",
        "견과류", "건강한", "고소한거좋아"
      ],
      "synonyms": [
        "부드러운 흑임자 롤", "부드러운흑임자롤",
        "흑임자롤", "흑임자", "흑임자케이크",
        "black sesame roll", "Black Sesame Roll Cake",
        "흑임자롤케이크", "롤케이크"
      ],
      "search_boost_score": 1.2
    },
    {
      "menu_id": "D003",
      "name": "클라우드 치즈 케이크",
      "category": "디저트",
      "description": "구름처럼 가벼운 식감의 치즈 케이크. 부드럽고 가벼운 맛이 특징입니다.",
      "base_price": 5500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5500,
        "Large": 5500,
        "Extra Large": 5500
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 290,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "계란", "밀"],
      "temperature": ["HOT"],
      "tags": [
        "부드러운", "가벼운", "치즈케이크", "클라우드",
        "촉촉한", "달콤한", "은은한",
        "디저트", "케이크", "간식",
        "저렴한", "가성비", "인기"
      ],
      "recommendation_keywords": [
        "부드러운", "가벼운", "폭신한", "구름같은",
        "치즈", "치즈케이크", "크림치즈",
        "촉촉한", "부드러운케이크",
        "달콤한", "달달한", "은은한", "순한",
        "가벼운디저트", "부담없는", "가볍게",
        "케이크", "간식", "디저트", "후식",
        "저렴한", "가성비", "합리적",
        "인기", "베스트", "많이찾는"
      ],
      "synonyms": [
        "클라우드 치즈 케이크", "클라우드치즈케이크",
        "클라우드케이크", "클라우드", "구름케이크",
        "cloud cheesecake", "Cloud Cheese Cake",
        "치즈케이크", "구름치즈"
      ],
      "search_boost_score": 1.1
    },
    {
      "menu_id": "D004",
      "name": "부드러운 생크림 카스텔라",
      "category": "디저트",
      "description": "촉촉하고 부드러운 생크림 카스텔라. 달콤하고 부드러운 맛이 특징입니다.",
      "base_price": 4500,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 4500,
        "Large": 4500,
        "Extra Large": 4500
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 320,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["우유", "계란", "밀"],
      "temperature": ["HOT"],
      "tags": [
        "부드러운", "촉촉한", "카스텔라", "생크림",
        "달콤한", "폭신한", "가벼운",
        "디저트", "간식", "케이크",
        "저렴한", "가성비", "간단한"
      ],
      "recommendation_keywords": [
        "부드러운", "촉촉한", "폭신한", "카스텔라",
        "생크림", "크림", "달콤한", "달달한",
        "가벼운", "부담없는", "간단한",
        "케이크", "간식", "디저트", "후식",
        "저렴한", "가성비", "합리적", "싼",
        "간편한", "간단히", "가볍게",
        "인기", "많이찾는", "베이직"
      ],
      "synonyms": [
        "부드러운 생크림 카스텔라", "부드러운생크림카스텔라",
        "카스텔라", "생크림카스텔라", "크림카스텔라",
        "castella", "Cream Castella",
        "까스테라", "카스테라", "생크림까스텔라"
      ],
      "search_boost_score": 1.0
    },
    {
      "menu_id": "DS001",
      "name": "바질 토마토 탕종 베이글 샌드",
      "category": "디저트",
      "description": "신선한 토마토와 바질의 건강한 베이글 샌드위치. 신선하고 상큼한 맛이 특징입니다.",
      "base_price": 5900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 5900,
        "Large": 5900,
        "Extra Large": 5900
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 350,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["밀", "우유"],
      "temperature": ["HOT"],
      "tags": [
        "신선한", "건강한", "토마토", "바질",
        "베이글", "샌드위치", "채소",
        "식사", "든든한", "브런치",
        "점심", "아침", "간편식사"
      ],
      "recommendation_keywords": [
        "식사", "배고픈", "든든한", "meal", "밥대신",
        "점심", "아침", "끼니", "브런치", "간편식사",
        "건강한", "샐러드", "채소", "야채", "헬시",
        "바질", "토마토", "베이글", "샌드위치",
        "신선한", "상큼한", "가벼운식사",
        "빵", "샌드", "간단히", "가볍게"
      ],
      "synonyms": [
        "바질 토마토 탕종 베이글 샌드", "바질토마토탕종베이글샌드",
        "바질샌드", "바질 샌드", "바질샌드위치", "바질 샌드위치",
        "토마토샌드", "토마토 샌드", "토마토샌드위치", "토마토 샌드위치",
        "베이글샌드", "베이글 샌드", "베이글샌드위치",
        "바질토마토", "토마토바질",
        "샌드", "샌드위치", "베이글",
        "탕종베이글", "탕종", "tangzhong"
      ],
      "search_boost_score": 1.2,
      "promotion": {
        "type": "combo",
        "description": "이 샌드위치 주문 시 아메리카노 Regular 500원 할인",
        "discount_amount": 500,
        "condition": "아메리카노(C001) Regular 사이즈와 동시 주문"
      }
    },
    {
      "menu_id": "DS002",
      "name": "치킨 & 머쉬룸 멜팅 치즈 샌드위치",
      "category": "디저트",
      "description": "치킨과 버섯, 녹는 치즈의 풍성한 샌드위치. 든든하고 고소한 맛이 특징입니다.",
      "base_price": 6900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 6900,
        "Large": 6900,
        "Extra Large": 6900
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 520,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["밀", "우유", "계란"],
      "temperature": ["HOT"],
      "tags": [
        "든든한", "풍성한", "치킨", "치즈",
        "버섯", "머쉬룸", "고소한",
        "샌드위치", "식사", "브런치",
        "점심", "아침", "배부른", "간편식사"
      ],
      "recommendation_keywords": [
        "식사", "배고픈", "든든한", "meal", "밥대신", "배부른",
        "점심", "아침", "끼니", "브런치", "간편식사",
        "치킨", "닭고기", "고기", "육류",
        "치즈", "녹는치즈", "멜팅치즈", "고소한",
        "버섯", "머쉬룸", "야채",
        "샌드위치", "샌드", "빵",
        "풍성한", "푸짐한", "많이든"
      ],
      "synonyms": [
        "치킨 & 머쉬룸 멜팅 치즈 샌드위치", "치킨머쉬룸멜팅치즈샌드위치",
        "치킨샌드", "치킨샌드위치", "치킨머쉬룸",
        "치즈샌드", "치즈샌드위치", "멜팅치즈샌드",
        "버섯샌드", "머쉬룸샌드", "치킨치즈",
        "chicken mushroom sandwich", "Chicken Sandwich",
        "샌드", "샌드위치"
      ],
      "search_boost_score": 1.3,
      "promotion": {
        "type": "combo",
        "description": "이 샌드위치 주문 시 아메리카노 Regular 500원 할인",
        "discount_amount": 500,
        "condition": "아메리카노(C001) Regular 사이즈와 동시 주문"
      }
    },
    {
      "menu_id": "DS003",
      "name": "베이컨 치즈 토스트",
      "category": "디저트",
      "description": "바삭한 베이컨과 치즈의 클래식 토스트. 간단하고 고소한 맛이 특징입니다.",
      "base_price": 4900,
      "price_note": "Regular 사이즈 기준",
      "size_prices": {
        "Regular": 4900,
        "Large": 4900,
        "Extra Large": 4900
      },
      "caffeine": {
        "level": "없음",
        "amount": "0mg"
      },
      "calories": {
        "regular": 380,
        "note": "Regular 사이즈 기준"
      },
      "allergens": ["밀", "우유", "돼지고기"],
      "temperature": ["HOT"],
      "tags": [
        "바삭한", "고소한", "베이컨", "치즈",
        "토스트", "간단한", "간편한",
        "식사", "브런치", "아침",
        "점심", "간편식사", "저렴한"
      ],
      "recommendation_keywords": [
        "식사", "배고픈", "간단한", "간편한", "밥대신",
        "아침", "브런치", "끼니", "간편식사",
        "베이컨", "고기", "육류", "돼지고기",
        "치즈", "고소한", "바삭한", "짭짤한",
        "토스트", "빵", "샌드",
        "저렴한", "가성비", "싼", "합리적",
        "빠른", "간단히", "가볍게"
      ],
      "synonyms": [
        "베이컨 치즈 토스트", "베이컨치즈토스트",
        "베이컨토스트", "베토", "베치토",
        "치즈토스트", "베이컨샌드", "베이컨빵",
        "bacon cheese toast", "Bacon Toast",
        "토스트", "샌드위치"
      ],
      "search_boost_score": 1.1,
      "promotion": {
        "type": "combo",
        "description": "이 토스트 주문 시 아메리카노 Regular 500원 할인",
        "discount_amount": 500,
        "condition": "아메리카노(C001) Regular 사이즈와 동시 주문"
      }
    }
  ]
}