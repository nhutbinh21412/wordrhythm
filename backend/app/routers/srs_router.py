import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import get_db
from ..models import SRSReview, User
from ..schemas import SRSReviewResponse, SRSStatsResponse, WeakWordItem, SRSSubmitRequest
from ..auth import require_current_user
from ..srs_engine import calculate_sm2, map_rhythm_performance_to_quality

router = APIRouter(prefix="/api/srs", tags=["Spaced Repetition System"])

@router.get("/stats", response_model=SRSStatsResponse)
def get_srs_stats(
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.datetime.utcnow()
    reviews = db.query(SRSReview).filter(SRSReview.user_id == current_user.id).all()
    
    total_cards = len(reviews)
    due_today = sum(1 for r in reviews if r.next_review_date <= now)
    mastered = sum(1 for r in reviews if r.repetition_n >= 3 and r.ease_factor >= 2.2)
    learning = sum(1 for r in reviews if 0 < r.repetition_n < 3)
    weak = sum(1 for r in reviews if r.total_mistakes > 0 or r.ease_factor < 2.0)

    return {
        "total_cards": total_cards,
        "due_today": due_today,
        "mastered_count": mastered,
        "learning_count": learning,
        "weak_count": weak
    }

@router.get("/due", response_model=List[SRSReviewResponse])
def get_due_reviews(
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    now = datetime.datetime.utcnow()
    due_items = db.query(SRSReview).filter(
        SRSReview.user_id == current_user.id,
        SRSReview.next_review_date <= now
    ).order_by(SRSReview.next_review_date.asc()).limit(20).all()
    return due_items

@router.get("/weak-words", response_model=List[WeakWordItem])
def get_weak_words(
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    reviews = db.query(SRSReview).filter(
        SRSReview.user_id == current_user.id
    ).all()

    weak_list = []
    for r in reviews:
        mistake_rate = r.total_mistakes / max(1, r.total_reviews)
        if r.total_mistakes > 0 or r.ease_factor < 2.0:
            weak_list.append({
                "id": r.id,
                "word_en": r.word_en,
                "meaning_vn": r.meaning_vn,
                "phonetic": r.phonetic or "",
                "mistake_rate": round(mistake_rate * 100, 1),
                "total_mistakes": r.total_mistakes,
                "total_reviews": r.total_reviews,
                "ease_factor": r.ease_factor
            })

    # Sort by highest mistake rate and most mistakes
    weak_list.sort(key=lambda x: (x["mistake_rate"], x["total_mistakes"]), reverse=True)
    return weak_list

@router.post("/review")
def review_single_word(
    data: SRSSubmitRequest,
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    quality = map_rhythm_performance_to_quality(
        data.is_correct,
        data.rhythm_rating or "PERFECT",
        data.response_time_ms or 2000
    )

    review = db.query(SRSReview).filter(
        SRSReview.user_id == current_user.id,
        SRSReview.word_en.ilike(data.word_en.strip())
    ).first()

    if not review:
        sm2_res = calculate_sm2(quality, 0, 2.5, 0)
        review = SRSReview(
            user_id=current_user.id,
            word_en=data.word_en.strip(),
            meaning_vn=data.meaning_vn,
            phonetic=data.phonetic or "",
            repetition_n=sm2_res["repetition_n"],
            ease_factor=sm2_res["ease_factor"],
            interval_days=sm2_res["interval_days"],
            next_review_date=sm2_res["next_review_date"],
            total_reviews=1,
            total_mistakes=0 if data.is_correct else 1,
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
        if not data.is_correct:
            review.total_mistakes += 1
        review.last_reviewed_at = datetime.datetime.utcnow()

    db.commit()
    db.refresh(review)

    return {
        "status": "success",
        "next_review_days": review.interval_days,
        "next_review_date": review.next_review_date.strftime("%Y-%m-%d"),
        "repetition_n": review.repetition_n,
        "ease_factor": review.ease_factor
    }

@router.get("/mistake-boss")
def get_mistake_practice_boss(
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db)
):
    """
    Dynamically generates a custom Boss level dedicated to practicing the user's weak words and mistakes!
    """
    reviews = db.query(SRSReview).filter(
        SRSReview.user_id == current_user.id,
        or_(SRSReview.total_mistakes > 0, SRSReview.ease_factor < 2.0)
    ).order_by((SRSReview.total_mistakes * 1.0 / SRSReview.total_reviews).desc()).limit(6).all()

    if not reviews:
        # Fallback if no mistakes yet
        reviews = db.query(SRSReview).filter(SRSReview.user_id == current_user.id).limit(4).all()

    challenges = []
    order = 1
    for r in reviews:
        # Create challenge alternating between vocab pronounce and fill blank
        if order % 2 == 1:
            challenges.append({
                "id": 9000 + order,
                "level_id": 9999,
                "challenge_type": "vocab_pronounce",
                "vn_prompt": r.meaning_vn,
                "en_target": r.word_en,
                "extra_data": {
                    "phonetic": r.phonetic or "",
                    "meaning_vn": r.meaning_vn,
                    "notes": f"Từ bạn đã sai {r.total_mistakes} lần. Hãy luyện phát âm và gõ đúng!"
                },
                "order_index": order
            })
        else:
            challenges.append({
                "id": 9000 + order,
                "level_id": 9999,
                "challenge_type": "fill_blank",
                "vn_prompt": f"Điền từ có nghĩa '{r.meaning_vn}'",
                "en_target": r.word_en,
                "extra_data": {
                    "sentence_with_blank": f"Remember to review the concept of ___ ({r.meaning_vn}).",
                    "hint": f"Bắt đầu bằng chữ '{r.word_en[0].upper()}'",
                    "phonetic": r.phonetic or "",
                    "meaning_vn": r.meaning_vn
                },
                "order_index": order
            })
        order += 1

    # If still empty (new user with 0 records), provide starter challenges
    if not challenges:
        challenges = [
            {
                "id": 9001,
                "level_id": 9999,
                "challenge_type": "vocab_pronounce",
                "vn_prompt": "con người",
                "en_target": "human",
                "extra_data": {"phonetic": "/ˈhjuː.mən/", "meaning_vn": "con người"},
                "order_index": 1
            },
            {
                "id": 9002,
                "level_id": 9999,
                "challenge_type": "fill_blank",
                "vn_prompt": "Điền từ còn thiếu vào câu:",
                "en_target": "apple",
                "extra_data": {
                    "sentence_with_blank": "I want to eat an ___.",
                    "hint": "Quả táo",
                    "phonetic": "/ˈæp.əl/",
                    "meaning_vn": "quả táo"
                },
                "order_index": 2
            }
        ]

    return {
        "id": 9999,
        "title": "Chế độ Luyện Sai: Shadow Phantom (Bóng Ma Ký Ức)",
        "theme": "Weak Words Mastery",
        "description": "Boss này được tạo tự động từ những từ vựng bạn hay làm sai nhất. Hãy phục thù và làm chủ chúng!",
        "boss_name": "Shadow Phantom",
        "boss_title": "Bóng Ma Sai Lầm",
        "boss_avatar": "boss_shadow",
        "bpm": 110,
        "boss_hp": max(60, len(challenges) * 25),
        "difficulty": "Custom (Adaptive)",
        "is_published": True,
        "created_by_id": None,
        "challenges": challenges
    }
