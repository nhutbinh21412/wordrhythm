from fastapi import APIRouter, Query
from typing import List, Optional

router = APIRouter(prefix="/api/cambridge", tags=["Cambridge Vocabulary"])

# Curated, extensive Cambridge English Vocabulary Bank (A1 to C1) with phonetics, CEFR, definitions & collocations
# 20 words per topic for 6 major themes (120 total words)
CAMBRIDGE_DICT = {
    # ==========================================
    # 1. FOOD & NUTRITION (20 WORDS)
    # ==========================================
    "recipe": {
        "word": "recipe", "phonetic": "/ˈres.ə.pi/", "pos": "noun", "cefr": "A2", "topic": "Food & Nutrition",
        "meaning_vn": "công thức nấu ăn",
        "definition": "a set of instructions telling you how to prepare and cook food",
        "example": "She followed her grandmother's recipe for beef stew.",
        "collocations": ["recipe book", "follow a recipe", "recipe for success"]
    },
    "ingredient": {
        "word": "ingredient", "phonetic": "/ɪnˈɡriː.di.ənt/", "pos": "noun", "cefr": "B1", "topic": "Food & Nutrition",
        "meaning_vn": "nguyên liệu, thành phần",
        "definition": "a food that is used with other foods in the preparation of a particular dish",
        "example": "Fresh vegetables are the main ingredient of this soup.",
        "collocations": ["key ingredient", "active ingredient", "essential ingredient"]
    },
    "nutrition": {
        "word": "nutrition", "phonetic": "/njuːˈtrɪʃ.ən/", "pos": "noun", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "dinh dưỡng",
        "definition": "the substances that you take into your body as food and the way that they influence your health",
        "example": "Good nutrition is essential for a growing child's brain development.",
        "collocations": ["adequate nutrition", "poor nutrition", "nutrition facts"]
    },
    "beverage": {
        "word": "beverage", "phonetic": "/ˈbev.ər.ɪdʒ/", "pos": "noun", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "đồ uống, thức uống",
        "definition": "a drink of any type",
        "example": "Hot beverages include tea, coffee, and hot chocolate.",
        "collocations": ["alcoholic beverage", "refreshing beverage", "beverage industry"]
    },
    "delicious": {
        "word": "delicious", "phonetic": "/dɪˈlɪʃ.əs/", "pos": "adjective", "cefr": "A1", "topic": "Food & Nutrition",
        "meaning_vn": "thơm ngon",
        "definition": "having a very pleasant taste or smell",
        "example": "The chef prepared a delicious seafood dinner.",
        "collocations": ["delicious meal", "smell delicious", "taste delicious"]
    },
    "cuisine": {
        "word": "cuisine", "phonetic": "/kwɪˈziːn/", "pos": "noun", "cefr": "B1", "topic": "Food & Nutrition",
        "meaning_vn": "ẩm thực, phong cách nấu ăn",
        "definition": "a style of cooking characteristic of a particular country or region",
        "example": "Vietnamese cuisine is world-famous for its balanced herbs and fresh pho broth.",
        "collocations": ["traditional cuisine", "local cuisine", "haute cuisine"]
    },
    "appetite": {
        "word": "appetite", "phonetic": "/ˈæp.ə.taɪt/", "pos": "noun", "cefr": "B1", "topic": "Food & Nutrition",
        "meaning_vn": "sự ngon miệng, cảm giác thèm ăn",
        "definition": "the feeling that you want to eat food",
        "example": "A brisk walk in the crisp morning air gave him a hearty appetite.",
        "collocations": ["spoil your appetite", "hearty appetite", "loss of appetite"]
    },
    "delicacy": {
        "word": "delicacy", "phonetic": "/ˈdel.ɪ.kə.si/", "pos": "noun", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "cao lương mỹ vị, món ăn đặc sản",
        "definition": "something especially rare or expensive that is good to eat",
        "example": "Smoked salmon and black truffles are regarded as expensive delicacies.",
        "collocations": ["local delicacy", "culinary delicacy", "rare delicacy"]
    },
    "gourmet": {
        "word": "gourmet", "phonetic": "/ˈɡʊə.meɪ/", "pos": "adjective", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "ngon miệng cao cấp, sành điệu",
        "definition": "producing or relating to high-quality food or cooking",
        "example": "The downtown district has several fine gourmet restaurants.",
        "collocations": ["gourmet meal", "gourmet chef", "gourmet food"]
    },
    "diet": {
        "word": "diet", "phonetic": "/ˈdaɪ.ət/", "pos": "noun", "cefr": "A2", "topic": "Food & Nutrition",
        "meaning_vn": "chế độ ăn uống",
        "definition": "the food and drink usually taken by a person or group",
        "example": "A healthy balanced diet contains plenty of fiber, fruits, and lean protein.",
        "collocations": ["balanced diet", "healthy diet", "go on a diet"]
    },
    "vegetarian": {
        "word": "vegetarian", "phonetic": "/ˌvedʒ.ɪˈteə.ri.ən/", "pos": "noun", "cefr": "A2", "topic": "Food & Nutrition",
        "meaning_vn": "người ăn chay",
        "definition": "a person who does not eat meat or fish",
        "example": "He decided to become a vegetarian for environmental and ethical reasons.",
        "collocations": ["strict vegetarian", "vegetarian food", "vegetarian diet"]
    },
    "carbohydrate": {
        "word": "carbohydrate", "phonetic": "/ˌkɑː.bəʊˈhaɪ.dreɪt/", "pos": "noun", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "tinh bột, carbohydrate",
        "definition": "substances like sugar and starch that provide your body with energy",
        "example": "Athletes consume carbohydrates before marathons to sustain their energy.",
        "collocations": ["complex carbohydrates", "low carbohydrate", "carbohydrate intake"]
    },
    "protein": {
        "word": "protein", "phonetic": "/ˈprəʊ.tiːn/", "pos": "noun", "cefr": "B1", "topic": "Food & Nutrition",
        "meaning_vn": "chất đạm, protein",
        "definition": "one of the many substances found in food such as meat, cheese, fish, or eggs, necessary for body growth",
        "example": "Eggs, chicken breast, and beans are rich sources of dietary protein.",
        "collocations": ["protein source", "high-protein diet", "lean protein"]
    },
    "digest": {
        "word": "digest", "phonetic": "/daɪˈdʒest/", "pos": "verb", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "tiêu hóa thức ăn",
        "definition": "to change food in your stomach into substances that your body can use",
        "example": "It takes several hours for the human stomach to digest red meat.",
        "collocations": ["easily digested", "digest food", "slow to digest"]
    },
    "flavor": {
        "word": "flavor", "phonetic": "/ˈfleɪ.vər/", "pos": "noun", "cefr": "A2", "topic": "Food & Nutrition",
        "meaning_vn": "hương vị",
        "definition": "the particular taste of a food or drink",
        "example": "Fresh mint imparts a subtle aromatic flavor to the iced tea.",
        "collocations": ["natural flavor", "distinctive flavor", "burst of flavor"]
    },
    "organic": {
        "word": "organic", "phonetic": "/ɔːˈɡæn.ɪk/", "pos": "adjective", "cefr": "B1", "topic": "Food & Nutrition",
        "meaning_vn": "hữu cơ, tự nhiên không hóa chất",
        "definition": "not using artificial chemicals in the growing of plants and animals for food",
        "example": "Our supermarket has expanded its aisle of organic fruits and vegetables.",
        "collocations": ["organic food", "organic farming", "organic vegetables"]
    },
    "hygiene": {
        "word": "hygiene", "phonetic": "/ˈhaɪ.dʒiːn/", "pos": "noun", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "vệ sinh, an toàn thực phẩm",
        "definition": "the practice of keeping yourself and things around you clean to prevent disease",
        "example": "Strict food hygiene regulations must be upheld in every professional kitchen.",
        "collocations": ["food hygiene", "personal hygiene", "hygiene standards"]
    },
    "vitamin": {
        "word": "vitamin", "phonetic": "/ˈvɪt.ə.mɪn/", "pos": "noun", "cefr": "A2", "topic": "Food & Nutrition",
        "meaning_vn": "vitamin, vi chất",
        "definition": "any of a group of natural substances that are necessary in small amounts for health",
        "example": "Citrus fruits like oranges and grapefruits provide abundant vitamin C.",
        "collocations": ["vitamin deficiency", "vitamin supplement", "rich in vitamins"]
    },
    "edible": {
        "word": "edible", "phonetic": "/ˈed.ə.bəl/", "pos": "adjective", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "có thể ăn được, không độc",
        "definition": "suitable or safe for humans to eat",
        "example": "Only certain species of wild mushrooms in this forest are edible.",
        "collocations": ["edible plants", "edible oils", "scarcely edible"]
    },
    "wholesome": {
        "word": "wholesome", "phonetic": "/ˈhəʊl.səm/", "pos": "adjective", "cefr": "C1", "topic": "Food & Nutrition",
        "meaning_vn": "lành mạnh, bổ dưỡng",
        "definition": "good for your health; fresh and containing no artificial ingredients",
        "example": "They prepare clean, wholesome meals using freshly harvested crops.",
        "collocations": ["wholesome food", "wholesome meal", "wholesome ingredients"]
    },
    "culinary": {
        "word": "culinary", "phonetic": "/ˈkʌl.ɪ.nər.i/", "pos": "adjective", "cefr": "B2", "topic": "Food & Nutrition",
        "meaning_vn": "thuộc về ẩm thực, nghệ thuật nấu ăn",
        "definition": "connected with cooking or kitchens",
        "example": "Paris is renowned as the culinary capital of the world.",
        "collocations": ["culinary skills", "culinary art", "culinary delight"]
    },

    # ==========================================
    # 2. TECHNOLOGY & AI (20 WORDS)
    # ==========================================
    "algorithm": {
        "word": "algorithm", "phonetic": "/ˈæl.ɡə.rɪ.ðəm/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "thuật toán",
        "definition": "a set of mathematical instructions or rules used to calculate an answer to a problem",
        "example": "Search engines use sophisticated algorithms to index web pages.",
        "collocations": ["search algorithm", "computer algorithm", "machine learning algorithm"]
    },
    "cybersecurity": {
        "word": "cybersecurity", "phonetic": "/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "an ninh mạng",
        "definition": "things done to protect a computer or system against unauthorized access or attack",
        "example": "Corporations invest billions annually in modern cybersecurity infrastructure.",
        "collocations": ["cybersecurity threat", "cybersecurity protocol", "cybersecurity expert"]
    },
    "automation": {
        "word": "automation", "phonetic": "/ˌɔː.təˈmeɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "sự tự động hóa",
        "definition": "the use of machines to do work that was previously done by people",
        "example": "Automation in car manufacturing has dramatically increased factory productivity.",
        "collocations": ["factory automation", "process automation", "workplace automation"]
    },
    "innovation": {
        "word": "innovation", "phonetic": "/ˌɪn.əˈveɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "sự đổi mới, sáng tạo",
        "definition": "the use of a new idea or method",
        "example": "Technological innovation has fundamentally changed the way people communicate.",
        "collocations": ["technological innovation", "encourage innovation", "continuous innovation"]
    },
    "database": {
        "word": "database", "phonetic": "/ˈdeɪ.tə.beɪs/", "pos": "noun", "cefr": "B1", "topic": "Technology & AI",
        "meaning_vn": "cơ sở dữ liệu",
        "definition": "an organized collection of data stored and accessed electronically",
        "example": "All customer account information is secured within a relational database.",
        "collocations": ["relational database", "database management", "query the database"]
    },
    "artificial": {
        "word": "artificial", "phonetic": "/ˌɑː.tɪˈfɪʃ.əl/", "pos": "adjective", "cefr": "B1", "topic": "Technology & AI",
        "meaning_vn": "nhân tạo",
        "definition": "made by people, often as a copy of something natural",
        "example": "Artificial neural networks mimic the synaptic structure of the human brain.",
        "collocations": ["artificial intelligence", "artificial light", "artificial limb"]
    },
    "software": {
        "word": "software", "phonetic": "/ˈsɒft.weər/", "pos": "noun", "cefr": "A2", "topic": "Technology & AI",
        "meaning_vn": "phần mềm",
        "definition": "the instructions that control what a computer does; computer programs",
        "example": "She specializes in developing open-source educational software.",
        "collocations": ["software development", "software engineer", "install software"]
    },
    "hardware": {
        "word": "hardware", "phonetic": "/ˈhɑːd.weər/", "pos": "noun", "cefr": "B1", "topic": "Technology & AI",
        "meaning_vn": "phần cứng máy tính",
        "definition": "the physical and electronic parts of a computer system",
        "example": "Modern gaming demands powerful graphics hardware and rapid cooling systems.",
        "collocations": ["computer hardware", "hardware component", "upgrade hardware"]
    },
    "interface": {
        "word": "interface", "phonetic": "/ˈɪn.tə.feɪs/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "giao diện người dùng",
        "definition": "a connection between two pieces of electronic equipment, or between a person and a computer",
        "example": "The application offers an intuitive graphical interface for effortless navigation.",
        "collocations": ["user interface", "graphical interface", "clean interface"]
    },
    "network": {
        "word": "network", "phonetic": "/ˈnet.wɜːk/", "pos": "noun", "cefr": "A2", "topic": "Technology & AI",
        "meaning_vn": "mạng máy tính, mạng lưới",
        "definition": "a system of connected computers and communication devices",
        "example": "Our office network is protected by high-speed firewalls and intrusion monitors.",
        "collocations": ["computer network", "wireless network", "secure network"]
    },
    "encryption": {
        "word": "encryption", "phonetic": "/ɪnˈkrɪp.ʃən/", "pos": "noun", "cefr": "C1", "topic": "Technology & AI",
        "meaning_vn": "mã hóa dữ liệu",
        "definition": "the process of converting information into a secret code to prevent unauthorized access",
        "example": "End-to-end encryption prevents third parties from eavesdropping on confidential chats.",
        "collocations": ["data encryption", "encryption key", "strong encryption"]
    },
    "processor": {
        "word": "processor", "phonetic": "/ˈprəʊ.ses.ər/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "bộ vi xử lý",
        "definition": "the part of a computer that handles and executes programs and instructions",
        "example": "The flagship smartphone is powered by a super-efficient eight-core processor.",
        "collocations": ["central processor", "processor speed", "fast processor"]
    },
    "virtual": {
        "word": "virtual", "phonetic": "/ˈvɜː.tʃu.əl/", "pos": "adjective", "cefr": "B1", "topic": "Technology & AI",
        "meaning_vn": "thực tế ảo, trên mạng",
        "definition": "created by computer technology and appearing to exist but not in physical reality",
        "example": "Students attended virtual classrooms during international travel restrictions.",
        "collocations": ["virtual reality", "virtual world", "virtual assistant"]
    },
    "simulation": {
        "word": "simulation", "phonetic": "/ˌsɪm.jəˈleɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Technology & AI",
        "meaning_vn": "mô phỏng kỹ thuật số",
        "definition": "a model of a real activity, situation, or system created by a computer",
        "example": "Pilots undergo hundreds of flight simulation training hours before commercial flying.",
        "collocations": ["computer simulation", "flight simulation", "simulation model"]
    },
    "intelligence": {
        "word": "intelligence", "phonetic": "/ɪnˈtel.ɪ.dʒəns/", "pos": "noun", "cefr": "B1", "topic": "Technology & AI",
        "meaning_vn": "trí tuệ, sự thông minh",
        "definition": "the ability to learn, understand, and make judgments or have opinions",
        "example": "Generative intelligence systems are capable of writing coherent analytical essays.",
        "collocations": ["artificial intelligence", "human intelligence", "high intelligence"]
    },
    "digital": {
        "word": "digital", "phonetic": "/ˈdɪdʒ.ɪ.təl/", "pos": "adjective", "cefr": "A2", "topic": "Technology & AI",
        "meaning_vn": "kỹ thuật số",
        "definition": "using computer technology, especially the internet and computerized signals",
        "example": "The ongoing digital transformation has revolutionized retail banking globally.",
        "collocations": ["digital transformation", "digital economy", "digital era"]
    },
    "bandwidth": {
        "word": "bandwidth", "phonetic": "/ˈbænd.wɪtθ/", "pos": "noun", "cefr": "C1", "topic": "Technology & AI",
        "meaning_vn": "băng thông mạng",
        "definition": "the rate at which information can be sent through an internet connection",
        "example": "Streaming 4K video requires substantial internet bandwidth and low latency.",
        "collocations": ["high bandwidth", "broadband bandwidth", "consume bandwidth"]
    },
    "protocol": {
        "word": "protocol", "phonetic": "/ˈprəʊ.tə.kɒl/", "pos": "noun", "cefr": "C1", "topic": "Technology & AI",
        "meaning_vn": "giao thức máy tính",
        "definition": "a set of rules that computers use to communicate with each other across a network",
        "example": "The HTTPS protocol ensures that web transactions remain private and tamper-proof.",
        "collocations": ["communication protocol", "standard protocol", "network protocol"]
    },
    "robot": {
        "word": "robot", "phonetic": "/ˈrəʊ.bɒt/", "pos": "noun", "cefr": "A2", "topic": "Technology & AI",
        "meaning_vn": "người máy, robot",
        "definition": "a machine controlled by a computer that can move and do work automatically",
        "example": "Robots perform delicate surgical operations with microscopic precision.",
        "collocations": ["industrial robot", "humanoid robot", "autonomous robot"]
    },
    "human": {
        "word": "human", "phonetic": "/ˈhjuː.mən/", "pos": "noun", "cefr": "A2", "topic": "Technology & AI",
        "meaning_vn": "con người, loài người",
        "definition": "a person, rather than an animal, a machine, or an alien",
        "example": "AI is designed to assist human beings in solving complex problems.",
        "collocations": ["human nature", "human rights", "human intelligence"]
    },

    # ==========================================
    # 3. NATURE & ENVIRONMENT (20 WORDS)
    # ==========================================
    "biodiversity": {
        "word": "biodiversity", "phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "sự đa dạng sinh học",
        "definition": "the number and types of plants and animals that exist in a particular area",
        "example": "The Amazon rainforest contains the richest terrestrial biodiversity on Earth.",
        "collocations": ["preserve biodiversity", "loss of biodiversity", "biodiversity hotspot"]
    },
    "sustainable": {
        "word": "sustainable", "phonetic": "/səˈsteɪ.nə.bəl/", "pos": "adjective", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "bền vững, thân thiện môi trường",
        "definition": "causing little or no damage to the environment and therefore able to continue for a long time",
        "example": "Cities must transition toward sustainable public transit and renewable energy.",
        "collocations": ["sustainable development", "sustainable energy", "sustainable agriculture"]
    },
    "ecosystem": {
        "word": "ecosystem", "phonetic": "/ˈiː.kəʊˌsɪs.təm/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "hệ sinh thái",
        "definition": "all the living things in an area and the way they affect each other and their environment",
        "example": "Pollution threatens the fragile marine ecosystem of coral reefs.",
        "collocations": ["fragile ecosystem", "marine ecosystem", "forest ecosystem"]
    },
    "extinction": {
        "word": "extinction", "phonetic": "/ɪkˈstɪŋk.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "sự tuyệt chủng",
        "definition": "a situation in which a plant, an animal, or a way of life stops existing",
        "example": "Overhunting drove the Tasmanian tiger to complete extinction in the 20th century.",
        "collocations": ["mass extinction", "threatened with extinction", "face extinction"]
    },
    "renewable": {
        "word": "renewable", "phonetic": "/rɪˈnjuː.ə.bəl/", "pos": "adjective", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "năng lượng tái tạo",
        "definition": "forms of energy produced from sources that do not use up natural resources",
        "example": "Wind and solar power are clean, abundant renewable energy resources.",
        "collocations": ["renewable energy", "renewable resource", "renewable electricity"]
    },
    "conservation": {
        "word": "conservation", "phonetic": "/ˌkɒn.səˈveɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "sự bảo tồn thiên nhiên",
        "definition": "the protection of plants and animals, natural areas, and interesting and important buildings",
        "example": "Wildlife conservation programs have helped revive the giant panda population.",
        "collocations": ["wildlife conservation", "environmental conservation", "conservation effort"]
    },
    "atmosphere": {
        "word": "atmosphere", "phonetic": "/ˈæt.məs.fɪər/", "pos": "noun", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "khí quyển",
        "definition": "the mixture of gases around the Earth or another planet",
        "example": "Carbon emissions trap excess solar heat in the upper atmosphere.",
        "collocations": ["Earth's atmosphere", "upper atmosphere", "pollute the atmosphere"]
    },
    "habitat": {
        "word": "habitat", "phonetic": "/ˈhæb.ɪ.tæt/", "pos": "noun", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "môi trường sống tự nhiên",
        "definition": "the natural environment in which an animal or plant normally lives or grows",
        "example": "Deforestation robs endangered orangutans of their natural rainforest habitat.",
        "collocations": ["natural habitat", "habitat destruction", "wildlife habitat"]
    },
    "climate": {
        "word": "climate", "phonetic": "/ˈklaɪ.mət/", "pos": "noun", "cefr": "A2", "topic": "Nature & Environment",
        "meaning_vn": "khí hậu",
        "definition": "the general weather conditions usually found in a particular place over a long period",
        "example": "Global climate change has caused unprecedented extreme weather events.",
        "collocations": ["climate change", "tropical climate", "climate action"]
    },
    "pollutant": {
        "word": "pollutant", "phonetic": "/pəˈluː.tənt/", "pos": "noun", "cefr": "C1", "topic": "Nature & Environment",
        "meaning_vn": "chất gây ô nhiễm",
        "definition": "a substance that pollutes something, especially water or the atmosphere",
        "example": "Automobile exhaust releases toxic air pollutants into congested city streets.",
        "collocations": ["air pollutant", "chemical pollutant", "eliminate pollutants"]
    },
    "wildlife": {
        "word": "wildlife", "phonetic": "/ˈwaɪld.laɪf/", "pos": "noun", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "động thực vật hoang dã",
        "definition": "animals and plants that grow independently of people, usually in natural conditions",
        "example": "The national park was established to protect endangered African wildlife.",
        "collocations": ["wildlife reserve", "protect wildlife", "local wildlife"]
    },
    "deforestation": {
        "word": "deforestation", "phonetic": "/diːˌfɒr.ɪˈsteɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "nạn chặt phá rừng",
        "definition": "the cutting down of trees in a large area, or the destruction of forests by people",
        "example": "Severe deforestation leads directly to soil erosion and loss of water retention.",
        "collocations": ["halt deforestation", "illegal deforestation", "rates of deforestation"]
    },
    "solar": {
        "word": "solar", "phonetic": "/ˈsəʊ.lər/", "pos": "adjective", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "thuộc mặt trời, năng lượng mặt trời",
        "definition": "relating to the sun, or using the energy of the sun",
        "example": "Rooftop solar panels convert abundant sunlight into domestic electricity.",
        "collocations": ["solar energy", "solar panel", "solar system"]
    },
    "ecology": {
        "word": "ecology", "phonetic": "/iˈkɒl.ə.dʒi/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "sinh thái học",
        "definition": "the relationship of living things to their environment and to each other",
        "example": "Industrial chemical waste has severely disrupted the local river ecology.",
        "collocations": ["river ecology", "human ecology", "study of ecology"]
    },
    "greenhouse": {
        "word": "greenhouse", "phonetic": "/ˈɡriːn.haʊs/", "pos": "noun", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "hiệu ứng nhà kính",
        "definition": "relating to the warming of the Earth caused by trapped gases",
        "example": "Methane and carbon dioxide are the most potent greenhouse gases.",
        "collocations": ["greenhouse gas", "greenhouse effect", "greenhouse emissions"]
    },
    "marine": {
        "word": "marine", "phonetic": "/məˈriːn/", "pos": "adjective", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "thuộc về biển, đại dương",
        "definition": "related to the sea or sea transport, or found in the sea",
        "example": "Plastic debris causes immense harm to whales, turtles, and marine life.",
        "collocations": ["marine life", "marine biology", "marine ecosystem"]
    },
    "vegetation": {
        "word": "vegetation", "phonetic": "/ˌvedʒ.ɪˈteɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "thảm thực vật",
        "definition": "plants in general, or plants that are found in a particular area",
        "example": "Dense tropical vegetation shields the rainforest floor from direct sunlight.",
        "collocations": ["lush vegetation", "dense vegetation", "natural vegetation"]
    },
    "footprint": {
        "word": "footprint", "phonetic": "/ˈfʊt.prɪnt/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "dấu chân sinh thái, lượng khí thải",
        "definition": "the amount of greenhouse gases produced by a particular human activity or person",
        "example": "Commuting by bicycle drastically reduces your personal carbon footprint.",
        "collocations": ["carbon footprint", "environmental footprint", "reduce footprint"]
    },
    "glacier": {
        "word": "glacier", "phonetic": "/ˈɡlæs.i.ər/", "pos": "noun", "cefr": "B2", "topic": "Nature & Environment",
        "meaning_vn": "sông băng, tảng băng trôi",
        "definition": "a large mass of ice that moves slowly down a valley",
        "example": "Rising temperatures cause alpine glaciers to retreat at an alarming pace.",
        "collocations": ["melting glacier", "alpine glacier", "retreat of glaciers"]
    },
    "organic": {
        "word": "organic", "phonetic": "/ɔːˈɡæn.ɪk/", "pos": "adjective", "cefr": "B1", "topic": "Nature & Environment",
        "meaning_vn": "hữu cơ, tự nhiên",
        "definition": "not using artificial chemicals in the growing of plants and animals",
        "example": "Organic compost enriches soil fertility without chemical fertilizers.",
        "collocations": ["organic matter", "organic farming", "organic compost"]
    },

    # ==========================================
    # 4. BUSINESS & ECONOMICS (20 WORDS)
    # ==========================================
    "entrepreneur": {
        "word": "entrepreneur", "phonetic": "/ˌɒn.trə.prəˈnɜːr/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "doanh nhân khởi nghiệp",
        "definition": "someone who starts their own business, especially when this involves risks",
        "example": "An ambitious entrepreneur founded a breakthrough green tech startup.",
        "collocations": ["successful entrepreneur", "aspiring entrepreneur", "tech entrepreneur"]
    },
    "investment": {
        "word": "investment", "phonetic": "/ɪnˈvest.mənt/", "pos": "noun", "cefr": "B1", "topic": "Business & Economics",
        "meaning_vn": "khoản đầu tư",
        "definition": "the act of putting money into something to make a profit or earn interest",
        "example": "Venture capitalists made a massive capital investment in renewable batteries.",
        "collocations": ["foreign investment", "capital investment", "return on investment"]
    },
    "monopoly": {
        "word": "monopoly", "phonetic": "/məˈnɒp.əl.i/", "pos": "noun", "cefr": "C1", "topic": "Business & Economics",
        "meaning_vn": "thế độc quyền kinh doanh",
        "definition": "an organization or company that has complete control of something, especially an industry",
        "example": "Antitrust regulators investigated the software giant for unfair monopoly practices.",
        "collocations": ["break up a monopoly", "virtual monopoly", "monopoly power"]
    },
    "revenue": {
        "word": "revenue", "phonetic": "/ˈrev.ən.juː/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "doanh thu",
        "definition": "the money that an organization receives from its business operations",
        "example": "Company annual revenue soared by thirty percent thanks to mobile subscriptions.",
        "collocations": ["total revenue", "annual revenue", "generate revenue"]
    },
    "strategy": {
        "word": "strategy", "phonetic": "/ˈstræt.ə.dʒi/", "pos": "noun", "cefr": "B1", "topic": "Business & Economics",
        "meaning_vn": "chiến lược kinh doanh",
        "definition": "a detailed plan for achieving success in situations such as business or politics",
        "example": "Their expansion strategy centers on entering dynamic Southeast Asian markets.",
        "collocations": ["business strategy", "marketing strategy", "long-term strategy"]
    },
    "marketing": {
        "word": "marketing", "phonetic": "/ˈmɑː.kɪ.tɪŋ/", "pos": "noun", "cefr": "B1", "topic": "Business & Economics",
        "meaning_vn": "tiếp thị, marketing",
        "definition": "a job that involves encouraging people to buy a product or service",
        "example": "Digital marketing campaigns target specific consumer demographics effectively.",
        "collocations": ["marketing campaign", "marketing strategy", "digital marketing"]
    },
    "shareholder": {
        "word": "shareholder", "phonetic": "/ˈʃeəˌhəʊl.dər/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "cổ đông",
        "definition": "a person who owns shares in a company and therefore gets part of the company's profits",
        "example": "Shareholders gathered at the headquarters for the annual general meeting.",
        "collocations": ["majority shareholder", "shareholder meeting", "protect shareholders"]
    },
    "dividend": {
        "word": "dividend", "phonetic": "/ˈdɪv.ɪ.dend/", "pos": "noun", "cefr": "C1", "topic": "Business & Economics",
        "meaning_vn": "cổ tức chi trả",
        "definition": "a part of the profits of a company for a particular period, paid to the shareholders",
        "example": "The board declared an attractive cash dividend of fifty cents per share.",
        "collocations": ["pay a dividend", "cash dividend", "quarterly dividend"]
    },
    "asset": {
        "word": "asset", "phonetic": "/ˈæs.et/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "tài sản",
        "definition": "a useful or valuable quality, skill, or person; or something with economic value",
        "example": "Real estate, intellectual property, and gold are valuable corporate assets.",
        "collocations": ["liquid assets", "tangible assets", "valuable asset"]
    },
    "liability": {
        "word": "liability", "phonetic": "/ˌlaɪ.əˈbɪl.ə.ti/", "pos": "noun", "cefr": "C1", "topic": "Business & Economics",
        "meaning_vn": "khoản nợ phải trả, nghĩa vụ tài chính",
        "definition": "debts or financial obligations that a person or company owes",
        "example": "The firm balanced its total assets against outstanding short-term liabilities.",
        "collocations": ["financial liability", "total liabilities", "limited liability"]
    },
    "inflation": {
        "word": "inflation", "phonetic": "/ɪnˈfleɪ.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "lạm phát",
        "definition": "a continuous increase in the price of goods and services, resulting in decreased currency purchasing power",
        "example": "Central banks raised interest rates to rein in runaway inflation.",
        "collocations": ["high inflation", "rate of inflation", "curb inflation"]
    },
    "corporate": {
        "word": "corporate", "phonetic": "/ˈkɔː.pər.ət/", "pos": "adjective", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "thuộc tập đoàn, doanh nghiệp",
        "definition": "relating to a large company or group of companies",
        "example": "They established a corporate culture prioritizing transparency and employee wellness.",
        "collocations": ["corporate culture", "corporate governance", "corporate finance"]
    },
    "bankruptcy": {
        "word": "bankruptcy", "phonetic": "/ˈbæŋ.krəpt.si/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "sự phá sản",
        "definition": "a situation in which a business or person cannot pay what they owe",
        "example": "The retail chain filed for bankruptcy protection following months of falling sales.",
        "collocations": ["file for bankruptcy", "declare bankruptcy", "near bankruptcy"]
    },
    "negotiate": {
        "word": "negotiate", "phonetic": "/nəˈɡəʊ.ʃi.eɪt/", "pos": "verb", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "đàm phán, thương lượng",
        "definition": "to have formal discussions with someone in order to reach an agreement",
        "example": "Union delegates met with management to negotiate higher annual bonuses.",
        "collocations": ["negotiate a deal", "negotiate terms", "successfully negotiate"]
    },
    "profit": {
        "word": "profit", "phonetic": "/ˈprɒf.ɪt/", "pos": "noun", "cefr": "A2", "topic": "Business & Economics",
        "meaning_vn": "lợi nhuận",
        "definition": "money that is earned in trade or business after paying the costs of producing and selling",
        "example": "Online sales generated exceptional net profits during the holiday shopping season.",
        "collocations": ["net profit", "make a profit", "profit margin"]
    },
    "budget": {
        "word": "budget", "phonetic": "/ˈbʌdʒ.ɪt/", "pos": "noun", "cefr": "B1", "topic": "Business & Economics",
        "meaning_vn": "ngân sách",
        "definition": "the amount of money you have available to spend, or a plan of how to spend it",
        "example": "The research and development department exceeded its allocated quarterly budget.",
        "collocations": ["annual budget", "tight budget", "within budget"]
    },
    "venture": {
        "word": "venture", "phonetic": "/ˈven.tʃər/", "pos": "noun", "cefr": "B2", "topic": "Business & Economics",
        "meaning_vn": "dự án kinh doanh mạo hiểm",
        "definition": "a new activity, usually in business, that involves risk or uncertainty",
        "example": "The joint business venture between the two airlines yielded strong market dominance.",
        "collocations": ["business venture", "venture capital", "commercial venture"]
    },
    "capital": {
        "word": "capital", "phonetic": "/ˈkæp.ɪ.təl/", "pos": "noun", "cefr": "B1", "topic": "Business & Economics",
        "meaning_vn": "nguồn vốn kinh doanh",
        "definition": "money and possessions, especially a large amount of money used to produce more wealth",
        "example": "Startups need substantial initial capital to manufacture early product prototypes.",
        "collocations": ["raise capital", "venture capital", "working capital"]
    },
    "commodity": {
        "word": "commodity", "phonetic": "/kəˈmɒd.ə.ti/", "pos": "noun", "cefr": "C1", "topic": "Business & Economics",
        "meaning_vn": "hàng hóa thương phẩm",
        "definition": "a substance or product that can be traded, bought, or sold, such as oil, grain, or metal",
        "example": "Crude oil and natural gas remain highly volatile global commodities.",
        "collocations": ["commodity market", "basic commodity", "trade commodities"]
    },
    "fiscal": {
        "word": "fiscal", "phonetic": "/ˈfɪs.kəl/", "pos": "adjective", "cefr": "C1", "topic": "Business & Economics",
        "meaning_vn": "thuộc tài khóa, tài chính công",
        "definition": "connected with (public) money, taxes, debts, or government finance",
        "example": "The government introduced prudent fiscal stimulus measures to boost domestic growth.",
        "collocations": ["fiscal policy", "fiscal year", "fiscal deficit"]
    },

    # ==========================================
    # 5. TRAVEL & CULTURE (20 WORDS)
    # ==========================================
    "itinerary": {
        "word": "itinerary", "phonetic": "/aɪˈtɪn.ər.ər.i/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "lịch trình chuyến đi",
        "definition": "a detailed plan or route of a journey",
        "example": "Our travel itinerary includes guided tours of Tokyo and Kyoto.",
        "collocations": ["travel itinerary", "detailed itinerary", "plan an itinerary"]
    },
    "destination": {
        "word": "destination", "phonetic": "/ˌdes.tɪˈneɪ.ʃən/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
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
    "voyage": {
        "word": "voyage", "phonetic": "/ˈvɔɪ.ɪdʒ/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "chuyến hải trình, du hành xa",
        "definition": "a long journey, especially by ship or in space",
        "example": "The historic sea voyage across the Pacific Ocean took almost three weeks.",
        "collocations": ["maiden voyage", "long voyage", "embark on a voyage"]
    },
    "landmark": {
        "word": "landmark", "phonetic": "/ˈlænd.mɑːk/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "thắng cảnh, địa danh nổi tiếng",
        "definition": "a building or feature of a landscape that is easily recognized and helps you know where you are",
        "example": "The Eiffel Tower is the most celebrated architectural landmark in Paris.",
        "collocations": ["famous landmark", "historic landmark", "prominent landmark"]
    },
    "excursion": {
        "word": "excursion", "phonetic": "/ɪkˈskɜː.ʃən/", "pos": "noun", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "chuyến tham quan dã ngoại",
        "definition": "a short journey usually made for pleasure, often by a group of people",
        "example": "We booked a day excursion to explore the limestone caves of Ha Long Bay.",
        "collocations": ["day excursion", "go on an excursion", "boat excursion"]
    },
    "expedition": {
        "word": "expedition", "phonetic": "/ˌek.spəˈdɪʃ.ən/", "pos": "noun", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "cuộc thám hiểm",
        "definition": "an organized journey for a particular purpose, especially to discover new places or scientific facts",
        "example": "Scientists led a scientific expedition to the polar ice caps to collect ice core samples.",
        "collocations": ["scientific expedition", "mountaineering expedition", "lead an expedition"]
    },
    "foreign": {
        "word": "foreign", "phonetic": "/ˈfɒr.ən/", "pos": "adjective", "cefr": "A2", "topic": "Travel & Culture",
        "meaning_vn": "thuộc về nước ngoài",
        "definition": "belonging or connected to a country that is not your own",
        "example": "Traveling enables you to immerse yourself in foreign customs and languages.",
        "collocations": ["foreign country", "foreign language", "foreign tourist"]
    },
    "custom": {
        "word": "custom", "phonetic": "/ˈkʌs.təm/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "phong tục tập quán",
        "definition": "a way of behaving or a belief that has been established for a long time",
        "example": "It is customary to remove shoes before entering traditional Japanese homes.",
        "collocations": ["local custom", "ancient custom", "respect customs"]
    },
    "tradition": {
        "word": "tradition", "phonetic": "/trəˈdɪʃ.ən/", "pos": "noun", "cefr": "A2", "topic": "Travel & Culture",
        "meaning_vn": "truyền thống",
        "definition": "a belief, principle, or way of acting that people in a particular society have continued to follow",
        "example": "Lighting lantern fireworks is a cherished festive tradition during Tet holiday.",
        "collocations": ["long tradition", "cultural tradition", "family tradition"]
    },
    "passenger": {
        "word": "passenger", "phonetic": "/ˈpæs.ən.dʒər/", "pos": "noun", "cefr": "A2", "topic": "Travel & Culture",
        "meaning_vn": "hành khách",
        "definition": "a person who is traveling in a vehicle but is not driving it, flying it, or working on it",
        "example": "All flight passengers were requested to fasten their seatbelts before landing.",
        "collocations": ["airline passenger", "rail passenger", "passenger cabin"]
    },
    "accommodation": {
        "word": "accommodation", "phonetic": "/əˌkɒm.əˈdeɪ.ʃən/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "chỗ ở, nơi lưu trú",
        "definition": "a place to live, work, or stay in in return for payment",
        "example": "We booked clean beachfront hotel accommodation at reasonable rates.",
        "collocations": ["hotel accommodation", "book accommodation", "luxury accommodation"]
    },
    "folklore": {
        "word": "folklore", "phonetic": "/ˈfəʊk.lɔːr/", "pos": "noun", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "văn học dân gian, truyện dân gian",
        "definition": "the traditional beliefs, myths, and stories of a community passed through generations",
        "example": "Irish folklore is replete with enchanting tales of fairies and mythical heroes.",
        "collocations": ["local folklore", "traditional folklore", "ancient folklore"]
    },
    "monument": {
        "word": "monument", "phonetic": "/ˈmɒn.jə.mənt/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "đài tưởng niệm, công trình lịch sử",
        "definition": "a structure or statue erected to commemorate a famous person or historic event",
        "example": "Tourists marvel at the majestic marble monuments of ancient Rome.",
        "collocations": ["historic monument", "national monument", "erect a monument"]
    },
    "cruise": {
        "word": "cruise", "phonetic": "/kruːz/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "chuyến du thuyền",
        "definition": "a journey on a large ship for pleasure, during which you visit several places",
        "example": "They enjoyed an unforgettable sunset cruise around the Caribbean islands.",
        "collocations": ["luxury cruise", "cruise ship", "take a cruise"]
    },
    "passport": {
        "word": "passport", "phonetic": "/ˈpɑːs.pɔːt/", "pos": "noun", "cefr": "A1", "topic": "Travel & Culture",
        "meaning_vn": "hộ chiếu",
        "definition": "an official document containing personal details that you need to enter or leave a foreign country",
        "example": "Ensure that your biometric passport has at least six months of validity remaining.",
        "collocations": ["valid passport", "passport control", "renew a passport"]
    },
    "picturesque": {
        "word": "picturesque", "phonetic": "/ˌpɪk.tʃərˈesk/", "pos": "adjective", "cefr": "B2", "topic": "Travel & Culture",
        "meaning_vn": "đẹp như tranh vẽ",
        "definition": "attractive in appearance, especially in an old-fashioned or quaint way",
        "example": "The train traveled through picturesque mountain villages surrounded by pine forests.",
        "collocations": ["picturesque village", "picturesque scenery", "picturesque harbor"]
    },
    "souvenir": {
        "word": "souvenir", "phonetic": "/ˌsuː.vənˈɪər/", "pos": "noun", "cefr": "A2", "topic": "Travel & Culture",
        "meaning_vn": "quà lưu niệm",
        "definition": "something you buy or keep to remember a place, vacation, or special event",
        "example": "I purchased handmade silk scarves as souvenirs for my relatives.",
        "collocations": ["buy souvenirs", "souvenir shop", "keep as a souvenir"]
    },
    "architecture": {
        "word": "architecture", "phonetic": "/ˈɑː.kɪ.tek.tʃər/", "pos": "noun", "cefr": "B1", "topic": "Travel & Culture",
        "meaning_vn": "kiến trúc",
        "definition": "the art or practice of designing and constructing buildings",
        "example": "The Gothic architecture of the cathedral features soaring arches and stained glass.",
        "collocations": ["modern architecture", "classical architecture", "stunning architecture"]
    },

    # ==========================================
    # 6. ACADEMIC & IELTS MASTERY (20 WORDS)
    # ==========================================
    "pivotal": {
        "word": "pivotal", "phonetic": "/ˈpɪv.ə.təl/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "then chốt, có tính quyết định",
        "definition": "central and important; having a critical effect on the success of something",
        "example": "Technological advancements played a pivotal role in the Industrial Revolution.",
        "collocations": ["pivotal role", "pivotal moment", "pivotal factor"]
    },
    "unprecedented": {
        "word": "unprecedented", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "chưa từng có tiền lệ",
        "definition": "never having happened or existed in the past",
        "example": "The pandemic caused unprecedented disruption to global logistics and commerce.",
        "collocations": ["unprecedented scale", "unprecedented growth", "unprecedented challenge"]
    },
    "paradigm": {
        "word": "paradigm", "phonetic": "/ˈpær.ə.daɪm/", "pos": "noun", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "mô hình, khuôn mẫu tư duy",
        "definition": "a model of something, or a very clear or typical example showing how something should be done",
        "example": "Quantum mechanics caused a fundamental paradigm shift in modern theoretical physics.",
        "collocations": ["paradigm shift", "dominant paradigm", "new paradigm"]
    },
    "comprehensive": {
        "word": "comprehensive", "phonetic": "/ˌkɒm.prɪˈhen.sɪv/", "pos": "adjective", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "toàn diện, bao quát",
        "definition": "complete and including everything that is necessary",
        "example": "Scholars published a comprehensive review of renewable energy literature.",
        "collocations": ["comprehensive review", "comprehensive approach", "comprehensive analysis"]
    },
    "hypothesis": {
        "word": "hypothesis", "phonetic": "/haɪˈpɒθ.ə.sɪs/", "pos": "noun", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "giả thuyết khoa học",
        "definition": "an idea or explanation for something that is based on known facts but has not yet been proved",
        "example": "Researchers designed double-blind laboratory trials to test their hypothesis.",
        "collocations": ["test a hypothesis", "formulate a hypothesis", "working hypothesis"]
    },
    "empirical": {
        "word": "empirical", "phonetic": "/ɪmˈpɪr.ɪ.kəl/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "thực nghiệm, dựa trên bằng chứng",
        "definition": "based on what is experienced or seen rather than on theory",
        "example": "Scientific theories must be substantiated by rigorous empirical evidence.",
        "collocations": ["empirical evidence", "empirical study", "empirical data"]
    },
    "methodology": {
        "word": "methodology", "phonetic": "/ˌmeθ.əˈdɒl.ə.dʒi/", "pos": "noun", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "phương pháp luận nghiên cứu",
        "definition": "a system of ways of doing, teaching, or studying something",
        "example": "The dissertation outlined the qualitative methodology utilized to interview subjects.",
        "collocations": ["research methodology", "rigorous methodology", "robust methodology"]
    },
    "synthesis": {
        "word": "synthesis", "phonetic": "/ˈsɪn.θə.sɪs/", "pos": "noun", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "sự tổng hợp kiến thức",
        "definition": "the production of a substance from simpler materials after chemical reaction; or a combination of ideas",
        "example": "Her academic essay represents a brilliant synthesis of history and economics.",
        "collocations": ["synthesis of ideas", "protein synthesis", "literature synthesis"]
    },
    "cognitive": {
        "word": "cognitive", "phonetic": "/ˈkɒɡ.nə.tɪv/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "thuộc về nhận thức tư duy",
        "definition": "connected with thinking or conscious mental processes",
        "example": "Regular aerobic exercise enhances cognitive function and memory in elderly adults.",
        "collocations": ["cognitive ability", "cognitive development", "cognitive impairment"]
    },
    "abstract": {
        "word": "abstract", "phonetic": "/ˈæb.strækt/", "pos": "adjective", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "trừu tượng",
        "definition": "existing as an idea, feeling, or quality, not as a material object",
        "example": "Philosophers often ponder abstract concepts such as truth, justice, and virtue.",
        "collocations": ["abstract concept", "abstract idea", "abstract reasoning"]
    },
    "analyze": {
        "word": "analyze", "phonetic": "/ˈæn.əl.aɪz/", "pos": "verb", "cefr": "B1", "topic": "Academic & IELTS",
        "meaning_vn": "phân tích dữ liệu",
        "definition": "to study or examine something in detail, in order to discover more about it",
        "example": "Statisticians analyzed census data to identify demographic trends.",
        "collocations": ["analyze data", "carefully analyze", "analyze results"]
    },
    "deduction": {
        "word": "deduction", "phonetic": "/dɪˈdʌk.ʃən/", "pos": "noun", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "sự suy luận diễn dịch",
        "definition": "the process of reaching a decision or answer by thinking about the known facts",
        "example": "Through logical deduction, the detective deduced the suspect's real motive.",
        "collocations": ["logical deduction", "reasoning by deduction", "make a deduction"]
    },
    "qualitative": {
        "word": "qualitative", "phonetic": "/ˈkwɒl.ɪ.tə.tɪv/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "định tính",
        "definition": "relating to how good or bad something is; or using subjective descriptions rather than numbers",
        "example": "The sociologist conducted in-depth qualitative interviews with migrant workers.",
        "collocations": ["qualitative research", "qualitative analysis", "qualitative data"]
    },
    "quantitative": {
        "word": "quantitative", "phonetic": "/ˈkwɒn.tɪ.tə.tɪv/", "pos": "adjective", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "định lượng, đo lường bằng số liệu",
        "definition": "relating to numbers or amounts rather than quality",
        "example": "Economists employ rigorous quantitative models to forecast gross domestic product.",
        "collocations": ["quantitative analysis", "quantitative data", "quantitative measurement"]
    },
    "cite": {
        "word": "cite", "phonetic": "/saɪt/", "pos": "verb", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "trích dẫn nguồn tài liệu",
        "definition": "to mention something as proof for a theory or as a reason why something has happened",
        "example": "Remember to cite peer-reviewed academic publications in your bibliography.",
        "collocations": ["cite sources", "cite evidence", "frequently cited"]
    },
    "discourse": {
        "word": "discourse", "phonetic": "/ˈdɪs.kɔːs/", "pos": "noun", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "diễn ngôn, cuộc đàm luận học thuật",
        "definition": "communication in speech or writing, especially formal discussion of a topic",
        "example": "Constructive civic discourse is foundational to any functioning democracy.",
        "collocations": ["academic discourse", "public discourse", "political discourse"]
    },
    "evaluate": {
        "word": "evaluate", "phonetic": "/ɪˈvæl.ju.eɪt/", "pos": "verb", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "đánh giá, thẩm định",
        "definition": "to judge or calculate the quality, importance, amount, or value of something",
        "example": "The committee convened to evaluate the environmental feasibility of the canal.",
        "collocations": ["evaluate effectiveness", "carefully evaluate", "evaluate performance"]
    },
    "feasible": {
        "word": "feasible", "phonetic": "/ˈfiː.zə.bəl/", "pos": "adjective", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "khả thi, có thể thực hiện được",
        "definition": "able to be made, done, or achieved; reasonable and likely",
        "example": "Engineers proved that the high-speed rail proposal was technically feasible.",
        "collocations": ["economically feasible", "technically feasible", "feasible plan"]
    },
    "implicate": {
        "word": "implicate", "phonetic": "/ˈɪm.plɪ.keɪt/", "pos": "verb", "cefr": "C1", "topic": "Academic & IELTS",
        "meaning_vn": "liên can, hàm ý ngụ ý",
        "definition": "to show that someone is involved in something bad; or to imply something as a necessary consequence",
        "example": "Laboratory findings implicate chronic sleep deprivation in long-term cognitive decline.",
        "collocations": ["directly implicate", "implicate in disease", "implicate someone"]
    },
    "phenomenon": {
        "word": "phenomenon", "phonetic": "/fəˈnɒm.ɪ.nən/", "pos": "noun", "cefr": "B2", "topic": "Academic & IELTS",
        "meaning_vn": "hiện tượng khoa học / xã hội",
        "definition": "something that exists and can be seen, felt, tasted, etc., especially something unusual or interesting",
        "example": "The Northern Lights are a mesmerizing atmospheric phenomenon.",
        "collocations": ["natural phenomenon", "cultural phenomenon", "widespread phenomenon"]
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
