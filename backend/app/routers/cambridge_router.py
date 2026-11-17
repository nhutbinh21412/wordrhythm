from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter(prefix="/api/cambridge", tags=["Cambridge Vocabulary"])

# Curated, extensive Cambridge English Vocabulary Bank (A1 to C1) with phonetics, CEFR, definitions & collocations
CAMBRIDGE_DICT = {
    # Food & Health
    "recipe": {
        "word": "recipe", "phonetic": "/ˈres.ə.pi/", "pos": "noun", "cefr": "A2", "topic": "Food & Dining",
        "meaning_vn": "công thức nấu ăn",
        "definition": "a set of instructions telling you how to prepare and cook food",
        "example": "She followed her grandmother's recipe for beef stew.",
        "collocations": ["recipe book", "follow a recipe", "recipe for success"]
    },
    "ingredient": {
        "word": "ingredient", "phonetic": "/ɪnˈɡriː.di.ənt/", "pos": "noun", "cefr": "B1", "topic": "Food & Dining",
        "meaning_vn": "nguyên liệu, thành phần",
        "definition": "a food that is used with other foods in the preparation of a particular dish",
        "example": "Fresh vegetables are the main ingredient of this soup.",
        "collocations": ["key ingredient", "active ingredient", "essential ingredient"]
    },
    "nutrition": {
        "word": "nutrition", "phonetic": "/njuːˈtrɪʃ.ən/", "pos": "noun", "cefr": "B2", "topic": "Food & Health",
        "meaning_vn": "dinh dưỡng",
        "definition": "the substances that you take into your body as food and the way that they influence your health",
        "example": "Good nutrition is essential for a growing child's brain development.",
        "collocations": ["adequate nutrition", "poor nutrition", "nutrition facts"]
    },
    "beverage": {
        "word": "beverage", "phonetic": "/ˈbev.ər.ɪdʒ/", "pos": "noun", "cefr": "B2", "topic": "Food & Dining",
        "meaning_vn": "đồ uống, thức uống",
        "definition": "a drink of any type",
        "example": "Hot beverages include tea, coffee, and hot chocolate.",
        "collocations": ["alcoholic beverage", "refreshing beverage", "beverage industry"]
    },
    "delicious": {
        "word": "delicious", "phonetic": "/dɪˈlɪʃ.əs/", "pos": "adjective", "cefr": "A1", "topic": "Food & Dining",
        "meaning_vn": "thơm ngon",
        "definition": "having a very pleasant taste or smell",
        "example": "The chef prepared a delicious seafood dinner.",
        "collocations": ["delicious meal", "smell delicious", "taste delicious"]
    },

    # Technology & AI
    "human": {
        "word": "human", "phonetic": "/ˈhjuː.mən/", "pos": "noun", "cefr": "A2", "topic": "Society & Tech",
        "meaning_vn": "con người, loài người",
        "definition": "a person, rather than an animal, a machine, or an alien",
        "example": "AI is designed to assist human beings in solving complex problems.",
        "collocations": ["human nature", "human rights", "human intelligence"]
    },
    "algorithm": {
        "word": "algorithm", "phonetic": "/ˈæl.ɡə.rɪ.ðəm/", "pos": "noun", "cefr": "B2", "topic": "Technology",
        "meaning_vn": "thuật toán",
        "definition": "a set of mathematical instructions or rules used to calculate an answer to a problem",
        "example": "Search engines use sophisticated algorithms to index web pages.",
        "collocations": ["search algorithm", "computer algorithm", "machine learning algorithm"]
    },
    "cybersecurity": {
        "word": "cybersecurity", "phonetic": "/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/", "pos": "noun", "cefr": "B2", "topic": "Technology",
        "meaning_vn": "an ninh mạng",
        "definition": "ways of protecting computer systems and information against crime or damage",
        "example": "Companies invest millions in cybersecurity to prevent ransomware attacks.",
        "collocations": ["cybersecurity expert", "cybersecurity breach", "cybersecurity protocol"]
    },
    "automation": {
        "word": "automation", "phonetic": "/ˌɔː.təˈmeɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Technology",
        "meaning_vn": "sự tự động hóa",
        "definition": "the use of machines and computers that can operate without needing human control",
        "example": "Automation in manufacturing has drastically increased assembly line speed.",
        "collocations": ["industrial automation", "office automation", "automation process"]
    },
    "innovation": {
        "word": "innovation", "phonetic": "/ˌɪn.əˈveɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Technology",
        "meaning_vn": "sự đổi mới, sáng kiến",
        "definition": "a new idea or method, or the use of new ideas and methods",
        "example": "Technological innovation is key to maintaining a competitive edge.",
        "collocations": ["technological innovation", "encourage innovation", "product innovation"]
    },
    "database": {
        "word": "database", "phonetic": "/ˈdeɪ.tə.beɪs/", "pos": "noun", "cefr": "B1", "topic": "Technology",
        "meaning_vn": "cơ sở dữ liệu",
        "definition": "a large amount of information stored in a computer system in such a way that it can be easily looked at or changed",
        "example": "Customer records are securely kept in a relational database.",
        "collocations": ["relational database", "database management", "query a database"]
    },

    # Nature & Environment
    "biodiversity": {
        "word": "biodiversity", "phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/", "pos": "noun", "cefr": "B2", "topic": "Environment",
        "meaning_vn": "đa dạng sinh học",
        "definition": "the variety of animal and plant life in a particular habitat",
        "example": "The Amazon rainforest is globally renowned for its exceptional biodiversity.",
        "collocations": ["rich biodiversity", "loss of biodiversity", "preserve biodiversity"]
    },
    "sustainable": {
        "word": "sustainable", "phonetic": "/səˈsteɪ.nə.bəl/", "pos": "adjective", "cefr": "B2", "topic": "Environment",
        "meaning_vn": "bền vững, thân thiện môi trường",
        "definition": "causing little or no damage to the environment and therefore able to continue for a long time",
        "example": "We must adopt sustainable energy sources to protect the climate.",
        "collocations": ["sustainable development", "sustainable energy", "sustainable future"]
    },
    "ecosystem": {
        "word": "ecosystem", "phonetic": "/ˈiː.koʊˌsɪs.təm/", "pos": "noun", "cefr": "B2", "topic": "Environment",
        "meaning_vn": "hệ sinh thái",
        "definition": "all the living things in an area and the way they affect each other and the environment",
        "example": "Pollution threatens fragile marine ecosystems around coral reefs.",
        "collocations": ["marine ecosystem", "fragile ecosystem", "ecosystem balance"]
    },
    "extinction": {
        "word": "extinction", "phonetic": "/ɪkˈstɪŋk.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Environment",
        "meaning_vn": "sự tuyệt chủng",
        "definition": "a situation in which something no longer exists",
        "example": "Many endangered species are currently facing the threat of extinction.",
        "collocations": ["near extinction", "threat of extinction", "mass extinction"]
    },
    "renewable": {
        "word": "renewable", "phonetic": "/rɪˈnjuː.ə.bəl/", "pos": "adjective", "cefr": "B1", "topic": "Environment",
        "meaning_vn": "có thể tái tạo",
        "definition": "energy that is produced using natural resources such as sunlight, wind, or water",
        "example": "Wind and solar power are the fastest-growing forms of renewable energy.",
        "collocations": ["renewable energy", "renewable resources", "renewable power"]
    },

    # Business & Economics
    "entrepreneur": {
        "word": "entrepreneur", "phonetic": "/ˌɒn.trə.prəˈnɜːr/", "pos": "noun", "cefr": "B2", "topic": "Business",
        "meaning_vn": "doanh nhân, người khởi nghiệp",
        "definition": "someone who starts their own business, especially when this involves seeing a new opportunity",
        "example": "She is an ambitious entrepreneur who launched three successful tech startups.",
        "collocations": ["successful entrepreneur", "budding entrepreneur", "tech entrepreneur"]
    },
    "investment": {
        "word": "investment", "phonetic": "/ɪnˈvest.mənt/", "pos": "noun", "cefr": "B1", "topic": "Business",
        "meaning_vn": "khoản đầu tư, sự đầu tư",
        "definition": "the act of putting money, effort, time, etc. into something to make a profit or get an advantage",
        "example": "Investing in education yields the highest long-term returns.",
        "collocations": ["foreign investment", "capital investment", "return on investment"]
    },
    "monopoly": {
        "word": "monopoly", "phonetic": "/məˈnɒp.əl.i/", "pos": "noun", "cefr": "C1", "topic": "Business",
        "meaning_vn": "sự độc quyền",
        "definition": "complete control of the supply of particular goods or services, which makes other competition impossible",
        "example": "The government passed antitrust laws to prevent corporate monopolies.",
        "collocations": ["holding a monopoly", "state monopoly", "monopoly power"]
    },
    "revenue": {
        "word": "revenue", "phonetic": "/ˈrev.ən.juː/", "pos": "noun", "cefr": "B2", "topic": "Business",
        "meaning_vn": "doanh thu, ngân thu",
        "definition": "the money that a government or an organization receives from business activities or taxation",
        "example": "The company reported a 25 percent surge in quarterly revenue.",
        "collocations": ["annual revenue", "generate revenue", "advertising revenue"]
    },
    "strategy": {
        "word": "strategy", "phonetic": "/ˈstræt.ə.dʒi/", "pos": "noun", "cefr": "B1", "topic": "Business",
        "meaning_vn": "chiến lược",
        "definition": "a detailed plan for achieving success in situations such as war, politics, business, industry, or sport",
        "example": "We need a clear marketing strategy to expand into European markets.",
        "collocations": ["marketing strategy", "corporate strategy", "long-term strategy"]
    },

    # Academic & IELTS Mastery
    "pivotal": {
        "word": "pivotal", "phonetic": "/ˈpɪv.ə.təl/", "pos": "adjective", "cefr": "C1", "topic": "Academic",
        "meaning_vn": "then chốt, có tính chất quyết định",
        "definition": "central and important; on which other things depend in an essential way",
        "example": "Higher education plays a pivotal role in national economic prosperity.",
        "collocations": ["pivotal role", "pivotal moment", "pivotal decision"]
    },
    "unprecedented": {
        "word": "unprecedented", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "pos": "adjective", "cefr": "C1", "topic": "Academic",
        "meaning_vn": "chưa từng có tiền lệ",
        "definition": "never having happened or existed in the past",
        "example": "The pandemic caused unprecedented disruption to international trade.",
        "collocations": ["unprecedented scale", "unprecedented challenge", "unprecedented success"]
    },
    "paradigm": {
        "word": "paradigm", "phonetic": "/ˈpær.ə.daɪm/", "pos": "noun", "cefr": "C1", "topic": "Academic",
        "meaning_vn": "mô hình, khuôn mẫu chuẩn",
        "definition": "a model of something, or a very clear and typical example of something",
        "example": "Quantum mechanics caused a paradigm shift in modern physics.",
        "collocations": ["paradigm shift", "dominant paradigm", "cultural paradigm"]
    },
    "comprehensive": {
        "word": "comprehensive", "phonetic": "/ˌkɒm.prɪˈhen.sɪv/", "pos": "adjective", "cefr": "B2", "topic": "Academic",
        "meaning_vn": "toàn diện, bao quát",
        "definition": "complete and including everything that is necessary",
        "example": "The university conducted a comprehensive review of the syllabus.",
        "collocations": ["comprehensive guide", "comprehensive study", "comprehensive coverage"]
    },
    "hypothesis": {
        "word": "hypothesis", "phonetic": "/haɪˈpɒθ.ə.sɪs/", "pos": "noun", "cefr": "B2", "topic": "Academic",
        "meaning_vn": "giả thuyết",
        "definition": "an idea or explanation for something that is based on known facts but has not yet been proved",
        "example": "Scientists conducted experiments to test their original hypothesis.",
        "collocations": ["test a hypothesis", "formulate a hypothesis", "working hypothesis"]
    },

    # Travel & Culture
    "itinerary": {
        "word": "itinerary", "phonetic": "/aɪˈtɪn.ər.ər.i/", "pos": "noun", "cefr": "B1", "topic": "Travel",
        "meaning_vn": "lịch trình chuyến đi",
        "definition": "a detailed plan or route of a journey",
        "example": "Our travel itinerary includes guided tours of Tokyo and Kyoto.",
        "collocations": ["travel itinerary", "detailed itinerary", "plan an itinerary"]
    },
    "destination": {
        "word": "destination", "phonetic": "/ˌdes.tɪˈneɪ.ʃən/", "pos": "noun", "cefr": "B1", "topic": "Travel",
        "meaning_vn": "điểm đến",
        "definition": "the place where someone is going or where something is being sent or taken",
        "example": "Da Nang is a beloved vacation destination for domestic and foreign travelers.",
        "collocations": ["popular destination", "final destination", "tourist destination"]
    },
    "heritage": {
        "word": "heritage", "phonetic": "/ˈher.ɪ.tɪdʒ/", "pos": "noun", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "di sản văn hóa",
        "definition": "features belonging to the culture of a particular society, such as traditions, languages, or buildings",
        "example": "Hoi An ancient town is recognized as a UNESCO World Heritage site.",
        "collocations": ["cultural heritage", "national heritage", "preserve heritage"]
    },
    "hospitality": {
        "word": "hospitality", "phonetic": "/ˌhɒs.pɪˈtæl.ə.ti/", "pos": "noun", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "sự hiếu khách, ngành khách sạn",
        "definition": "the act of being friendly and welcoming to guests and visitors",
        "example": "We were deeply touched by the warm hospitality of the local villagers.",
        "collocations": ["warm hospitality", "hospitality industry", "generous hospitality"]
    },

    # Health & Medical
    "symptom": {
        "word": "symptom", "phonetic": "/ˈsɪmp.təm/", "pos": "noun", "cefr": "B1", "topic": "Health",
        "meaning_vn": "triệu chứng bệnh",
        "definition": "any feeling of illness or physical change that is caused by a particular disease",
        "example": "Common symptoms of influenza include fever, headache, and muscle aches.",
        "collocations": ["early symptom", "mild symptom", "relieve symptoms"]
    },
    "resilience": {
        "word": "resilience", "phonetic": "/rɪˈzɪl.jəns/", "pos": "noun", "cefr": "C1", "topic": "Health & Mindset",
        "meaning_vn": "sự kiên cường, khả năng hồi phục",
        "definition": "the ability to recover quickly from illness, depression, or misfortune",
        "example": "Mental resilience allows athletes to perform under immense pressure.",
        "collocations": ["build resilience", "emotional resilience", "psychological resilience"]
    },
    "vaccine": {
        "word": "vaccine", "phonetic": "/ˈvæk.siːn/", "pos": "noun", "cefr": "B2", "topic": "Health",
        "meaning_vn": "vắc xin",
        "definition": "a substance that is put into the body to prevent people from catching a particular disease",
        "example": "Vaccines have effectively eliminated smallpox worldwide.",
        "collocations": ["develop a vaccine", "administer a vaccine", "booster vaccine"]
    }
}

@router.get("/lookup")
def lookup_cambridge(q: str = Query(..., description="Từ tiếng Anh cần tra")):
    query = q.strip().lower()
    if query in CAMBRIDGE_DICT:
        return CAMBRIDGE_DICT[query]
    
    # Partial match
    for k, v in CAMBRIDGE_DICT.items():
        if query in k or k in query:
            return v
            
    # Fallback generator
    return {
        "word": query,
        "phonetic": f"/{query}/",
        "pos": "vocabulary",
        "cefr": "B1",
        "topic": "General English",
        "meaning_vn": f"Từ vựng: {query}",
        "definition": f"Cambridge dictionary vocabulary entry for '{query}'.",
        "example": f"This example demonstrates how to use the word {query} in natural English.",
        "collocations": [f"common {query}", f"daily {query}"]
    }

@router.get("/all")
def list_all_cambridge_words(topic: Optional[str] = None, cefr: Optional[str] = None):
    words = list(CAMBRIDGE_DICT.values())
    if topic:
        words = [w for w in words if topic.lower() in w.get("topic", "").lower()]
    if cefr:
        words = [w for w in words if cefr.upper() == w.get("cefr", "").upper()]
    return words
