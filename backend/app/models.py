import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student", nullable=False) # 'student' or 'teacher' or 'admin'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    created_levels = relationship("Level", back_populates="creator")
    srs_reviews = relationship("SRSReview", back_populates="user")
    game_sessions = relationship("GameSession", back_populates="user")
    leaderboard_entries = relationship("LeaderboardEntry", back_populates="user")

class Level(Base):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    theme = Column(String(80), nullable=False)
    description = Column(Text, default="")
    boss_name = Column(String(80), nullable=False)
    boss_title = Column(String(100), default="Guardian")
    boss_avatar = Column(String(50), default="boss_dragon") # boss_dragon, boss_cyber, boss_golem, boss_phantom, boss_examiner
    bpm = Column(Integer, default=120)
    boss_hp = Column(Integer, default=100)
    difficulty = Column(String(20), default="Medium") # Easy, Medium, Hard
    is_published = Column(Boolean, default=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship("User", back_populates="created_levels")
    challenges = relationship("Challenge", back_populates="level", cascade="all, delete-orphan", order_by="Challenge.order_index")
    sessions = relationship("GameSession", back_populates="level")
    leaderboards = relationship("LeaderboardEntry", back_populates="level")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    challenge_type = Column(String(40), nullable=False) # sentence_assemble, fill_blank, vocab_pronounce, paragraph_order
    vn_prompt = Column(Text, nullable=False)
    en_target = Column(Text, nullable=False)
    extra_data = Column(Text, default="{}") # JSON containing distractors, blanks, phonetic, hints, paragraph sentences
    order_index = Column(Integer, default=0)

    level = relationship("Level", back_populates="challenges")

class SRSReview(Base):
    __tablename__ = "srs_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_en = Column(String(150), nullable=False, index=True)
    meaning_vn = Column(String(255), nullable=False)
    phonetic = Column(String(100), default="")
    repetition_n = Column(Integer, default=0) # repetition number (n)
    ease_factor = Column(Float, default=2.5) # SM-2 EF factor (initially 2.5)
    interval_days = Column(Integer, default=0) # Interval (days)
    next_review_date = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    total_reviews = Column(Integer, default=0)
    total_mistakes = Column(Integer, default=0)
    last_reviewed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="srs_reviews")

class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    score = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    max_combo = Column(Integer, default=0)
    won = Column(Boolean, default=False)
    hp_remaining = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="game_sessions")
    level = relationship("Level", back_populates="sessions")

class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=True) # None for overall
    score = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    max_combo = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="leaderboard_entries")
    level = relationship("Level", back_populates="leaderboards")
