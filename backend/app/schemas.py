import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "student"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Challenge Schemas
class ChallengeBase(BaseModel):
    challenge_type: str # sentence_assemble, fill_blank, vocab_pronounce, paragraph_order
    vn_prompt: str
    en_target: str
    extra_data: Optional[Dict[str, Any]] = {}
    order_index: Optional[int] = 0

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeResponse(BaseModel):
    id: int
    level_id: int
    challenge_type: str
    vn_prompt: str
    en_target: str
    extra_data: Dict[str, Any]
    order_index: int

    class Config:
        from_attributes = True

# Level Schemas
class LevelBase(BaseModel):
    title: str
    theme: str
    description: Optional[str] = ""
    boss_name: str
    boss_title: Optional[str] = "Guardian"
    boss_avatar: Optional[str] = "boss_dragon"
    bpm: Optional[int] = 120
    boss_hp: Optional[int] = 100
    difficulty: Optional[str] = "Medium"
    is_published: Optional[bool] = True

class LevelCreate(LevelBase):
    challenges: Optional[List[ChallengeBase]] = []

class LevelUpdate(BaseModel):
    title: Optional[str] = None
    theme: Optional[str] = None
    description: Optional[str] = None
    boss_name: Optional[str] = None
    boss_title: Optional[str] = None
    boss_avatar: Optional[str] = None
    bpm: Optional[int] = None
    boss_hp: Optional[int] = None
    difficulty: Optional[str] = None
    is_published: Optional[bool] = None

class LevelSummaryResponse(BaseModel):
    id: int
    title: str
    theme: str
    description: str
    boss_name: str
    boss_title: str
    boss_avatar: str
    bpm: int
    boss_hp: int
    difficulty: str
    is_published: bool
    created_by_id: Optional[int]
    challenges_count: int

    class Config:
        from_attributes = True

class LevelDetailResponse(BaseModel):
    id: int
    title: str
    theme: str
    description: str
    boss_name: str
    boss_title: str
    boss_avatar: str
    bpm: int
    boss_hp: int
    difficulty: str
    is_published: bool
    created_by_id: Optional[int]
    challenges: List[ChallengeResponse]

    class Config:
        from_attributes = True

# SRS Schemas
class SRSSubmitRequest(BaseModel):
    word_en: str
    meaning_vn: str
    phonetic: Optional[str] = ""
    is_correct: bool
    response_time_ms: Optional[int] = 2000
    rhythm_rating: Optional[str] = "PERFECT" # PERFECT, GREAT, GOOD, MISS

class SRSReviewResponse(BaseModel):
    id: int
    word_en: str
    meaning_vn: str
    phonetic: str
    repetition_n: int
    ease_factor: float
    interval_days: int
    next_review_date: datetime.datetime
    total_reviews: int
    total_mistakes: int

    class Config:
        from_attributes = True

class SRSStatsResponse(BaseModel):
    total_cards: int
    due_today: int
    mastered_count: int
    learning_count: int
    weak_count: int

class WeakWordItem(BaseModel):
    id: int
    word_en: str
    meaning_vn: str
    phonetic: str
    mistake_rate: float
    total_mistakes: int
    total_reviews: int
    ease_factor: float

# Game Session & Leaderboard Schemas
class GameResultSubmit(BaseModel):
    level_id: int
    score: int
    accuracy: float
    max_combo: int
    won: bool
    hp_remaining: int
    word_results: Optional[List[SRSSubmitRequest]] = []

class LeaderboardItemResponse(BaseModel):
    id: int
    username: str
    score: int
    accuracy: float
    max_combo: int
    level_title: Optional[str] = "All Levels"
    created_at: datetime.datetime

    class Config:
        from_attributes = True
