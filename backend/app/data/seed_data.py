import json
import datetime
from sqlalchemy.orm import Session
from ..models import User, Level, Challenge, SRSReview
from ..auth import hash_password

CAMBRIDGE_LEVELS_DATA = [
    # =========================================================================
    # LEVEL 1: FOOD & NUTRITION (CHEF GLUTTON) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 1: Neon Diner (Ẩm thực & Dinh dưỡng)",
        "theme": "Food & Nutrition",
        "description": "Đối đầu với Bếp Trưởng Bạo Chúa! Nắm vững từ vựng A1-B1 Cambridge về thức ăn, đồ uống và chế độ dinh dưỡng.",
        "boss_name": "Chef Glutton",
        "boss_title": "Bếp Trưởng Bạo Chúa",
        "boss_avatar": "boss_chef",
        "bpm": 105,
        "boss_hp": 100,
        "difficulty": "Easy",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Tôi muốn ăn một quả táo tươi ngon.",
                "en_target": "I want to eat a fresh apple",
                "extra_data": {
                    "distractors": ["drinks", "he", "an", "banana", "fast"],
                    "audio_hint": "I want to eat a fresh apple.",
                    "notes": "Lưu ý mạo từ 'a' trước phụ âm 'fresh'."
                },
                "order_index": 1
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "recipe",
                "extra_data": {
                    "sentence_with_blank": "She is following a traditional Italian ___ to make pasta.",
                    "hint": "Danh từ chỉ 'công thức nấu ăn' (r______)",
                    "phonetic": "/ˈres.ə.pi/",
                    "meaning_vn": "công thức nấu ăn"
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Thành phần dinh dưỡng / Nguyên liệu",
                "en_target": "ingredient",
                "extra_data": {
                    "phonetic": "/ɪnˈɡriː.di.ənt/",
                    "meaning_vn": "nguyên liệu, thành phần",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "Fresh vegetables are the main ingredient of this soup."
                },
                "order_index": 3
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Một chế độ ăn uống lành mạnh rất quan trọng đối với trẻ em.",
                "en_target": "A healthy diet is very important for children",
                "extra_data": {
                    "distractors": ["fast", "sweet", "bad", "play"],
                    "audio_hint": "A healthy diet is very important for children.",
                    "notes": "Cấu trúc chủ ngữ số ít đi với động từ to be 'is'."
                },
                "order_index": 4
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ có nghĩa 'ẩm thực, phong cách nấu nướng':",
                "en_target": "cuisine",
                "extra_data": {
                    "sentence_with_blank": "Vietnamese ___ is world-famous for its delicious street food.",
                    "hint": "Bắt đầu bằng chữ 'c' (c______)",
                    "phonetic": "/kwɪˈziːn/",
                    "meaning_vn": "ẩm thực"
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Đồ uống, thức uống giải khát",
                "en_target": "beverage",
                "extra_data": {
                    "phonetic": "/ˈbev.ər.ɪdʒ/",
                    "meaning_vn": "đồ uống, thức uống",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Hot beverages include tea and coffee."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'chất đạm':",
                "en_target": "protein",
                "extra_data": {
                    "sentence_with_blank": "Eggs and chicken are rich in dietary ___ for muscle growth.",
                    "hint": "Chất đạm (p______)",
                    "phonetic": "/ˈprəʊ.tiːn/",
                    "meaning_vn": "chất đạm, protein"
                },
                "order_index": 7
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Rau củ hữu cơ tươi ngon hơn.",
                "en_target": "Fresh organic vegetables taste more delicious",
                "extra_data": {
                    "distractors": ["sour", "canned", "oil", "heavy"],
                    "audio_hint": "Fresh organic vegetables taste more delicious."
                },
                "order_index": 8
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự ngon miệng, cảm giác thèm ăn",
                "en_target": "appetite",
                "extra_data": {
                    "phonetic": "/ˈæp.ə.taɪt/",
                    "meaning_vn": "cảm giác ngon miệng, thèm ăn",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "Exercise gives you a good appetite."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp các câu sau thành một đoạn văn hoàn chỉnh về bữa sáng dinh dưỡng:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, drinking a glass of warm lemon water boosts your metabolism."},
                        {"id": 2, "text": "Next, prepare an omelet with fresh spinach and whole-grain toast."},
                        {"id": 3, "text": "Then, enjoy a cup of green tea to provide gentle antioxidants."},
                        {"id": 4, "text": "Finally, you are energized and prepared for a productive workday."}
                    ]
                },
                "order_index": 10
            }
        ]
    },

    # =========================================================================
    # LEVEL 2: TECHNOLOGY & AI (CYBERCORE AI) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 2: Cyber Grid (Công nghệ & Trí tuệ Nhân tạo)",
        "theme": "Technology & AI",
        "description": "Đột nhập vào lõi máy chủ của CyberCore AI! Thử thách từ vựng Cambridge B1-B2 về phần mềm, an ninh mạng và thuật toán.",
        "boss_name": "CyberCore AI",
        "boss_title": "Trí tuệ Siêu việt",
        "boss_avatar": "boss_cyber",
        "bpm": 120,
        "boss_hp": 120,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc.",
                "en_target": "Artificial intelligence is changing the way we work",
                "extra_data": {
                    "distractors": ["robot", "games", "sleep", "slow"],
                    "audio_hint": "Artificial intelligence is changing the way we work."
                },
                "order_index": 1
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'an ninh mạng':",
                "en_target": "cybersecurity",
                "extra_data": {
                    "sentence_with_blank": "Banks spend millions every year to upgrade their ___ systems.",
                    "hint": "An ninh mạng (c___________)",
                    "phonetic": "/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/",
                    "meaning_vn": "an ninh mạng"
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Thuật toán máy tính",
                "en_target": "algorithm",
                "extra_data": {
                    "phonetic": "/ˈæl.ɡə.rɪ.ðəm/",
                    "meaning_vn": "thuật toán",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Search engines use complex algorithms to rank websites."
                },
                "order_index": 3
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'sự tự động hóa':",
                "en_target": "automation",
                "extra_data": {
                    "sentence_with_blank": "Factory ___ has reduced human errors and boosted productivity.",
                    "hint": "Tự động hóa (a_________)",
                    "phonetic": "/ˌɔː.təˈmeɪ.ʃən/",
                    "meaning_vn": "tự động hóa"
                },
                "order_index": 4
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Dữ liệu được mã hóa để bảo vệ an toàn thông tin.",
                "en_target": "Data is encrypted to protect user privacy",
                "extra_data": {
                    "distractors": ["open", "stolen", "loss", "broken"],
                    "audio_hint": "Data is encrypted to protect user privacy."
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự đổi mới, sáng tạo công nghệ",
                "en_target": "innovation",
                "extra_data": {
                    "phonetic": "/ˌɪn.əˈveɪ.ʃən/",
                    "meaning_vn": "sự đổi mới, sáng tạo",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Technological innovation drives economic growth."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'cơ sở dữ liệu':",
                "en_target": "database",
                "extra_data": {
                    "sentence_with_blank": "All customer records are safely stored in a cloud ___.",
                    "hint": "Cơ sở dữ liệu (d_______)",
                    "phonetic": "/ˈdeɪ.tə.beɪs/",
                    "meaning_vn": "cơ sở dữ liệu"
                },
                "order_index": 7
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Giao thức mạng máy tính",
                "en_target": "protocol",
                "extra_data": {
                    "phonetic": "/ˈprəʊ.tə.kɒl/",
                    "meaning_vn": "giao thức mạng",
                    "part_of_speech": "noun (Cambridge C1)",
                    "example": "HTTPS is the standard security protocol for websites."
                },
                "order_index": 8
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Giao diện người dùng phải trực quan và dễ sử dụng.",
                "en_target": "The user interface should be clean and intuitive",
                "extra_data": {
                    "distractors": ["ugly", "slow", "buggy", "heavy"],
                    "audio_hint": "The user interface should be clean and intuitive."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp đoạn văn mô tả sự phát triển của điện toán đám mây:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "In the past, organizations stored all their data on local hard drives."},
                        {"id": 2, "text": "However, physical servers were costly to maintain and vulnerable to damage."},
                        {"id": 3, "text": "Today, cloud computing allows instant access to remote data anywhere."},
                        {"id": 4, "text": "Consequently, global business agility and security have reached new heights."}
                    ]
                },
                "order_index": 10
            }
        ]
    },

    # =========================================================================
    # LEVEL 3: NATURE & ENVIRONMENT (FOREST CHIMERA) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 3: Wild Sanctuary (Môi trường & Thiên nhiên)",
        "theme": "Nature & Environment",
        "description": "Lạc vào rừng thiêng của Quái Thú Sinh Thái! Bộ từ vựng Cambridge B1-B2 về đa dạng sinh học, biến đổi khí hậu và bảo tồn.",
        "boss_name": "Forest Chimera",
        "boss_title": "Thú Vương Rừng Thiêng",
        "boss_avatar": "boss_chimera",
        "bpm": 115,
        "boss_hp": 120,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Chúng ta phải bảo vệ các loài động vật hoang dã nguy cấp.",
                "en_target": "We must protect endangered species of wildlife",
                "extra_data": {
                    "distractors": ["hunt", "kill", "forest", "tree"],
                    "audio_hint": "We must protect endangered species of wildlife."
                },
                "order_index": 1
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'sự đa dạng sinh học':",
                "en_target": "biodiversity",
                "extra_data": {
                    "sentence_with_blank": "The tropical rainforest contains an extraordinary wealth of plant ___.",
                    "hint": "Đa dạng sinh thái (b___________)",
                    "phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/",
                    "meaning_vn": "sự đa dạng sinh học"
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Hệ sinh thái tự nhiên",
                "en_target": "ecosystem",
                "extra_data": {
                    "phonetic": "/ˈiː.kəʊˌsɪs.təm/",
                    "meaning_vn": "hệ sinh thái",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Coral reefs form a fragile marine ecosystem."
                },
                "order_index": 3
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ có nghĩa 'bền vững':",
                "en_target": "sustainable",
                "extra_data": {
                    "sentence_with_blank": "Solar and wind power are key sources of ___ clean energy.",
                    "hint": "Bền vững (s__________)",
                    "phonetic": "/səˈsteɪ.nə.bəl/",
                    "meaning_vn": "bền vững"
                },
                "order_index": 4
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Năng lượng tái tạo giúp giảm lượng khí thải carbon.",
                "en_target": "Renewable energy helps reduce our carbon footprint",
                "extra_data": {
                    "distractors": ["coal", "burn", "smoke", "dirty"],
                    "audio_hint": "Renewable energy helps reduce our carbon footprint."
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Nạn chặt phá rừng",
                "en_target": "deforestation",
                "extra_data": {
                    "phonetic": "/diːˌfɒr.ɪˈsteɪ.ʃən/",
                    "meaning_vn": "nạn phá rừng",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Deforestation threatens indigenous wildlife habitats."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'sự tuyệt chủng':",
                "en_target": "extinction",
                "extra_data": {
                    "sentence_with_blank": "Many rare animal species are currently facing the threat of ___.",
                    "hint": "Tuyệt chủng (e_________)",
                    "phonetic": "/ɪkˈstɪŋk.ʃən/",
                    "meaning_vn": "sự tuyệt chủng"
                },
                "order_index": 7
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Môi trường sống tự nhiên của sinh vật",
                "en_target": "habitat",
                "extra_data": {
                    "phonetic": "/ˈhæb.ɪ.tæt/",
                    "meaning_vn": "môi trường sống tự nhiên",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "Panda bears need their natural bamboo habitat to survive."
                },
                "order_index": 8
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Khí thải nhà kính gây ra hiện tượng nóng lên toàn cầu.",
                "en_target": "Greenhouse gas emissions cause rapid global warming",
                "extra_data": {
                    "distractors": ["ice", "cold", "winter", "clean"],
                    "audio_hint": "Greenhouse gas emissions cause rapid global warming."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp chuỗi nguyên nhân và giải pháp cho biến đổi khí hậu:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "Global temperatures continue to rise due to greenhouse gas emissions."},
                        {"id": 2, "text": "As polar glaciers melt, sea levels threaten coastal communities."},
                        {"id": 3, "text": "Nations must rapidly transition toward renewable solar and wind power."},
                        {"id": 4, "text": "Together, collective environmental conservation can restore planetary equilibrium."}
                    ]
                },
                "order_index": 10
            }
        ]
    },

    # =========================================================================
    # LEVEL 4: BUSINESS & ECONOMICS (LORD MONOPOLY) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 4: Business Empire (Kinh doanh & Tài chính)",
        "theme": "Business & Economics",
        "description": "Vượt qua những cạm bẫy thương trường của Bá tước Độc quyền! Bộ từ vựng Cambridge Business & Economics B2-C1.",
        "boss_name": "Lord Monopoly",
        "boss_title": "Bá Tước Tài Chính",
        "boss_avatar": "boss_monopoly",
        "bpm": 130,
        "boss_hp": 130,
        "difficulty": "Hard",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'doanh nhân khởi nghiệp':",
                "en_target": "entrepreneur",
                "extra_data": {
                    "sentence_with_blank": "An innovative ___ takes financial risks to establish a new venture.",
                    "hint": "Doanh nhân khởi nghiệp (e___________)",
                    "phonetic": "/ˌɒn.trə.prəˈnɜːr/",
                    "meaning_vn": "doanh nhân khởi nghiệp"
                },
                "order_index": 1
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Công ty báo cáo doanh thu hàng năm tăng trưởng mạnh mẽ.",
                "en_target": "The company reported strong annual revenue growth",
                "extra_data": {
                    "distractors": ["loss", "debt", "fail", "bad"],
                    "audio_hint": "The company reported strong annual revenue growth."
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự độc quyền thị trường",
                "en_target": "monopoly",
                "extra_data": {
                    "phonetic": "/məˈnɒp.əl.i/",
                    "meaning_vn": "sự độc quyền kinh doanh",
                    "part_of_speech": "noun (Cambridge C1)",
                    "example": "Antitrust laws prevent large firms from forming a monopoly."
                },
                "order_index": 3
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'khoản đầu tư':",
                "en_target": "investment",
                "extra_data": {
                    "sentence_with_blank": "Real estate remains a reliable long-term capital ___.",
                    "hint": "Khoản đầu tư (i_________)",
                    "phonetic": "/ɪnˈvest.mənt/",
                    "meaning_vn": "khoản đầu tư"
                },
                "order_index": 4
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Cổ đông nhận được cổ tức hàng quý hấp dẫn.",
                "en_target": "Shareholders received an attractive quarterly cash dividend",
                "extra_data": {
                    "distractors": ["tax", "penalty", "bank", "fine"],
                    "audio_hint": "Shareholders received an attractive quarterly cash dividend."
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Lạm phát kinh tế",
                "en_target": "inflation",
                "extra_data": {
                    "phonetic": "/ɪnˈfleɪ.ʃən/",
                    "meaning_vn": "lạm phát",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Rising energy prices pushed annual inflation to a record high."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'đàm phán, thương lượng':",
                "en_target": "negotiate",
                "extra_data": {
                    "sentence_with_blank": "Both parties gathered to ___ a mutually beneficial contract.",
                    "hint": "Đàm phán (n________)",
                    "phonetic": "/nəˈɡəʊ.ʃi.eɪt/",
                    "meaning_vn": "đàm phán, thương lượng"
                },
                "order_index": 7
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Tài sản kinh doanh có giá trị",
                "en_target": "asset",
                "extra_data": {
                    "phonetic": "/ˈæs.et/",
                    "meaning_vn": "tài sản",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Patents and trademarks are valuable corporate assets."
                },
                "order_index": 8
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Một chiến lược kinh doanh tốt mang lại lợi nhuận cao.",
                "en_target": "A sound business strategy yields high profit margins",
                "extra_data": {
                    "distractors": ["debt", "loss", "bankrupt", "cost"],
                    "audio_hint": "A sound business strategy yields high profit margins."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp vòng đời phát triển sản phẩm của một doanh nghiệp:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, the team conducts thorough market research to identify customer pain points."},
                        {"id": 2, "text": "Next, engineers build an early prototype and test it with pilot users."},
                        {"id": 3, "text": "Then, a targeted digital marketing campaign creates pre-launch excitement."},
                        {"id": 4, "text": "Finally, the product launches globally and drives substantial recurring revenue."}
                    ]
                },
                "order_index": 10
            }
        ]
    },

    # =========================================================================
    # LEVEL 5: TRAVEL & CULTURE (CAPTAIN NOMAD) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 5: Global Voyager (Du lịch & Văn hóa Quốc tế)",
        "theme": "Travel & Culture",
        "description": "Chu du khắp thế giới cùng Thuyền Trưởng Viễn Du! Bộ từ vựng Cambridge A2-B2 về du lịch, phong tục và di sản.",
        "boss_name": "Captain Nomad",
        "boss_title": "Thuyền Trưởng Viễn Du",
        "boss_avatar": "boss_nomad",
        "bpm": 115,
        "boss_hp": 110,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'lịch trình chuyến đi':",
                "en_target": "itinerary",
                "extra_data": {
                    "sentence_with_blank": "Our guided tour ___ covers historic temples in Kyoto and Tokyo.",
                    "hint": "Lịch trình (i________)",
                    "phonetic": "/aɪˈtɪn.ər.ər.i/",
                    "meaning_vn": "lịch trình"
                },
                "order_index": 1
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Hội An là một di sản văn hóa thế giới nổi tiếng.",
                "en_target": "Hoi An is a famous world cultural heritage site",
                "extra_data": {
                    "distractors": ["modern", "car", "factory", "dirty"],
                    "audio_hint": "Hoi An is a famous world cultural heritage site."
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự hiếu khách nồng hậu",
                "en_target": "hospitality",
                "extra_data": {
                    "phonetic": "/ˌhɒs.pɪˈtæl.ə.ti/",
                    "meaning_vn": "sự hiếu khách, ngành khách sạn",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "We appreciated the warm hospitality of the locals."
                },
                "order_index": 3
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'điểm đến du lịch':",
                "en_target": "destination",
                "extra_data": {
                    "sentence_with_blank": "Da Nang is a premier holiday ___ for coastal tourists.",
                    "hint": "Điểm đến (d__________)",
                    "phonetic": "/ˌdes.tɪˈneɪ.ʃən/",
                    "meaning_vn": "điểm đến"
                },
                "order_index": 4
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Khách du lịch thích mua quà lưu niệm truyền thống.",
                "en_target": "Tourists love buying traditional handmade souvenirs",
                "extra_data": {
                    "distractors": ["rubbish", "iron", "ugly", "throw"],
                    "audio_hint": "Tourists love buying traditional handmade souvenirs."
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Thắng cảnh, địa danh nổi tiếng",
                "en_target": "landmark",
                "extra_data": {
                    "phonetic": "/ˈlænd.mɑːk/",
                    "meaning_vn": "thắng cảnh, địa danh",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "The Golden Gate Bridge is an iconic landmark of San Francisco."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ có nghĩa 'chỗ ở, nơi lưu trú':",
                "en_target": "accommodation",
                "extra_data": {
                    "sentence_with_blank": "We reserved comfortable hotel ___ near the central train station.",
                    "hint": "Nơi lưu trú (a____________)",
                    "phonetic": "/əˌkɒm.əˈdeɪ.ʃən/",
                    "meaning_vn": "chỗ ở, lưu trú"
                },
                "order_index": 7
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Đẹp như tranh vẽ",
                "en_target": "picturesque",
                "extra_data": {
                    "phonetic": "/ˌpɪk.tʃərˈesk/",
                    "meaning_vn": "đẹp như tranh vẽ",
                    "part_of_speech": "adjective (Cambridge B2)",
                    "example": "They visited picturesque fishing villages along the rugged coast."
                },
                "order_index": 8
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Du lịch giúp bạn tôn trọng phong tục nước ngoài.",
                "en_target": "Travel helps you understand and respect foreign customs",
                "extra_data": {
                    "distractors": ["fight", "anger", "hate", "war"],
                    "audio_hint": "Travel helps you understand and respect foreign customs."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp các bước chuẩn bị cho một chuyến du lịch nước ngoài:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, check passport validity and apply for necessary visas."},
                        {"id": 2, "text": "Next, compare airfares and secure your round-trip flight tickets."},
                        {"id": 3, "text": "Then, book convenient accommodations and create a flexible daily itinerary."},
                        {"id": 4, "text": "Finally, pack essentials and embark on your exciting journey."}
                    ]
                },
                "order_index": 10
            }
        ]
    },

    # =========================================================================
    # LEVEL 6: ACADEMIC & IELTS MASTERY (GRAND EXAMINER) - 10 CHALLENGES
    # =========================================================================
    {
        "title": "Level 6: Academic Summit (IELTS & Luận Học thuật)",
        "theme": "Academic & IELTS Mastery",
        "description": "Đối mặt với Đại Giám Khảo Học Thuật! Bộ từ vựng tinh hoa C1 chuẩn Cambridge IELTS phục vụ viết luận và phân tích phản biện.",
        "boss_name": "Grand Examiner",
        "boss_title": "Đại Giám Khảo Học Thuật",
        "boss_avatar": "boss_examiner",
        "bpm": 125,
        "boss_hp": 150,
        "difficulty": "Hard",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'chưa từng có tiền lệ':",
                "en_target": "unprecedented",
                "extra_data": {
                    "sentence_with_blank": "The modern digital era has witnessed ___ technological disruption.",
                    "hint": "Chưa từng có (u____________)",
                    "phonetic": "/ʌnˈpres.ɪ.den.tɪd/",
                    "meaning_vn": "chưa từng có tiền lệ"
                },
                "order_index": 1
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Giáo dục đóng một vai trò then chốt trong phát triển xã hội.",
                "en_target": "Education plays a pivotal role in social development",
                "extra_data": {
                    "distractors": ["tiny", "useless", "cheap", "stop"],
                    "audio_hint": "Education plays a pivotal role in social development."
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Khuôn mẫu, mô hình tư duy chuẩn mực",
                "en_target": "paradigm",
                "extra_data": {
                    "phonetic": "/ˈpær.ə.daɪm/",
                    "meaning_vn": "mô hình, khuôn mẫu tư duy",
                    "part_of_speech": "noun (Cambridge C1)",
                    "example": "Artificial intelligence creates a paradigm shift in scientific inquiry."
                },
                "order_index": 3
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ có nghĩa 'dựa trên thực nghiệm':",
                "en_target": "empirical",
                "extra_data": {
                    "sentence_with_blank": "Valid scientific conclusions must rely upon sound ___ evidence.",
                    "hint": "Thực nghiệm (e________)",
                    "phonetic": "/ɪmˈpɪr.ɪ.kəl/",
                    "meaning_vn": "dựa trên thực nghiệm"
                },
                "order_index": 4
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Các nhà khoa học tiến hành thí nghiệm để kiểm chứng giả thuyết.",
                "en_target": "Scientists conducted experiments to test their primary hypothesis",
                "extra_data": {
                    "distractors": ["guess", "rumor", "lie", "false"],
                    "audio_hint": "Scientists conducted experiments to test their primary hypothesis."
                },
                "order_index": 5
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Toàn diện, bao quát mọi mặt",
                "en_target": "comprehensive",
                "extra_data": {
                    "phonetic": "/ˌkɒm.prɪˈhen.sɪv/",
                    "meaning_vn": "toàn diện, sâu rộng",
                    "part_of_speech": "adjective (Cambridge B2)",
                    "example": "The thesis provided a comprehensive overview of urban economics."
                },
                "order_index": 6
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ chỉ 'phương pháp luận nghiên cứu':",
                "en_target": "methodology",
                "extra_data": {
                    "sentence_with_blank": "The author defended the research ___ utilized in the field study.",
                    "hint": "Phương pháp luận (m__________)",
                    "phonetic": "/ˌmeθ.əˈdɒl.ə.dʒi/",
                    "meaning_vn": "phương pháp luận"
                },
                "order_index": 7
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Khả thi, có thể thực hiện thành công",
                "en_target": "feasible",
                "extra_data": {
                    "phonetic": "/ˈfiː.zə.bəl/",
                    "meaning_vn": "khả thi",
                    "part_of_speech": "adjective (Cambridge B2)",
                    "example": "Civil engineers proved the offshore wind farm was economically feasible."
                },
                "order_index": 8
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Nghiên cứu định lượng cung cấp phân tích thống kê chính xác.",
                "en_target": "Quantitative research provides rigorous and accurate statistical analysis",
                "extra_data": {
                    "distractors": ["random", "guess", "story", "bad"],
                    "audio_hint": "Quantitative research provides rigorous and accurate statistical analysis."
                },
                "order_index": 9
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp bài luận phân tích tác động của tự động hóa:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "It is undeniable that automation has streamlined modern industrial production."},
                        {"id": 2, "text": "Nonetheless, rapid mechanization risks displacing vulnerable segments of the workforce."},
                        {"id": 3, "text": "Governments must therefore invest comprehensively in adult vocational retraining programs."},
                        {"id": 4, "text": "Ultimately, proactive technological governance ensures equitable prosperity for all."}
                    ]
                },
                "order_index": 10
            }
        ]
    }
]

