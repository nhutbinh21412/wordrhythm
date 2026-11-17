import datetime
from typing import Dict, Any

def calculate_sm2(
    quality: int,
    repetition_n: int,
    ease_factor: float,
    interval_days: int
) -> Dict[str, Any]:
    """
    Computes new repetition parameters using the SuperMemo SM-2 algorithm.
    Quality q in range [0, 5]:
      5: Perfect recall
      4: Good recall
      3: Pass / Difficult
      2: Incorrect (familiar)
      1: Incorrect (vague)
      0: Complete blackout
    """
    # Clamp quality to 0-5
    q = max(0, min(5, quality))
    
    # Calculate new ease factor
    # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ef = ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if new_ef < 1.3:
        new_ef = 1.3
        
    if q < 3:
        # Failed recall - reset repetitions
        new_n = 0
        new_interval = 1
    else:
        # Successful recall
        if repetition_n == 0:
            new_interval = 1
        elif repetition_n == 1:
            new_interval = 6
        else:
            new_interval = int(round(interval_days * new_ef))
            if new_interval <= interval_days:
                new_interval = interval_days + 1
        new_n = repetition_n + 1

    next_review = datetime.datetime.utcnow() + datetime.timedelta(days=new_interval)

    return {
        "repetition_n": new_n,
        "ease_factor": round(new_ef, 2),
        "interval_days": new_interval,
        "next_review_date": next_review
    }

def map_rhythm_performance_to_quality(is_correct: bool, rhythm_rating: str = "PERFECT", response_time_ms: int = 2000) -> int:
    """
    Maps game rhythm performance (accuracy, timing, speed) to SM-2 quality (0 - 5).
    """
    if not is_correct:
        if rhythm_rating in ["GOOD", "GREAT"]:
            return 2  # Near miss
        elif rhythm_rating == "MISS" and response_time_ms < 5000:
            return 1  # Vague recall
        else:
            return 0  # Blackout / timeout

    # If correct:
    if rhythm_rating == "PERFECT" or response_time_ms <= 1500:
        return 5
    elif rhythm_rating == "GREAT" or response_time_ms <= 3000:
        return 4
    else:
        return 3
