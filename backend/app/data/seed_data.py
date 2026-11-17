import json
import datetime
from sqlalchemy.orm import Session
from ..models import User, Level, Challenge, SRSReview
from ..auth import hash_password

CAMBRIDGE_LEVELS_DATA = [
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
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp các câu sau thành một đoạn văn hoàn chỉnh về bữa sáng dinh dưỡng:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, drinking a glass of warm lemon water boosts your metabolism."},
                        {"id": 2, "text": "Next, prepare oatmeal topped with fresh berries and almonds."},
                        {"id": 3, "text": "Then, enjoy your meal slowly to ensure optimal digestion."},
                        {"id": 4, "text": "Finally, this healthy routine gives you sustained energy throughout the morning."}
                    ]
                },
                "order_index": 4
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "nutrition",
                "extra_data": {
                    "sentence_with_blank": "Adequate ___ is vital for a healthy immune system.",
                    "hint": "Dinh dưỡng (n________)",
                    "phonetic": "/njuːˈtrɪʃ.ən/",
                    "meaning_vn": "dinh dưỡng"
                },
                "order_index": 5
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Bữa sáng là bữa ăn quan trọng nhất trong ngày.",
                "en_target": "Breakfast is the most important meal of the day",
                "extra_data": {
                    "distractors": ["lunch", "are", "more", "night", "good"],
                    "audio_hint": "Breakfast is the most important meal of the day.",
                    "notes": "So sánh nhất 'the most important'."
                },
                "order_index": 6
            }
        ]
    },
    {
        "title": "Level 2: Cyber City (Công nghệ & Trí tuệ Nhân tạo)",
        "theme": "Technology & AI",
        "description": "Thâm nhập vào hệ thống lõi và đánh bại CyberCore AI! Luyện tập từ vựng công nghệ hiện đại Cambridge B1-B2.",
        "boss_name": "CyberCore AI",
        "boss_title": "Trí tuệ Siêu việt",
        "boss_avatar": "boss_cyber",
        "bpm": 118,
        "boss_hp": 120,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "con người / loài người",
                "en_target": "human",
                "extra_data": {
                    "phonetic": "/ˈhjuː.mən/",
                    "meaning_vn": "con người, loài người",
                    "part_of_speech": "noun (Cambridge A2)",
                    "example": "AI is designed to assist human beings in solving complex problems."
                },
                "order_index": 1
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc.",
                "en_target": "Artificial intelligence is changing the way we work",
                "extra_data": {
                    "distractors": ["robot", "was", "sleep", "smart", "they"],
                    "audio_hint": "Artificial intelligence is changing the way we work.",
                    "notes": "Thì hiện tại tiếp diễn biểu thị sự thay đổi."
                },
                "order_index": 2
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "algorithm",
                "extra_data": {
                    "sentence_with_blank": "The search engine relies on a sophisticated ___ to rank pages.",
                    "hint": "Thuật toán (a________)",
                    "phonetic": "/ˈæl.ɡə.rɪ.ðəm/",
                    "meaning_vn": "thuật toán"
                },
                "order_index": 3
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Bảo mật mạng / An ninh thông tin",
                "en_target": "cybersecurity",
                "extra_data": {
                    "phonetic": "/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/",
                    "meaning_vn": "an ninh mạng",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Companies invest heavily in cybersecurity to protect sensitive data."
                },
                "order_index": 4
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "automation",
                "extra_data": {
                    "sentence_with_blank": "Modern factories use robotic ___ to assemble cars rapidly.",
                    "hint": "Sự tự động hóa (a_________)",
                    "phonetic": "/ˌɔː.təˈmeɪ.ʃən/",
                    "meaning_vn": "sự tự động hóa"
                },
                "order_index": 5
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp đoạn văn mô tả sự phát triển của điện toán đám mây:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "In the past, organizations stored all their data on local hard drives."},
                        {"id": 2, "text": "However, maintenance costs and hardware limitations became major hurdles."},
                        {"id": 3, "text": "Cloud computing emerged as a scalable and cost-effective alternative."},
                        {"id": 4, "text": "Today, businesses of all sizes utilize the cloud for global collaboration."}
                    ]
                },
                "order_index": 6
            }
        ]
    },
    {
        "title": "Level 3: Mystic Forest (Môi trường & Thiên nhiên)",
        "theme": "Nature & Wildlife",
        "description": "Thức tỉnh rừng già và chiến đấu với Vua Quái thú Chimera! Bộ từ vựng sinh thái, khí hậu từ Cambridge B1-B2.",
        "boss_name": "Forest Chimera",
        "boss_title": "Thú Vương Rừng Thiêng",
        "boss_avatar": "boss_chimera",
        "bpm": 125,
        "boss_hp": 120,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Chúng ta phải bảo vệ những loài động vật có nguy cơ tuyệt chủng.",
                "en_target": "We must protect endangered species from extinction",
                "extra_data": {
                    "distractors": ["destroy", "danger", "animal", "into", "hunters"],
                    "audio_hint": "We must protect endangered species from extinction.",
                    "notes": "Cụm 'endangered species' (loài có nguy cơ tuyệt chủng)."
                },
                "order_index": 1
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Đa dạng sinh học",
                "en_target": "biodiversity",
                "extra_data": {
                    "phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/",
                    "meaning_vn": "đa dạng sinh học",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "The Amazon rainforest is famous for its incredible biodiversity."
                },
                "order_index": 2
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "renewable",
                "extra_data": {
                    "sentence_with_blank": "Solar and wind power are clean sources of ___ energy.",
                    "hint": "Có thể tái tạo (r________)",
                    "phonetic": "/rɪˈnjuː.ə.bəl/",
                    "meaning_vn": "tái tạo được"
                },
                "order_index": 3
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Hệ sinh thái",
                "en_target": "ecosystem",
                "extra_data": {
                    "phonetic": "/ˈiː.koʊˌsɪs.təm/",
                    "meaning_vn": "hệ sinh thái",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "Pollution threatens fragile marine ecosystems around coral reefs."
                },
                "order_index": 4
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp chuỗi nguyên nhân và giải pháp cho biến đổi khí hậu:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "Global temperatures continue to rise due to greenhouse gas emissions."},
                        {"id": 2, "text": "As polar ice caps melt, sea levels threaten coastal communities."},
                        {"id": 3, "text": "Switching to green energy and reforestation are vital solutions."},
                        {"id": 4, "text": "Together, international cooperation can preserve our planet for future generations."}
                    ]
                },
                "order_index": 5
            }
        ]
    },
    {
        "title": "Level 4: Business Empire (Kinh doanh & Tài chính)",
        "theme": "Business & Finance",
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
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "entrepreneur",
                "extra_data": {
                    "sentence_with_blank": "An innovative ___ takes financial risks to establish a new venture.",
                    "hint": "Doanh nhân khởi nghiệp (e___________)",
                    "phonetic": "/ˌɒn.trə.prəˈnɜːr/",
                    "meaning_vn": "doanh nhân"
                },
                "order_index": 1
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự đầu tư / Vốn đầu tư",
                "en_target": "investment",
                "extra_data": {
                    "phonetic": "/ɪnˈvest.mənt/",
                    "meaning_vn": "khoản đầu tư, sự đầu tư",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "Education is the best investment you can make for your future."
                },
                "order_index": 2
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "revenue",
                "extra_data": {
                    "sentence_with_blank": "The startup announced a substantial increase in annual ___.",
                    "hint": "Doanh thu (r______)",
                    "phonetic": "/ˈrev.ən.juː/",
                    "meaning_vn": "doanh thu"
                },
                "order_index": 3
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Chiến lược tiếp thị tốt giúp gia tăng doanh số đáng kể.",
                "en_target": "A good marketing strategy increases sales significantly",
                "extra_data": {
                    "distractors": ["decrease", "plan", "are", "cheap", "losses"],
                    "audio_hint": "A good marketing strategy increases sales significantly.",
                    "notes": "Trạng từ 'significantly' bổ nghĩa cho động từ 'increases'."
                },
                "order_index": 4
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp vòng đời phát triển sản phẩm của một doanh nghiệp:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, the team conducts thorough market research to identify customer pain points."},
                        {"id": 2, "text": "Next, engineers build a minimum viable product to test core hypotheses."},
                        {"id": 3, "text": "Then, user feedback guides iterative refinements before the official launch."},
                        {"id": 4, "text": "Finally, marketing campaigns scale up to acquire market share."}
                    ]
                },
                "order_index": 5
            }
        ]
    },
    {
        "title": "Level 5: Global Voyager (Du lịch & Văn hóa Quốc tế)",
        "theme": "Travel & Culture",
        "description": "Chu du khắp thế giới cùng Thuyền Trưởng Viễn Du! Bộ từ vựng Cambridge A2-B2 về du lịch, phong tục và di sản.",
        "boss_name": "Captain Nomad",
        "boss_title": "Thuyền Trưởng Viễn Du",
        "boss_avatar": "boss_monopoly",
        "bpm": 115,
        "boss_hp": 110,
        "difficulty": "Medium",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "destination",
                "extra_data": {
                    "sentence_with_blank": "Paris is one of the most popular tourist ___ in the world.",
                    "hint": "Điểm đến du lịch (d__________)",
                    "phonetic": "/ˌdes.tɪˈneɪ.ʃən/",
                    "meaning_vn": "điểm đến"
                },
                "order_index": 1
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Lịch trình chuyến đi",
                "en_target": "itinerary",
                "extra_data": {
                    "phonetic": "/aɪˈtɪn.ər.ər.i/",
                    "meaning_vn": "lịch trình chuyến đi",
                    "part_of_speech": "noun (Cambridge B1)",
                    "example": "Our holiday itinerary includes visiting historical museums."
                },
                "order_index": 2
            },
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Du lịch mở rộng tầm nhìn và sự hiểu biết của chúng ta.",
                "en_target": "Traveling broadens our horizons and cultural understanding",
                "extra_data": {
                    "distractors": ["narrows", "is", "sleep", "hard", "money"],
                    "audio_hint": "Traveling broadens our horizons and cultural understanding.",
                    "notes": "Thành ngữ 'broadens our horizons' (mở rộng tầm mắt)."
                },
                "order_index": 3
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Sự hiếu khách, lòng mến khách",
                "en_target": "hospitality",
                "extra_data": {
                    "phonetic": "/ˌhɒs.pɪˈtæl.ə.ti/",
                    "meaning_vn": "lòng hiếu khách",
                    "part_of_speech": "noun (Cambridge B2)",
                    "example": "We were touched by the warm hospitality of the locals."
                },
                "order_index": 4
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp các bước chuẩn bị cho một chuyến du lịch nước ngoài:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "First, check passport validity and apply for necessary visas."},
                        {"id": 2, "text": "Next, book flight tickets and reserve accommodation in advance."},
                        {"id": 3, "text": "Then, pack lightweight clothes suitable for local weather conditions."},
                        {"id": 4, "text": "Finally, arrive at the international airport early for departure check-in."}
                    ]
                },
                "order_index": 5
            }
        ]
    },
    {
        "title": "Level 6: IELTS Titan Arena (Học thuật Đỉnh cao)",
        "theme": "Academic & IELTS Mastery",
        "description": "Thách thức tối thượng với Đại Giám Khảo Học Thuật! Nhịp điệu 140 BPM dồn dập, tổng hợp từ vựng C1-C2.",
        "boss_name": "Grand Examiner",
        "boss_title": "Đại Giám Khảo Học Thuật",
        "boss_avatar": "boss_examiner",
        "bpm": 140,
        "boss_hp": 150,
        "difficulty": "Hard",
        "is_published": True,
        "challenges": [
            {
                "challenge_type": "sentence_assemble",
                "vn_prompt": "Giáo dục đóng vai trò then chốt trong việc xóa đói giảm nghèo.",
                "en_target": "Education plays a pivotal role in eradicating poverty",
                "extra_data": {
                    "distractors": ["school", "makes", "poor", "money", "with"],
                    "audio_hint": "Education plays a pivotal role in eradicating poverty.",
                    "notes": "Collocation học thuật: 'play a pivotal role in'."
                },
                "order_index": 1
            },
            {
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "unprecedented",
                "extra_data": {
                    "sentence_with_blank": "The rapid advancement of quantum computing brings ___ opportunities.",
                    "hint": "Chưa từng có tiền lệ (u____________)",
                    "phonetic": "/ʌnˈpres.ɪ.den.tɪd/",
                    "meaning_vn": "chưa từng có"
                },
                "order_index": 2
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Bền vững / Thân thiện môi trường",
                "en_target": "sustainable",
                "extra_data": {
                    "phonetic": "/səˈsteɪ.nə.bəl/",
                    "meaning_vn": "bền vững",
                    "part_of_speech": "adjective (Cambridge B2)",
                    "example": "Sustainable development balances economic growth with environmental protection."
                },
                "order_index": 3
            },
            {
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "Mô hình, khuôn mẫu chuẩn",
                "en_target": "paradigm",
                "extra_data": {
                    "phonetic": "/ˈpær.ə.daɪm/",
                    "meaning_vn": "mô hình mẫu, hệ hình",
                    "part_of_speech": "noun (Cambridge C1)",
                    "example": "A fundamental paradigm shift occurred in computer science."
                },
                "order_index": 4
            },
            {
                "challenge_type": "paragraph_order",
                "vn_prompt": "Sắp xếp bài luận phân tích tác động của tự động hóa:",
                "en_target": "1|2|3|4",
                "extra_data": {
                    "sentences": [
                        {"id": 1, "text": "It is undeniable that automation has streamlined modern industrial production."},
                        {"id": 2, "text": "Consequently, routine manual labor is rapidly being superseded by machines."},
                        {"id": 3, "text": "This paradigm shift demands substantial investments in workforce upskilling."},
                        {"id": 4, "text": "Ultimately, lifelong learning will be essential for future economic resilience."}
                    ]
                },
                "order_index": 5
            }
        ]
    }
]

def seed_database(db: Session):
    """Populates users, levels, challenges, and initial SRS entries if db is empty."""
    # 1. Seed Users
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

    # 2. Seed Levels & Challenges
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

    # 3. Seed initial SRS reviews for demonstration
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
