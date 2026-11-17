import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Level, Challenge, User
from ..schemas import LevelCreate, LevelUpdate, ChallengeCreate, LevelDetailResponse
from ..auth import require_teacher

router = APIRouter(prefix="/api/editor", tags=["Teacher Level Editor"])

@router.get("/levels")
def get_teacher_levels(
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    levels = db.query(Level).filter(Level.created_by_id == current_user.id).order_by(Level.id.desc()).all()
    results = []
    for lvl in levels:
        results.append({
            "id": lvl.id,
            "title": lvl.title,
            "theme": lvl.theme,
            "boss_name": lvl.boss_name,
            "boss_avatar": lvl.boss_avatar,
            "bpm": lvl.bpm,
            "boss_hp": lvl.boss_hp,
            "difficulty": lvl.difficulty,
            "is_published": lvl.is_published,
            "challenges_count": len(lvl.challenges),
            "created_at": lvl.created_at.strftime("%Y-%m-%d %H:%M")
        })
    return results

@router.post("/levels")
def create_level(
    level_data: LevelCreate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    new_lvl = Level(
        title=level_data.title,
        theme=level_data.theme,
        description=level_data.description or "",
        boss_name=level_data.boss_name,
        boss_title=level_data.boss_title or "Guardian",
        boss_avatar=level_data.boss_avatar or "boss_dragon",
        bpm=level_data.bpm or 120,
        boss_hp=level_data.boss_hp or 100,
        difficulty=level_data.difficulty or "Medium",
        is_published=level_data.is_published,
        created_by_id=current_user.id
    )
    db.add(new_lvl)
    db.commit()
    db.refresh(new_lvl)

    # Add challenges if provided
    if level_data.challenges:
        for idx, ch_data in enumerate(level_data.challenges):
            ch = Challenge(
                level_id=new_lvl.id,
                challenge_type=ch_data.challenge_type,
                vn_prompt=ch_data.vn_prompt,
                en_target=ch_data.en_target,
                extra_data=json.dumps(ch_data.extra_data or {}, ensure_ascii=False),
                order_index=idx + 1
            )
            db.add(ch)
        db.commit()

    return {"status": "success", "level_id": new_lvl.id, "message": "Tạo màn chơi thành công!"}

@router.put("/levels/{level_id}")
def update_level(
    level_id: int,
    data: LevelUpdate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    lvl = db.query(Level).filter(Level.id == level_id).first()
    if not lvl:
        raise HTTPException(status_code=404, detail="Không tìm thấy màn chơi")
    if lvl.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền chỉnh sửa màn chơi này")

    for key, val in data.dict(exclude_unset=True).items():
        setattr(lvl, key, val)

    db.commit()
    return {"status": "success", "message": "Cập nhật màn chơi thành công!"}

@router.delete("/levels/{level_id}")
def delete_level(
    level_id: int,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    lvl = db.query(Level).filter(Level.id == level_id).first()
    if not lvl:
        raise HTTPException(status_code=404, detail="Không tìm thấy màn chơi")
    if lvl.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Bạn không có quyền xóa màn chơi này")

    db.delete(lvl)
    db.commit()
    return {"status": "success", "message": "Xóa màn chơi thành công!"}

@router.post("/levels/{level_id}/challenges")
def add_challenge(
    level_id: int,
    ch_data: ChallengeCreate,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    lvl = db.query(Level).filter(Level.id == level_id).first()
    if not lvl:
        raise HTTPException(status_code=404, detail="Không tìm thấy màn chơi")
    if lvl.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền thêm câu hỏi vào màn chơi này")

    ch = Challenge(
        level_id=level_id,
        challenge_type=ch_data.challenge_type,
        vn_prompt=ch_data.vn_prompt,
        en_target=ch_data.en_target,
        extra_data=json.dumps(ch_data.extra_data or {}, ensure_ascii=False),
        order_index=ch_data.order_index or (len(lvl.challenges) + 1)
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return {"status": "success", "challenge_id": ch.id, "message": "Thêm thử thách thành công!"}

@router.delete("/challenges/{challenge_id}")
def delete_challenge(
    challenge_id: int,
    current_user: User = Depends(require_teacher),
    db: Session = Depends(get_db)
):
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(status_code=404, detail="Không tìm thấy thử thách")
    if ch.level.created_by_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền xóa thử thách này")

    db.delete(ch)
    db.commit()
    return {"status": "success", "message": "Đã xóa thử thách!"}
