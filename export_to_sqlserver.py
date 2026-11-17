import json
from backend.app.database import SessionLocal
from backend.app.models import User, Level, Challenge, SRSReview, GameSession, LeaderboardEntry
from backend.app.routers.cambridge_router import CAMBRIDGE_DICT

def escape_sql(val):
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "1" if val else "0"
    if isinstance(val, (int, float)):
        return str(val)
    # String
    s = str(val).replace("'", "''")
    return f"N'{s}'"

def generate_tsql():
    db = SessionLocal()

    sql = []
    sql.append("-- ========================================================")
    sql.append("-- WordRhythm Database Creation & Seed Script for Microsoft SQL Server")
    sql.append("-- Target: SQL Server Management Studio (SSMS) 2016 / 2019 / 2022 / Azure SQL")
    sql.append("-- Character Encoding: UTF-8 / NCHAR / NVARCHAR")
    sql.append("-- ========================================================\n")
    
    sql.append("USE master;")
    sql.append("GO\n")
    sql.append("IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'WordRhythmDB')")
    sql.append("BEGIN")
    sql.append("    CREATE DATABASE WordRhythmDB COLLATE Latin1_General_100_CI_AS_SC_UTF8;")
    sql.append("END")
    sql.append("GO\n")
    sql.append("USE WordRhythmDB;")
    sql.append("GO\n")

    # 1. Drop existing tables if re-running
    sql.append("-- Drop foreign keys & tables if already exist")
    sql.append("IF OBJECT_ID('dbo.leaderboard_entries', 'U') IS NOT NULL DROP TABLE dbo.leaderboard_entries;")
    sql.append("IF OBJECT_ID('dbo.game_sessions', 'U') IS NOT NULL DROP TABLE dbo.game_sessions;")
    sql.append("IF OBJECT_ID('dbo.srs_reviews', 'U') IS NOT NULL DROP TABLE dbo.srs_reviews;")
    sql.append("IF OBJECT_ID('dbo.challenges', 'U') IS NOT NULL DROP TABLE dbo.challenges;")
    sql.append("IF OBJECT_ID('dbo.levels', 'U') IS NOT NULL DROP TABLE dbo.levels;")
    sql.append("IF OBJECT_ID('dbo.cambridge_vocabulary', 'U') IS NOT NULL DROP TABLE dbo.cambridge_vocabulary;")
    sql.append("IF OBJECT_ID('dbo.users', 'U') IS NOT NULL DROP TABLE dbo.users;")
    sql.append("GO\n")

    # 2. Table: users
    sql.append("-- Table: users")
    sql.append("""CREATE TABLE dbo.users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    email NVARCHAR(100) NOT NULL UNIQUE,
    hashed_password NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL DEFAULT N'student',
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO""")

    # 3. Table: levels
    sql.append("-- Table: levels")
    sql.append("""CREATE TABLE dbo.levels (
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
GO""")

    # 4. Table: challenges
    sql.append("-- Table: challenges")
    sql.append("""CREATE TABLE dbo.challenges (
    id INT IDENTITY(1,1) PRIMARY KEY,
    level_id INT NOT NULL,
    challenge_type NVARCHAR(40) NOT NULL, -- sentence_assemble, fill_blank, vocab_pronounce, paragraph_order
    vn_prompt NVARCHAR(MAX) NOT NULL,
    en_target NVARCHAR(MAX) NOT NULL,
    extra_data NVARCHAR(MAX) NULL, -- JSON formatted data
    order_index INT NOT NULL DEFAULT 0,
    CONSTRAINT FK_challenges_level FOREIGN KEY (level_id) REFERENCES dbo.levels(id) ON DELETE CASCADE
);
GO""")

    # 5. Table: srs_reviews
    sql.append("-- Table: srs_reviews (SuperMemo SM-2 Engine Data)")
    sql.append("""CREATE TABLE dbo.srs_reviews (
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
GO""")

    # 6. Table: game_sessions
    sql.append("-- Table: game_sessions")
    sql.append("""CREATE TABLE dbo.game_sessions (
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
GO""")

    # 7. Table: leaderboard_entries
    sql.append("-- Table: leaderboard_entries")
    sql.append("""CREATE TABLE dbo.leaderboard_entries (
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
GO""")

    # 8. Table: cambridge_vocabulary
    sql.append("-- Table: cambridge_vocabulary")
    sql.append("""CREATE TABLE dbo.cambridge_vocabulary (
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
GO""")

    # ==========================================
    # INSERT SEED DATA
    # ==========================================
    sql.append("\n-- ==========================================")
    sql.append("-- SEED DATA INSERTION")
    sql.append("-- ==========================================\n")

    # Users
    users = db.query(User).order_by(User.id).all()
    if users:
        sql.append("SET IDENTITY_INSERT dbo.users ON;")
        for u in users:
            sql.append(f"INSERT INTO dbo.users (id, username, email, hashed_password, role, created_at) VALUES ({u.id}, {escape_sql(u.username)}, {escape_sql(u.email)}, {escape_sql(u.hashed_password)}, {escape_sql(u.role)}, {escape_sql(u.created_at.strftime('%Y-%m-%d %H:%M:%S'))});")
        sql.append("SET IDENTITY_INSERT dbo.users OFF;")
        sql.append("GO\n")

    # Levels
    levels = db.query(Level).order_by(Level.id).all()
    if levels:
        sql.append("SET IDENTITY_INSERT dbo.levels ON;")
        for l in levels:
            sql.append(f"INSERT INTO dbo.levels (id, title, theme, description, boss_name, boss_title, boss_avatar, bpm, boss_hp, difficulty, is_published, created_by_id, created_at) VALUES ({l.id}, {escape_sql(l.title)}, {escape_sql(l.theme)}, {escape_sql(l.description)}, {escape_sql(l.boss_name)}, {escape_sql(l.boss_title)}, {escape_sql(l.boss_avatar)}, {l.bpm}, {l.boss_hp}, {escape_sql(l.difficulty)}, {1 if l.is_published else 0}, {l.created_by_id or 'NULL'}, {escape_sql(l.created_at.strftime('%Y-%m-%d %H:%M:%S'))});")
        sql.append("SET IDENTITY_INSERT dbo.levels OFF;")
        sql.append("GO\n")

    # Challenges
    challenges = db.query(Challenge).order_by(Challenge.id).all()
    if challenges:
        sql.append("SET IDENTITY_INSERT dbo.challenges ON;")
        for c in challenges:
            sql.append(f"INSERT INTO dbo.challenges (id, level_id, challenge_type, vn_prompt, en_target, extra_data, order_index) VALUES ({c.id}, {c.level_id}, {escape_sql(c.challenge_type)}, {escape_sql(c.vn_prompt)}, {escape_sql(c.en_target)}, {escape_sql(c.extra_data)}, {c.order_index});")
        sql.append("SET IDENTITY_INSERT dbo.challenges OFF;")
        sql.append("GO\n")

    # SRS Reviews
    reviews = db.query(SRSReview).order_by(SRSReview.id).all()
    if reviews:
        sql.append("SET IDENTITY_INSERT dbo.srs_reviews ON;")
        for r in reviews:
            sql.append(f"INSERT INTO dbo.srs_reviews (id, user_id, word_en, meaning_vn, phonetic, repetition_n, ease_factor, interval_days, next_review_date, total_reviews, total_mistakes, last_reviewed_at) VALUES ({r.id}, {r.user_id}, {escape_sql(r.word_en)}, {escape_sql(r.meaning_vn)}, {escape_sql(r.phonetic)}, {r.repetition_n}, {r.ease_factor}, {r.interval_days}, {escape_sql(r.next_review_date.strftime('%Y-%m-%d %H:%M:%S'))}, {r.total_reviews}, {r.total_mistakes}, {escape_sql(r.last_reviewed_at.strftime('%Y-%m-%d %H:%M:%S'))});")
        sql.append("SET IDENTITY_INSERT dbo.srs_reviews OFF;")
        sql.append("GO\n")

    # Cambridge Dictionary Table
    sql.append("SET IDENTITY_INSERT dbo.cambridge_vocabulary ON;")
    c_id = 1
    for k, v in CAMBRIDGE_DICT.items():
        colls = ", ".join(v.get("collocations", []))
        sql.append(f"INSERT INTO dbo.cambridge_vocabulary (id, word, phonetic, part_of_speech, cefr_level, topic, meaning_vn, definition, example, collocations) VALUES ({c_id}, {escape_sql(v['word'])}, {escape_sql(v['phonetic'])}, {escape_sql(v['pos'])}, {escape_sql(v['cefr'])}, {escape_sql(v.get('topic', 'General'))}, {escape_sql(v['meaning_vn'])}, {escape_sql(v['definition'])}, {escape_sql(v['example'])}, {escape_sql(colls)});")
        c_id += 1
    sql.append("SET IDENTITY_INSERT dbo.cambridge_vocabulary OFF;")
    sql.append("GO\n")

    # Views & Stored Procedures for Analysis
    sql.append("""-- ========================================================
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
""")

    db.close()
    return "\n".join(sql)

if __name__ == "__main__":
    content = generate_tsql()
    out_path = "database/wordrhythm_sqlserver.sql"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path} with {len(content)} characters.")
