-- ========================================================
-- WordRhythm Database Creation & Seed Script for Microsoft SQL Server
-- Target: SQL Server Management Studio (SSMS) 2016 / 2019 / 2022 / Azure SQL
-- Character Encoding: UTF-8 / NCHAR / NVARCHAR
-- ========================================================

USE master;
GO

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'WordRhythmDB')
BEGIN
    CREATE DATABASE WordRhythmDB COLLATE Latin1_General_100_CI_AS_SC_UTF8;
END
GO

USE WordRhythmDB;
GO

-- Drop foreign keys & tables if already exist
IF OBJECT_ID('dbo.leaderboard_entries', 'U') IS NOT NULL DROP TABLE dbo.leaderboard_entries;
IF OBJECT_ID('dbo.game_sessions', 'U') IS NOT NULL DROP TABLE dbo.game_sessions;
IF OBJECT_ID('dbo.srs_reviews', 'U') IS NOT NULL DROP TABLE dbo.srs_reviews;
IF OBJECT_ID('dbo.challenges', 'U') IS NOT NULL DROP TABLE dbo.challenges;
IF OBJECT_ID('dbo.levels', 'U') IS NOT NULL DROP TABLE dbo.levels;
IF OBJECT_ID('dbo.cambridge_vocabulary', 'U') IS NOT NULL DROP TABLE dbo.cambridge_vocabulary;
IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;
GO

-- Table: users
CREATE TABLE dbo.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    hashed_password NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL DEFAULT N'student',
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO
-- Table: levels
CREATE TABLE dbo.levels (
    id INT IDENTITY(1,1) PRIMARY KEY,
    title NVARCHAR(120) NOT NULL,
    theme NVARCHAR(80) NOT NULL,
    description NVARCHAR(MAX) NULL,
    boss_name NVARCHAR(80) NOT NULL,
    boss_title NVARCHAR(100) NOT NULL DEFAULT N'Guardian',
    boss_avatar NVARCHAR(50) NOT NULL DEFAULT N'boss_cyber',
    bpm INT NOT NULL DEFAULT 120,
    boss_hp INT NOT NULL DEFAULT 100,
    difficulty NVARCHAR(20) NOT NULL DEFAULT N'Medium',
    is_published BIT NOT NULL DEFAULT 1,
    created_by_id INT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_levels_created_by FOREIGN KEY (created_by_id) REFERENCES dbo.users(id) ON DELETE SET NULL
);
GO
-- Table: challenges
CREATE TABLE dbo.challenges (
    id INT IDENTITY(1,1) PRIMARY KEY,
    level_id INT NOT NULL,
    challenge_type NVARCHAR(40) NOT NULL, -- sentence_assemble, fill_blank, vocab_pronounce, paragraph_order
    vn_prompt NVARCHAR(MAX) NOT NULL,
    en_target NVARCHAR(MAX) NOT NULL,
    extra_data NVARCHAR(MAX) NULL, -- JSON formatted data
    order_index INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_challenges_level FOREIGN KEY (level_id) REFERENCES dbo.levels(id) ON DELETE CASCADE
);
GO
-- Table: srs_reviews (SuperMemo SM-2 Engine Data)
CREATE TABLE dbo.srs_reviews (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    word_en NVARCHAR(150) NOT NULL,
    meaning_vn NVARCHAR(255) NOT NULL,
    phonetic NVARCHAR(100) NULL,
    repetition_n INT NOT NULL DEFAULT 0,
    ease_factor FLOAT NOT NULL DEFAULT 2.5,
    interval_days INT NOT NULL DEFAULT 0,
    next_review_date DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    total_reviews INT NOT NULL DEFAULT 0,
    total_mistakes INT NOT NULL DEFAULT 0,
    last_reviewed_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_srs_user FOREIGN KEY (user_id) REFERENCES dbo.users(id) ON DELETE CASCADE
);
CREATE INDEX IX_srs_reviews_user_next ON dbo.srs_reviews(user_id, next_review_date);
GO
-- Table: game_sessions
CREATE TABLE dbo.game_sessions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    level_id INT NOT NULL,
    score INT NOT NULL DEFAULT 0,
    accuracy FLOAT NOT NULL DEFAULT 0.0,
    max_combo INT NOT NULL DEFAULT 0,
    won BIT NOT NULL DEFAULT 0,
    hp_remaining INT NOT NULL DEFAULT 0,
    completed_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_sessions_user FOREIGN KEY (user_id) REFERENCES dbo.users(id) ON DELETE CASCADE,
    CONSTRAINT FK_sessions_level FOREIGN KEY (level_id) REFERENCES dbo.levels(id) ON DELETE CASCADE
);
GO
-- Table: leaderboard_entries
CREATE TABLE dbo.leaderboard_entries (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    level_id INT NULL,
    score INT NOT NULL DEFAULT 0,
    accuracy FLOAT NOT NULL DEFAULT 0.0,
    max_combo INT NOT NULL DEFAULT 0,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT FK_leaderboard_user FOREIGN KEY (user_id) REFERENCES dbo.users(id) ON DELETE CASCADE,
    CONSTRAINT FK_leaderboard_level FOREIGN KEY (level_id) REFERENCES dbo.levels(id) ON DELETE SET NULL
);
GO
-- Table: cambridge_vocabulary
CREATE TABLE dbo.cambridge_vocabulary (
    id INT IDENTITY(1,1) PRIMARY KEY,
    word NVARCHAR(100) NOT NULL UNIQUE,
    phonetic NVARCHAR(100) NULL,
    part_of_speech NVARCHAR(30) NULL,
    cefr_level NVARCHAR(10) NULL,
    topic NVARCHAR(80) NULL,
    meaning_vn NVARCHAR(255) NOT NULL,
    definition NVARCHAR(MAX) NULL,
    example NVARCHAR(MAX) NULL,
    collocations NVARCHAR(MAX) NULL
);
GO

