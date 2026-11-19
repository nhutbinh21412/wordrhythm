import json
import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Level, Challenge, GameSession, LeaderboardEntry, SRSReview, User
from ..schemas import LevelSummaryResponse, LevelDetailResponse, GameResultSubmit
from ..auth import get_current_user, require_current_user
from ..srs_engine import calculate_sm2, map_rhythm_performance_to_quality

router = APIRouter(prefix="/api/game", tags=["Game"])

@router.get("/levels", response_model=List[LevelSummaryResponse])
def get_levels(db: Session = Depends(get_db)):
    levels = db.query(Level).filter(Level.is_published == True).order_by(Level.id.asc()).all()
    results = []
    for lvl in levels:
        results.append({
            "id": lvl.id,
            "title": lvl.title,
            "theme": lvl.theme,
            "description": lvl.description,
            "boss_name": lvl.boss_name,
            "boss_title": lvl.boss_title,
            "boss_avatar": lvl.boss_avatar,
            "bpm": lvl.bpm,
            "boss_hp": lvl.boss_hp,
            "difficulty": lvl.difficulty,
            "is_published": lvl.is_published,
            "created_by_id": lvl.created_by_id,
            "challenges_count": len(lvl.challenges)
        })
    return results

@router.get("/levels/{level_id}")
def get_level_details(level_id: int, db: Session = Depends(get_db)):
    lvl = db.query(Level).filter(Level.id == level_id).first()
    if not lvl:
        raise HTTPException(status_code=404, detail="Không tìm thấy màn chơi")
    
    challenges_data = []
    for ch in lvl.challenges:
        try:
            extra = json.loads(ch.extra_data) if ch.extra_data else {}
        except Exception:
            extra = {}
        challenges_data.append({
            "id": ch.id,
            "level_id": ch.level_id,
            "challenge_type": ch.challenge_type,
            "vn_prompt": ch.vn_prompt,
            "en_target": ch.en_target,
            "extra_data": extra,
            "order_index": ch.order_index
        })

    # Randomize challenges order so every boss fight is fresh and dynamic
    import random
    random.shuffle(challenges_data)
    for idx, ch in enumerate(challenges_data):
        ch["order_index"] = idx + 1

    return {
        "id": lvl.id,
        "title": lvl.title,
        "theme": lvl.theme,
        "description": lvl.description,
        "boss_name": lvl.boss_name,
        "boss_title": lvl.boss_title,
        "boss_avatar": lvl.boss_avatar,
        "bpm": lvl.bpm,
        "boss_hp": lvl.boss_hp,
        "difficulty": lvl.difficulty,
        "is_published": lvl.is_published,
        "created_by_id": lvl.created_by_id,
        "challenges": challenges_data
    }

@router.post("/submit-session")
def submit_game_session(
    data: GameResultSubmit,
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    # 1. Save game session
    session = GameSession(
        user_id=current_user.id,
        level_id=data.level_id,
        score=data.score,
        accuracy=data.accuracy,
        max_combo=data.max_combo,
        won=data.won,
        hp_remaining=data.hp_remaining,
        completed_at=datetime.datetime.utcnow()
    )
    db.add(session)

    # 2. Add or update leaderboard
    best_entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.user_id == current_user.id,
        LeaderboardEntry.level_id == data.level_id
    ).first()

    if not best_entry:
        entry = LeaderboardEntry(
            user_id=current_user.id,
            level_id=data.level_id,
            score=data.score,
            accuracy=data.accuracy,
            max_combo=data.max_combo
        )
        db.add(entry)
    elif data.score > best_entry.score:
        best_entry.score = data.score
        best_entry.accuracy = data.accuracy
        best_entry.max_combo = max(best_entry.max_combo, data.max_combo)

    # 3. Update Spaced Repetition (SM-2) for each word tested in this battle
    if data.word_results:
        for item in data.word_results:
            quality = map_rhythm_performance_to_quality(
                item.is_correct,
                item.rhythm_rating or "PERFECT",
                item.response_time_ms or 2000
            )
            # Find existing review or create new
            review = db.query(SRSReview).filter(
                SRSReview.user_id == current_user.id,
                SRSReview.word_en.ilike(item.word_en.strip())
            ).first()

            # Avoid double-counting if reviewed in real-time just seconds ago
            if review and (datetime.datetime.utcnow() - review.last_reviewed_at).total_seconds() < 60:
                continue

            if not review:
                sm2_res = calculate_sm2(quality, 0, 2.5, 0)
                review = SRSReview(
                    user_id=current_user.id,
                    word_en=item.word_en.strip(),
                    meaning_vn=item.meaning_vn,
                    phonetic=item.phonetic or "",
                    repetition_n=sm2_res["repetition_n"],
                    ease_factor=sm2_res["ease_factor"],
                    interval_days=sm2_res["interval_days"],
                    next_review_date=sm2_res["next_review_date"],
                    total_reviews=1,
                    total_mistakes=0 if item.is_correct else 1,
                    last_reviewed_at=datetime.datetime.utcnow()
                )
                db.add(review)
            else:
                sm2_res = calculate_sm2(
                    quality,
                    review.repetition_n,
                    review.ease_factor,
                    review.interval_days
                )
                review.repetition_n = sm2_res["repetition_n"]
                review.ease_factor = sm2_res["ease_factor"]
                review.interval_days = sm2_res["interval_days"]
                review.next_review_date = sm2_res["next_review_date"]
                review.total_reviews += 1
                if not item.is_correct:
                    review.total_mistakes += 1
                review.last_reviewed_at = datetime.datetime.utcnow()

    db.commit()
    return {"status": "success", "session_id": session.id, "message": "Kết quả trận chiến đã được ghi nhận!"}
