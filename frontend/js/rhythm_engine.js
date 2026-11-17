// WordRhythm Rhythm & Beat Synchronization Engine
class RhythmEngine {
    constructor() {
        this.bpm = 120;
        this.beatDuration = 60 / this.bpm; // in seconds
        this.startTime = 0;
        this.isRunning = false;
        this.currentBeat = 0;
        this.combo = 0;
        this.maxCombo = 0;
        this.score = 0;
        this.totalNotes = 0;
        this.hitNotes = 0;

        // Listeners for beat pulses
        this.beatListeners = [];
    }

    start(bpm = 120) {
        this.bpm = bpm;
        this.beatDuration = 60 / bpm;
        this.startTime = performance.now() / 1000;
        this.isRunning = true;
        this.combo = 0;
        this.maxCombo = 0;
        this.score = 0;
        this.totalNotes = 0;
        this.hitNotes = 0;

        // Start Web Audio beat
        window.soundEngine.startRhythmTrack(this.bpm, (beatCount) => {
            this.currentBeat = beatCount;
            this.notifyBeat(beatCount);
        });
    }

    stop() {
        this.isRunning = false;
        window.soundEngine.stopRhythmTrack();
    }

    onBeat(callback) {
        this.beatListeners.push(callback);
    }

    notifyBeat(beatCount) {
        for (const cb of this.beatListeners) {
            try {
                cb(beatCount, this.bpm);
            } catch (e) {
                console.error("Beat callback error:", e);
            }
        }
    }

    getAccuracy() {
        if (this.totalNotes === 0) return 100.0;
        return Math.round((this.hitNotes / this.totalNotes) * 1000) / 10;
    }

    getComboMultiplier() {
        if (this.combo >= 20) return 3.0;
        if (this.combo >= 10) return 2.0;
        if (this.combo >= 5) return 1.5;
        return 1.0;
    }

    // Evaluate timing accuracy of player input
    evaluateHitTiming(targetTime, hitTime = null) {
        if (!hitTime) hitTime = performance.now() / 1000;
        const diff = Math.abs(hitTime - targetTime);

        this.totalNotes++;

        if (diff <= 0.14) { // 140ms
            this.combo++;
            this.hitNotes++;
            this.maxCombo = Math.max(this.maxCombo, this.combo);
            const pts = Math.round(100 * this.getComboMultiplier());
            this.score += pts;
            window.soundEngine.playHitPerfect();
            return { rating: "PERFECT", diff, points: pts, combo: this.combo };
        } else if (diff <= 0.26) { // 260ms
            this.combo++;
            this.hitNotes++;
            this.maxCombo = Math.max(this.maxCombo, this.combo);
            const pts = Math.round(70 * this.getComboMultiplier());
            this.score += pts;
            window.soundEngine.playHitGreat();
            return { rating: "GREAT", diff, points: pts, combo: this.combo };
        } else if (diff <= 0.40) { // 400ms
            this.combo++;
            this.hitNotes++;
            this.maxCombo = Math.max(this.maxCombo, this.combo);
            const pts = Math.round(40 * this.getComboMultiplier());
            this.score += pts;
            window.soundEngine.playHitGreat();
            return { rating: "GOOD", diff, points: pts, combo: this.combo };
        } else {
            this.combo = 0;
            window.soundEngine.playMiss();
            return { rating: "MISS", diff, points: 0, combo: 0 };
        }
    }

    registerManualHit(isCorrect, qualityRating = "PERFECT") {
        this.totalNotes++;
        if (isCorrect) {
            this.combo++;
            this.hitNotes++;
            this.maxCombo = Math.max(this.maxCombo, this.combo);
            let mult = this.getComboMultiplier();
            let base = qualityRating === "PERFECT" ? 150 : 100;
            let pts = Math.round(base * mult);
            this.score += pts;
            if (qualityRating === "PERFECT") window.soundEngine.playHitPerfect();
            else window.soundEngine.playHitGreat();
            return { rating: qualityRating, points: pts, combo: this.combo };
        } else {
            this.combo = 0;
            window.soundEngine.playMiss();
            return { rating: "MISS", points: 0, combo: 0 };
        }
    }
}

window.rhythmEngine = new RhythmEngine();