-- ==========================================
-- SEED DATA INSERTION
-- ==========================================

SET IDENTITY_INSERT dbo.users ON;
INSERT INTO dbo.users (id, username, email, hashed_password, role, created_at) VALUES (1, N'teacher', N'teacher@wordrhythm.com', N'$2b$12$gEbNvUv/YdkHynDe1V72eOC.cRtRKAasm/H0tAIKVzJ8PxgZFwB6a', N'teacher', N'2026-11-17 09:46:41');
INSERT INTO dbo.users (id, username, email, hashed_password, role, created_at) VALUES (2, N'student', N'student@wordrhythm.com', N'$2b$12$cBjZ/J4yizoC6mBTXuD6MehH1Pq/VQD9chXGKSrjkk8tciF5EDSs2', N'student', N'2026-11-17 09:46:41');
SET IDENTITY_INSERT dbo.users OFF;
GO

SET IDENTITY_INSERT dbo.levels ON;
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (1, N'Level 1: Neon Diner (Ẩm thực & Dinh dưỡng)', N'Food & Nutrition', N'Đối đầu với Bếp Trưởng Ma Quái! Nắm vững từ vựng A1-B1 Cambridge về thức ăn, đồ uống và chế độ dinh dưỡng.', N'Chef Glutton', N'Bếp Trưởng Bạo Chúa', N'boss_chef', 105, 100, N'Easy', 1, 1, N'2026-11-17 09:46:41');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (2, N'Level 2: Cyber City (Công nghệ & Trí tuệ Nhân tạo)', N'Technology & AI', N'Thâm nhập vào hệ thống lõi và đánh bại CyberCore AI! Luyện tập từ vựng công nghệ hiện đại Cambridge B1-B2.', N'CyberCore AI', N'Trí tuệ Siêu việt', N'boss_cyber', 118, 120, N'Medium', 1, 1, N'2026-11-17 09:46:41');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (3, N'Level 3: Mystic Forest (Môi trường & Thiên nhiên)', N'Nature & Wildlife', N'Thức tỉnh rừng già và chiến đấu với Vua Quái thú Chimera! Bộ từ vựng sinh thái, khí hậu từ Cambridge B1-B2.', N'Forest Chimera', N'Thú Vương Rừng Thiêng', N'boss_chimera', 125, 120, N'Medium', 1, 1, N'2026-11-17 09:46:41');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (4, N'Level 4: Business Empire (Kinh doanh & Tài chính)', N'Business & Finance', N'Vượt qua những cạm bẫy thương trường của Bá tước Độc quyền! Bộ từ vựng Cambridge Business & Economics B2-C1.', N'Lord Monopoly', N'Bá Tước Tài Chính', N'boss_monopoly', 130, 130, N'Hard', 1, 1, N'2026-11-17 09:46:41');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (5, N'Level 5: IELTS Titan Arena (Học thuật Đỉnh cao)', N'Academic & IELTS Mastery', N'Thách thức tối thượng với Giám Khảo Huyền Thoại! Nhịp điệu 140 BPM dồn dập, tổng hợp từ vựng học thuật Cambridge C1.', N'Grand Examiner', N'Đại Giám Khảo Học Thuật', N'boss_examiner', 140, 150, N'Hard', 1, 1, N'2026-11-17 09:46:41');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (6, N'Level 5: Global Voyager (Du lịch & Văn hóa Quốc tế)', N'Travel & Culture', N'Chu du khắp thế giới cùng Thuyền Trưởng Viễn Du! Bộ từ vựng Cambridge A2-B2 về du lịch, phong tục và di sản.', N'Captain Nomad', N'Thuyền Trưởng Viễn Du', N'boss_monopoly', 115, 110, N'Medium', 1, 1, N'2026-11-17 10:04:36');
INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES (7, N'Level 6: IELTS Titan Arena (Học thuật Đỉnh cao)', N'Academic & IELTS Mastery', N'Thách thức tối thượng với Đại Giám Khảo Học Thuật! Nhịp điệu 140 BPM dồn dập, tổng hợp từ vựng C1-C2.', N'Grand Examiner', N'Đại Giám Khảo Học Thuật', N'boss_examiner', 140, 150, N'Hard', 1, 1, N'2026-11-17 10:04:36');
SET IDENTITY_INSERT dbo.levels OFF;
GO