def seed_database(db: Session):
    """
    Seeds initial users, 6 Cambridge levels with 10 challenges each, and sample SRS data.
    Syncs/updates levels automatically if fewer challenges are found in existing database.
    """
    # 1. Seed Users (Teacher & Student)
    teacher = db.query(User).filter(User.username == "teacher").first()
    if not teacher:
        teacher = User(
            username="teacher",
            email="teacher@wordrhythm.com",
            hashed_password=hash_password("teacher123"),
            role="teacher"
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

    student = db.query(User).filter(User.username == "student").first()
    if not student:
        student = User(
            username="student",
            email="student@wordrhythm.com",
            hashed_password=hash_password("student123"),
            role="student"
        )
        db.add(student)
        db.commit()
        db.refresh(student)

    teacherdemo = db.query(User).filter(User.username == "teacherdemo").first()
    if not teacherdemo:
        teacherdemo = User(
            username="teacherdemo",
            email="teacherdemo@wordrhythm.com",
            hashed_password=hash_password("123456"),
            role="teacher"
        )
        db.add(teacherdemo)
        db.commit()
        db.refresh(teacherdemo)

    # 2. Seed Levels & 10 Challenges per level
    for level_data in CAMBRIDGE_LEVELS_DATA:
        existing_lvl = db.query(Level).filter(Level.title == level_data["title"]).first()
        if not existing_lvl:
            lvl = Level(
                title=level_data["title"],
                theme=level_data["theme"],
                description=level_data["description"],
                boss_name=level_data["boss_name"],
                boss_title=level_data["boss_title"],
                boss_avatar=level_data["boss_avatar"],
                bpm=level_data["bpm"],
                boss_hp=level_data["boss_hp"],
                difficulty=level_data["difficulty"],
                is_published=level_data["is_published"],
                created_by_id=teacher.id
            )
            db.add(lvl)
            db.commit()
            db.refresh(lvl)

            for c_data in level_data["challenges"]:
                ch = Challenge(
                    level_id=lvl.id,
                    challenge_type=c_data["challenge_type"],
                    vn_prompt=c_data["vn_prompt"],
                    en_target=c_data["en_target"],
                    extra_data=json.dumps(c_data["extra_data"], ensure_ascii=False),
                    order_index=c_data["order_index"]
                )
                db.add(ch)
            db.commit()
        else:
            # Sync boss avatar, bpm, hp
            existing_lvl.boss_avatar = level_data["boss_avatar"]
            existing_lvl.bpm = level_data["bpm"]
            existing_lvl.boss_hp = level_data["boss_hp"]
            existing_lvl.boss_name = level_data["boss_name"]
            existing_lvl.boss_title = level_data["boss_title"]
            db.commit()

            # Ensure all 10 challenges are synced
            existing_count = db.query(Challenge).filter(Challenge.level_id == existing_lvl.id).count()
            if existing_count < len(level_data["challenges"]):
                db.query(Challenge).filter(Challenge.level_id == existing_lvl.id).delete()
                for c_data in level_data["challenges"]:
                    ch = Challenge(
                        level_id=existing_lvl.id,
                        challenge_type=c_data["challenge_type"],
                        vn_prompt=c_data["vn_prompt"],
                        en_target=c_data["en_target"],
                        extra_data=json.dumps(c_data["extra_data"], ensure_ascii=False),
                        order_index=c_data["order_index"]
                    )
                    db.add(ch)
                db.commit()

    # 3. Seed initial SRS reviews for student demonstration
    initial_srs = db.query(SRSReview).filter(SRSReview.user_id == student.id).first()
    if not initial_srs:
        sample_words = [
            {"word": "human", "vn": "con người", "phonetic": "/ˈhjuː.mən/", "ef": 2.5, "n": 1, "days": 1, "mistakes": 0, "reviews": 1},
            {"word": "recipe", "vn": "công thức nấu ăn", "phonetic": "/ˈres.ə.pi/", "ef": 1.6, "n": 0, "days": 0, "mistakes": 3, "reviews": 4},
            {"word": "biodiversity", "vn": "đa dạng sinh học", "phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/", "ef": 1.7, "n": 0, "days": 0, "mistakes": 2, "reviews": 3},
            {"word": "ingredient", "vn": "nguyên liệu, thành phần", "phonetic": "/ɪnˈɡriː.di.ənt/", "ef": 2.6, "n": 2, "days": 6, "mistakes": 0, "reviews": 2},
            {"word": "algorithm", "vn": "thuật toán", "phonetic": "/ˈæl.ɡə.rɪ.ðəm/", "ef": 2.3, "n": 1, "days": 1, "mistakes": 1, "reviews": 2},
            {"word": "unprecedented", "vn": "chưa từng có tiền lệ", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "ef": 1.5, "n": 0, "days": 0, "mistakes": 3, "reviews": 3},
            {"word": "sustainable", "vn": "bền vững", "phonetic": "/səˈsteɪ.nə.bəl/", "ef": 2.5, "n": 1, "days": 1, "mistakes": 0, "reviews": 1},
        ]
        now = datetime.datetime.utcnow()
        for sw in sample_words:
            review_date = now - datetime.timedelta(hours=1) if sw["mistakes"] > 0 else now + datetime.timedelta(days=sw["days"])
            srs_obj = SRSReview(
                user_id=student.id,
                word_en=sw["word"],
                meaning_vn=sw["vn"],
                phonetic=sw["phonetic"],
                repetition_n=sw["n"],
                ease_factor=sw["ef"],
                interval_days=sw["days"],
                next_review_date=review_date,
                total_reviews=sw["reviews"],
                total_mistakes=sw["mistakes"],
                last_reviewed_at=now
            )
            db.add(srs_obj)
        db.commit()
