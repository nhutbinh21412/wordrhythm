from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import LeaderboardEntry, User, Level
from ..schemas import LeaderboardItemResponse

router = APIRouter(prefix="/api/leaderboard", tags=["Leaderboard"])

@router.get("/global")
def get_global_leaderboard(db: Session = Depends(get_db)):
    # Group by user to get top total score
    entries = db.query(LeaderboardEntry).order_by(LeaderboardEntry.score.desc()).limit(20).all()
    results = []
    for e in entries:
        results.append({
            "id": e.id,
            "username": e.user.username if e.user else "Anonymous",
            "score": e.score,
            "accuracy": round(e.accuracy, 1),
            "max_combo": e.max_combo,
            "level_title": e.level.title if e.level else "All Levels",
            "created_at": e.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return results

@router.get("/level/{level_id}")
def get_level_leaderboard(level_id: int, db: Session = Depends(get_db)):
    entries = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.level_id == level_id
    ).order_by(LeaderboardEntry.score.desc()).limit(15).all()

    results = []
    for e in entries:
        results.append({
            "id": e.id,
            "username": e.user.username if e.user else "Anonymous",
            "score": e.score,
            "accuracy": round(e.accuracy, 1),
            "max_combo": e.max_combo,
            "level_title": e.level.title if e.level else f"Level #{level_id}",
            "created_at": e.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return results