SET IDENTITY_INSERT dbo.challenges ON;
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (1, 1, N'sentence_assemble', N'Tôi muốn ăn một quả táo tươi ngon.', N'I want to eat a fresh apple', N'{"distractors": ["drinks", "he", "an", "banana", "fast"], "audio_hint": "I want to eat a fresh apple.", "notes": "Lưu ý mạo từ ''a'' trước phụ âm ''fresh''."}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (2, 1, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'recipe', N'{"sentence_with_blank": "She is following a traditional Italian ___ to make pasta.", "hint": "Danh từ chỉ ''công thức nấu ăn'' (r______)", "phonetic": "/ˈres.ə.pi/", "meaning_vn": "công thức nấu ăn"}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (3, 1, N'vocab_pronounce', N'Thành phần dinh dưỡng / Nguyên liệu', N'ingredient', N'{"phonetic": "/ɪnˈɡriː.di.ənt/", "meaning_vn": "nguyên liệu, thành phần", "part_of_speech": "noun (Cambridge B1)", "example": "Fresh vegetables are the main ingredient of this soup."}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (4, 1, N'paragraph_order', N'Sắp xếp các câu sau thành một đoạn văn hoàn chỉnh về bữa sáng dinh dưỡng:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "First, drinking a glass of warm lemon water boosts your metabolism."}, {"id": 2, "text": "Next, prepare oatmeal topped with fresh berries and almonds."}, {"id": 3, "text": "Then, enjoy your meal slowly to ensure optimal digestion."}, {"id": 4, "text": "Finally, this healthy routine gives you sustained energy throughout the morning."}]}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (5, 1, N'sentence_assemble', N'Bữa sáng là bữa ăn quan trọng nhất trong ngày.', N'Breakfast is the most important meal of the day', N'{"distractors": ["lunch", "are", "more", "night", "good"], "audio_hint": "Breakfast is the most important meal of the day.", "notes": "So sánh nhất ''the most important''."}', 5);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (6, 2, N'vocab_pronounce', N'con người / loài người', N'human', N'{"phonetic": "/ˈhjuː.mən/", "meaning_vn": "con người, loài người", "part_of_speech": "noun (Cambridge A2)", "example": "AI is designed to assist human beings in solving complex problems."}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (7, 2, N'sentence_assemble', N'Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc.', N'Artificial intelligence is changing the way we work', N'{"distractors": ["robot", "was", "sleep", "smart", "they"], "audio_hint": "Artificial intelligence is changing the way we work.", "notes": "Thì hiện tại tiếp diễn biểu thị sự thay đổi."}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (8, 2, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'algorithm', N'{"sentence_with_blank": "The search engine relies on a sophisticated ___ to rank pages.", "hint": "Thuật toán (a________)", "phonetic": "/ˈæl.ɡə.rɪ.ðəm/", "meaning_vn": "thuật toán"}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (9, 2, N'vocab_pronounce', N'Bảo mật mạng / An ninh thông tin', N'cybersecurity', N'{"phonetic": "/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/", "meaning_vn": "an ninh mạng", "part_of_speech": "noun (Cambridge B2)", "example": "Companies invest heavily in cybersecurity to protect sensitive data."}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (10, 2, N'paragraph_order', N'Sắp xếp đoạn văn mô tả sự phát triển của điện toán đám mây:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "In the past, organizations stored all their data on local hard drives."}, {"id": 2, "text": "However, maintenance costs and hardware limitations became major hurdles."}, {"id": 3, "text": "Cloud computing emerged as a scalable and cost-effective alternative."}, {"id": 4, "text": "Today, businesses of all sizes utilize the cloud for global collaboration."}]}', 5);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (11, 3, N'sentence_assemble', N'Chúng ta phải bảo vệ những loài động vật có nguy cơ tuyệt chủng.', N'We must protect endangered species from extinction', N'{"distractors": ["destroy", "danger", "animal", "into", "hunters"], "audio_hint": "We must protect endangered species from extinction.", "notes": "Cụm ''endangered species'' (loài có nguy cơ tuyệt chủng)."}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (12, 3, N'vocab_pronounce', N'Đa dạng sinh học', N'biodiversity', N'{"phonetic": "/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/", "meaning_vn": "đa dạng sinh học", "part_of_speech": "noun (Cambridge B2)", "example": "The Amazon rainforest is famous for its incredible biodiversity."}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (13, 3, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'renewable', N'{"sentence_with_blank": "Solar and wind power are clean sources of ___ energy.", "hint": "Có thể tái tạo (r________)", "phonetic": "/rɪˈnjuː.ə.bəl/", "meaning_vn": "tái tạo được"}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (14, 3, N'paragraph_order', N'Sắp xếp chuỗi nguyên nhân và giải pháp cho biến đổi khí hậu:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "Global temperatures continue to rise due to greenhouse gas emissions."}, {"id": 2, "text": "As polar ice caps melt, sea levels threaten coastal communities."}, {"id": 3, "text": "Switching to green energy and reforestation are vital solutions."}, {"id": 4, "text": "Together, international cooperation can preserve our planet for future generations."}]}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (15, 4, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'entrepreneur', N'{"sentence_with_blank": "An innovative ___ takes financial risks to establish a new venture.", "hint": "Doanh nhân khởi nghiệp (e___________)", "phonetic": "/ˌɒn.trə.prəˈnɜːr/", "meaning_vn": "doanh nhân"}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (16, 4, N'vocab_pronounce', N'Sự đầu tư / Vốn đầu tư', N'investment', N'{"phonetic": "/ɪnˈvest.mənt/", "meaning_vn": "khoản đầu tư, sự đầu tư", "part_of_speech": "noun (Cambridge B1)", "example": "Education is the best investment you can make for your future."}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (17, 4, N'sentence_assemble', N'Chiến lược tiếp thị tốt giúp gia tăng doanh số đáng kể.', N'A good marketing strategy increases sales significantly', N'{"distractors": ["decrease", "plan", "are", "cheap", "losses"], "audio_hint": "A good marketing strategy increases sales significantly.", "notes": "Trạng từ ''significantly'' bổ nghĩa cho động từ ''increases''."}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (18, 4, N'paragraph_order', N'Sắp xếp vòng đời phát triển sản phẩm của một doanh nghiệp:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "First, the team conducts thorough market research to identify customer pain points."}, {"id": 2, "text": "Next, engineers build a minimum viable product to test core hypotheses."}, {"id": 3, "text": "Then, user feedback guides iterative refinements before the official launch."}, {"id": 4, "text": "Finally, marketing campaigns scale up to acquire market share."}]}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (19, 5, N'sentence_assemble', N'Giáo dục đóng vai trò then chốt trong việc xóa đói giảm nghèo.', N'Education plays a pivotal role in eradicating poverty', N'{"distractors": ["school", "makes", "poor", "money", "with"], "audio_hint": "Education plays a pivotal role in eradicating poverty.", "notes": "Collocation học thuật: ''play a pivotal role in''."}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (20, 5, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'unprecedented', N'{"sentence_with_blank": "The rapid advancement of quantum computing brings ___ opportunities.", "hint": "Chưa từng có tiền lệ (u____________)", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "meaning_vn": "chưa từng có"}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (21, 5, N'vocab_pronounce', N'Bền vững / Thân thiện môi trường', N'sustainable', N'{"phonetic": "/səˈsteɪ.nə.bəl/", "meaning_vn": "bền vững", "part_of_speech": "adjective (Cambridge B2)", "example": "Sustainable development balances economic growth with environmental protection."}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (22, 5, N'paragraph_order', N'Sắp xếp bài luận phân tích tác động của tự động hóa:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "It is undeniable that automation has streamlined modern industrial production."}, {"id": 2, "text": "Consequently, routine manual labor is rapidly being superseded by machines."}, {"id": 3, "text": "This paradigm shift demands substantial investments in workforce upskilling."}, {"id": 4, "text": "Ultimately, lifelong learning will be essential for future economic resilience."}]}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (23, 6, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'destination', N'{"sentence_with_blank": "Paris is one of the most popular tourist ___ in the world.", "hint": "Điểm đến du lịch (d__________)", "phonetic": "/ˌdes.tɪˈneɪ.ʃən/", "meaning_vn": "điểm đến"}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (24, 6, N'vocab_pronounce', N'Lịch trình chuyến đi', N'itinerary', N'{"phonetic": "/aɪˈtɪn.ər.ər.i/", "meaning_vn": "lịch trình chuyến đi", "part_of_speech": "noun (Cambridge B1)", "example": "Our holiday itinerary includes visiting historical museums."}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (25, 6, N'sentence_assemble', N'Du lịch mở rộng tầm nhìn và sự hiểu biết của chúng ta.', N'Traveling broadens our horizons and cultural understanding', N'{"distractors": ["narrows", "is", "sleep", "hard", "money"], "audio_hint": "Traveling broadens our horizons and cultural understanding.", "notes": "Thành ngữ ''broadens our horizons'' (mở rộng tầm mắt)."}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (26, 6, N'vocab_pronounce', N'Sự hiếu khách, lòng mến khách', N'hospitality', N'{"phonetic": "/ˌhɒs.pɪˈtæl.ə.ti/", "meaning_vn": "lòng hiếu khách", "part_of_speech": "noun (Cambridge B2)", "example": "We were touched by the warm hospitality of the locals."}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (27, 6, N'paragraph_order', N'Sắp xếp các bước chuẩn bị cho một chuyến du lịch nước ngoài:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "First, check passport validity and apply for necessary visas."}, {"id": 2, "text": "Next, book flight tickets and reserve accommodation in advance."}, {"id": 3, "text": "Then, pack lightweight clothes suitable for local weather conditions."}, {"id": 4, "text": "Finally, arrive at the international airport early for departure check-in."}]}', 5);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (28, 7, N'sentence_assemble', N'Giáo dục đóng vai trò then chốt trong việc xóa đói giảm nghèo.', N'Education plays a pivotal role in eradicating poverty', N'{"distractors": ["school", "makes", "poor", "money", "with"], "audio_hint": "Education plays a pivotal role in eradicating poverty.", "notes": "Collocation học thuật: ''play a pivotal role in''."}', 1);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (29, 7, N'fill_blank', N'Điền từ còn thiếu vào câu:', N'unprecedented', N'{"sentence_with_blank": "The rapid advancement of quantum computing brings ___ opportunities.", "hint": "Chưa từng có tiền lệ (u____________)", "phonetic": "/ʌnˈpres.ɪ.den.tɪd/", "meaning_vn": "chưa từng có"}', 2);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (30, 7, N'vocab_pronounce', N'Bền vững / Thân thiện môi trường', N'sustainable', N'{"phonetic": "/səˈsteɪ.nə.bəl/", "meaning_vn": "bền vững", "part_of_speech": "adjective (Cambridge B2)", "example": "Sustainable development balances economic growth with environmental protection."}', 3);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (31, 7, N'vocab_pronounce', N'Mô hình, khuôn mẫu chuẩn', N'paradigm', N'{"phonetic": "/ˈpær.ə.daɪm/", "meaning_vn": "mô hình mẫu, hệ hình", "part_of_speech": "noun (Cambridge C1)", "example": "A fundamental paradigm shift occurred in computer science."}', 4);
INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES (32, 7, N'paragraph_order', N'Sắp xếp bài luận phân tích tác động của tự động hóa:', N'1|2|3|4', N'{"sentences": [{"id": 1, "text": "It is undeniable that automation has streamlined modern industrial production."}, {"id": 2, "text": "Consequently, routine manual labor is rapidly being superseded by machines."}, {"id": 3, "text": "This paradigm shift demands substantial investments in workforce upskilling."}, {"id": 4, "text": "Ultimately, lifelong learning will be essential for future economic resilience."}]}', 5);
SET IDENTITY_INSERT dbo.challenges OFF;
GO

SET IDENTITY_INSERT dbo.srs_reviews ON;
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (1, 2, N'human', N'con người', N'/ˈhjuː.mən/', 2, 2.6, 6, N'2026-11-23 10:09:33', 2, 0, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (2, 2, N'recipe', N'công thức nấu ăn', N'/ˈres.ə.pi/', 0, 1.6, 0, N'2026-11-17 08:46:41', 4, 3, N'2026-11-17 09:46:41');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (3, 2, N'biodiversity', N'đa dạng sinh học', N'/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/', 0, 1.7, 0, N'2026-11-17 08:46:41', 3, 2, N'2026-11-17 09:46:41');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (4, 2, N'ingredient', N'nguyên liệu, thành phần', N'/ɪnˈɡriː.di.ənt/', 2, 2.6, 6, N'2026-11-23 09:46:41', 2, 0, N'2026-11-17 09:46:41');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (5, 2, N'algorithm', N'thuật toán', N'/ˈæl.ɡə.rɪ.ðəm/', 0, 1.76, 1, N'2026-11-18 10:09:33', 3, 2, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (6, 2, N'Artificial intelligence is changing the way we work', N'Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc.', N'', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (7, 2, N'cybersecurity', N'Bảo mật mạng / An ninh thông tin', N'/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (8, 2, N'cybersecurity', N'Bảo mật mạng / An ninh thông tin', N'/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (9, 2, N'Artificial intelligence is changing the way we work', N'Trí tuệ nhân tạo đang thay đổi cách chúng ta làm việc.', N'', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (10, 2, N'cybersecurity', N'Bảo mật mạng / An ninh thông tin', N'/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES (11, 2, N'cybersecurity', N'Bảo mật mạng / An ninh thông tin', N'/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/', 0, 1.96, 1, N'2026-11-18 10:09:33', 1, 1, N'2026-11-17 10:09:33');
SET IDENTITY_INSERT dbo.srs_reviews OFF;
GO

SET IDENTITY_INSERT dbo.cambridge_vocabulary ON;
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (1, N'recipe', N'/ˈres.ə.pi/', N'noun', N'A2', N'Food & Dining', N'công thức nấu ăn', N'a set of instructions telling you how to prepare and cook food', N'She followed her grandmother''s recipe for beef stew.', N'recipe book, follow a recipe, recipe for success');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (2, N'ingredient', N'/ɪnˈɡriː.di.ənt/', N'noun', N'B1', N'Food & Dining', N'nguyên liệu, thành phần', N'a food that is used with other foods in the preparation of a particular dish', N'Fresh vegetables are the main ingredient of this soup.', N'key ingredient, active ingredient, essential ingredient');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (3, N'nutrition', N'/njuːˈtrɪʃ.ən/', N'noun', N'B2', N'Food & Health', N'dinh dưỡng', N'the substances that you take into your body as food and the way that they influence your health', N'Good nutrition is essential for a growing child''s brain development.', N'adequate nutrition, poor nutrition, nutrition facts');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (4, N'beverage', N'/ˈbev.ər.ɪdʒ/', N'noun', N'B2', N'Food & Dining', N'đồ uống, thức uống', N'a drink of any type', N'Hot beverages include tea, coffee, and hot chocolate.', N'alcoholic beverage, refreshing beverage, beverage industry');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (5, N'delicious', N'/dɪˈlɪʃ.əs/', N'adjective', N'A1', N'Food & Dining', N'thơm ngon', N'having a very pleasant taste or smell', N'The chef prepared a delicious seafood dinner.', N'delicious meal, smell delicious, taste delicious');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (6, N'human', N'/ˈhjuː.mən/', N'noun', N'A2', N'Society & Tech', N'con người, loài người', N'a person, rather than an animal, a machine, or an alien', N'AI is designed to assist human beings in solving complex problems.', N'human nature, human rights, human intelligence');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (7, N'algorithm', N'/ˈæl.ɡə.rɪ.ðəm/', N'noun', N'B2', N'Technology', N'thuật toán', N'a set of mathematical instructions or rules used to calculate an answer to a problem', N'Search engines use sophisticated algorithms to index web pages.', N'search algorithm, computer algorithm, machine learning algorithm');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (8, N'cybersecurity', N'/ˌsaɪ.bə.sɪˈkjʊə.rə.ti/', N'noun', N'B2', N'Technology', N'an ninh mạng', N'ways of protecting computer systems and information against crime or damage', N'Companies invest millions in cybersecurity to prevent ransomware attacks.', N'cybersecurity expert, cybersecurity breach, cybersecurity protocol');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (9, N'automation', N'/ˌɔː.təˈmeɪ.ʃən/', N'noun', N'B2', N'Technology', N'sự tự động hóa', N'the use of machines and computers that can operate without needing human control', N'Automation in manufacturing has drastically increased assembly line speed.', N'industrial automation, office automation, automation process');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (10, N'innovation', N'/ˌɪn.əˈveɪ.ʃən/', N'noun', N'B2', N'Technology', N'sự đổi mới, sáng kiến', N'a new idea or method, or the use of new ideas and methods', N'Technological innovation is key to maintaining a competitive edge.', N'technological innovation, encourage innovation, product innovation');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (11, N'database', N'/ˈdeɪ.tə.beɪs/', N'noun', N'B1', N'Technology', N'cơ sở dữ liệu', N'a large amount of information stored in a computer system in such a way that it can be easily looked at or changed', N'Customer records are securely kept in a relational database.', N'relational database, database management, query a database');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (12, N'biodiversity', N'/ˌbaɪ.oʊ.daɪˈvɝː.sə.t̬i/', N'noun', N'B2', N'Environment', N'đa dạng sinh học', N'the variety of animal and plant life in a particular habitat', N'The Amazon rainforest is globally renowned for its exceptional biodiversity.', N'rich biodiversity, loss of biodiversity, preserve biodiversity');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (13, N'sustainable', N'/səˈsteɪ.nə.bəl/', N'adjective', N'B2', N'Environment', N'bền vững, thân thiện môi trường', N'causing little or no damage to the environment and therefore able to continue for a long time', N'We must adopt sustainable energy sources to protect the climate.', N'sustainable development, sustainable energy, sustainable future');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (14, N'ecosystem', N'/ˈiː.koʊˌsɪs.təm/', N'noun', N'B2', N'Environment', N'hệ sinh thái', N'all the living things in an area and the way they affect each other and the environment', N'Pollution threatens fragile marine ecosystems around coral reefs.', N'marine ecosystem, fragile ecosystem, ecosystem balance');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (15, N'extinction', N'/ɪkˈstɪŋk.ʃən/', N'noun', N'B2', N'Environment', N'sự tuyệt chủng', N'a situation in which something no longer exists', N'Many endangered species are currently facing the threat of extinction.', N'near extinction, threat of extinction, mass extinction');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (16, N'renewable', N'/rɪˈnjuː.ə.bəl/', N'adjective', N'B1', N'Environment', N'có thể tái tạo', N'energy that is produced using natural resources such as sunlight, wind, or water', N'Wind and solar power are the fastest-growing forms of renewable energy.', N'renewable energy, renewable resources, renewable power');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (17, N'entrepreneur', N'/ˌɒn.trə.prəˈnɜːr/', N'noun', N'B2', N'Business', N'doanh nhân, người khởi nghiệp', N'someone who starts their own business, especially when this involves seeing a new opportunity', N'She is an ambitious entrepreneur who launched three successful tech startups.', N'successful entrepreneur, budding entrepreneur, tech entrepreneur');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (18, N'investment', N'/ɪnˈvest.mənt/', N'noun', N'B1', N'Business', N'khoản đầu tư, sự đầu tư', N'the act of putting money, effort, time, etc. into something to make a profit or get an advantage', N'Investing in education yields the highest long-term returns.', N'foreign investment, capital investment, return on investment');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (19, N'monopoly', N'/məˈnɒp.əl.i/', N'noun', N'C1', N'Business', N'sự độc quyền', N'complete control of the supply of particular goods or services, which makes other competition impossible', N'The government passed antitrust laws to prevent corporate monopolies.', N'holding a monopoly, state monopoly, monopoly power');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (20, N'revenue', N'/ˈrev.ən.juː/', N'noun', N'B2', N'Business', N'doanh thu, ngân thu', N'the money that a government or an organization receives from business activities or taxation', N'The company reported a 25 percent surge in quarterly revenue.', N'annual revenue, generate revenue, advertising revenue');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (21, N'strategy', N'/ˈstræt.ə.dʒi/', N'noun', N'B1', N'Business', N'chiến lược', N'a detailed plan for achieving success in situations such as war, politics, business, industry, or sport', N'We need a clear marketing strategy to expand into European markets.', N'marketing strategy, corporate strategy, long-term strategy');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (22, N'pivotal', N'/ˈpɪv.ə.təl/', N'adjective', N'C1', N'Academic', N'then chốt, có tính chất quyết định', N'central and important; on which other things depend in an essential way', N'Higher education plays a pivotal role in national economic prosperity.', N'pivotal role, pivotal moment, pivotal decision');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (23, N'unprecedented', N'/ʌnˈpres.ɪ.den.tɪd/', N'adjective', N'C1', N'Academic', N'chưa từng có tiền lệ', N'never having happened or existed in the past', N'The pandemic caused unprecedented disruption to international trade.', N'unprecedented scale, unprecedented challenge, unprecedented success');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (24, N'paradigm', N'/ˈpær.ə.daɪm/', N'noun', N'C1', N'Academic', N'mô hình, khuôn mẫu chuẩn', N'a model of something, or a very clear and typical example of something', N'Quantum mechanics caused a paradigm shift in modern physics.', N'paradigm shift, dominant paradigm, cultural paradigm');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (25, N'comprehensive', N'/ˌkɒm.prɪˈhen.sɪv/', N'adjective', N'B2', N'Academic', N'toàn diện, bao quát', N'complete and including everything that is necessary', N'The university conducted a comprehensive review of the syllabus.', N'comprehensive guide, comprehensive study, comprehensive coverage');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (26, N'hypothesis', N'/haɪˈpɒθ.ə.sɪs/', N'noun', N'B2', N'Academic', N'giả thuyết', N'an idea or explanation for something that is based on known facts but has not yet been proved', N'Scientists conducted experiments to test their original hypothesis.', N'test a hypothesis, formulate a hypothesis, working hypothesis');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (27, N'itinerary', N'/aɪˈtɪn.ər.ər.i/', N'noun', N'B1', N'Travel', N'lịch trình chuyến đi', N'a detailed plan or route of a journey', N'Our travel itinerary includes guided tours of Tokyo and Kyoto.', N'travel itinerary, detailed itinerary, plan an itinerary');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (28, N'destination', N'/ˌdes.tɪˈneɪ.ʃən/', N'noun', N'B1', N'Travel', N'điểm đến', N'the place where someone is going or where something is being sent or taken', N'Da Nang is a beloved vacation destination for domestic and foreign travelers.', N'popular destination, final destination, tourist destination');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (29, N'heritage', N'/ˈher.ɪ.tɪdʒ/', N'noun', N'B2', N'Travel & Culture', N'di sản văn hóa', N'features belonging to the culture of a particular society, such as traditions, languages, or buildings', N'Hoi An ancient town is recognized as a UNESCO World Heritage site.', N'cultural heritage, national heritage, preserve heritage');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (30, N'hospitality', N'/ˌhɒs.pɪˈtæl.ə.ti/', N'noun', N'B2', N'Travel & Culture', N'sự hiếu khách, ngành khách sạn', N'the act of being friendly and welcoming to guests and visitors', N'We were deeply touched by the warm hospitality of the local villagers.', N'warm hospitality, hospitality industry, generous hospitality');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (31, N'symptom', N'/ˈsɪmp.təm/', N'noun', N'B1', N'Health', N'triệu chứng bệnh', N'any feeling of illness or physical change that is caused by a particular disease', N'Common symptoms of influenza include fever, headache, and muscle aches.', N'early symptom, mild symptom, relieve symptoms');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (32, N'resilience', N'/rɪˈzɪl.jəns/', N'noun', N'C1', N'Health & Mindset', N'sự kiên cường, khả năng hồi phục', N'the ability to recover quickly from illness, depression, or misfortune', N'Mental resilience allows athletes to perform under immense pressure.', N'build resilience, emotional resilience, psychological resilience');
INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES (33, N'vaccine', N'/ˈvæk.siːn/', N'noun', N'B2', N'Health', N'vắc xin', N'a substance that is put into the body to prevent people from catching a particular disease', N'Vaccines have effectively eliminated smallpox worldwide.', N'develop a vaccine, administer a vaccine, booster vaccine');
SET IDENTITY_INSERT dbo.cambridge_vocabulary OFF;
GO

-- ========================================================
-- HELPFUL REPORT VIEWS FOR TEACHERS & ADMINISTRATORS
-- ========================================================
GO
CREATE OR ALTER VIEW dbo.vw_WeakWordsAnalysis AS
SELECT 
    u.username,
    r.word_en,
    r.meaning_vn,
    r.phonetic,
    r.total_mistakes,
    r.total_reviews,
    CASE WHEN r.total_reviews > 0 THEN ROUND((CAST(r.total_mistakes AS FLOAT) / r.total_reviews) * 100.0, 1) ELSE 0 END AS mistake_percentage,
    r.ease_factor,
    r.interval_days,
    r.next_review_date
FROM dbo.srs_reviews r
JOIN dbo.users u ON r.user_id = u.id
WHERE (r.total_mistakes > 0 AND (CAST(r.total_mistakes AS FLOAT) / CASE WHEN r.total_reviews = 0 THEN 1 ELSE r.total_reviews END) >= 0.25)
   OR r.ease_factor < 1.9;
GO

CREATE OR ALTER VIEW dbo.vw_LevelLeaderboardOverview AS
SELECT 
    l.title AS level_title,
    l.bpm,
    u.username,
    e.score,
    e.max_combo,
    e.accuracy,
    e.created_at
FROM dbo.leaderboard_entries e
JOIN dbo.users u ON e.user_id = u.id
LEFT JOIN dbo.levels l ON e.level_id = l.id;
GO

PRINT N'✅ WordRhythmDB initialized and seeded successfully for SQL Server Management Studio!';
GO
