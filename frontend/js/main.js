// WordRhythm Main Game Master & App Orchestrator
class GameManager {
    constructor() {
        this.currentLevel = null;
        this.currentChallengeIndex = 0;
        this.playerHp = 3;
        this.bossHp = 100;
        this.testedWords = [];
        this.isBattleActive = false;

        this.canvasRenderer = null;
        this.challengeController = null;
    }

    async init() {
        // Initialize 2D Canvas
        this.canvasRenderer = new window.GameCanvas("game-canvas");
        this.challengeController = new window.ChallengeController(this);

        // Bind rhythm beat pulse to Canvas and HUD
        window.rhythmEngine.onBeat((beatCount, bpm) => {
            this.canvasRenderer.triggerBeat();
            this.updateHUDBeat();
        });

        this.bindNavigation();
        this.bindBattleControls();
        await this.loadCampaignLevels();
    }

    bindNavigation() {
        const navBtns = document.querySelectorAll(".nav-tab-btn");
        const views = document.querySelectorAll(".view-section");

        navBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                const targetViewId = btn.getAttribute("data-target");

                navBtns.forEach(b => b.classList.remove("active"));
                views.forEach(v => v.classList.remove("active"));

                btn.classList.add("active");
                const targetView = document.getElementById(targetViewId);
                if (targetView) targetView.classList.add("active");

                // If navigating to SRS, Vocab, Leaderboard or Editor, refresh them
                if (targetViewId === "view-srs") {
                    window.srsDashboard.init();
                } else if (targetViewId === "view-vocab") {
                    window.vocabExplorer.init();
                } else if (targetViewId === "view-leaderboard") {
                    window.leaderboardView.init();
                } else if (targetViewId === "view-editor") {
                    window.levelEditor.init();
                }
            });
        });

        // Launch Mistake Practice Boss from SRS view
        const btnMistakeBoss = document.getElementById("btn-launch-mistake-boss");
        if (btnMistakeBoss) {
            btnMistakeBoss.addEventListener("click", async () => {
                await this.startMistakeBossBattle();
            });
        }
    }

    bindBattleControls() {
        // Leave battle button
        const btnLeave = document.getElementById("btn-leave-battle");
        if (btnLeave) {
            btnLeave.addEventListener("click", () => {
                if (confirm("Bạn có muốn rời khỏi trận chiến hiện tại?")) {
                    this.endBattle(false);
                }
            });
        }

        // Restart battle button on modal
        const btnRestart = document.getElementById("btn-restart-battle");
        if (btnRestart) {
            btnRestart.addEventListener("click", () => {
                document.getElementById("battle-result-modal").classList.add("hidden");
                if (this.currentLevel) {
                    this.startBattle(this.currentLevel);
                }
            });
        }

        // Back to levels button on modal
        const btnBackLevels = document.getElementById("btn-back-levels");
        if (btnBackLevels) {
            btnBackLevels.addEventListener("click", () => {
                document.getElementById("battle-result-modal").classList.add("hidden");
                this.endBattle(false);
            });
        }
    }

    async loadCampaignLevels() {
        try {
            const levels = await window.ApiClient.getLevels();
            const grid = document.getElementById("levels-grid");
            if (!grid) return;

            grid.innerHTML = levels.map((lvl, idx) => `
                <div class="level-card animate-fade-in" data-id="${lvl.id}">
                    <div class="level-header">
                        <span class="difficulty-badge ${lvl.difficulty.toLowerCase()}">${lvl.difficulty}</span>
                        <span class="bpm-badge">⚡ ${lvl.bpm} BPM</span>
                    </div>
                    <div class="level-boss-portrait avatar-${lvl.boss_avatar}">
                        <div class="boss-emoji">${this.getAvatarEmoji(lvl.boss_avatar)}</div>
                    </div>
                    <div class="level-info">
                        <h3 class="level-title">${lvl.title}</h3>
                        <div class="boss-title">${lvl.boss_title}: <strong>${lvl.boss_name}</strong></div>
                        <p class="level-desc">${lvl.description}</p>
                    </div>
                    <div class="level-footer">
                        <span class="challenge-count">🎯 ${lvl.challenges_count} thử thách</span>
                        <button class="btn-play-level" data-id="${lvl.id}">⚔️ Chiến Boss</button>
                    </div>
                </div>
            `).join("");

            grid.querySelectorAll(".btn-play-level").forEach(btn => {
                btn.addEventListener("click", async () => {
                    const id = parseInt(btn.getAttribute("data-id"));
                    await this.loadAndStartLevel(id);
                });
            });
        } catch (e) {
            console.error("Failed to load levels:", e);
        }
    }

    getAvatarEmoji(avatar) {
        switch (avatar) {
            case "boss_chef": return "👨‍🍳";
            case "boss_cyber": return "🤖";
            case "boss_chimera": return "🐉";
            case "boss_monopoly": return "🎩";
            case "boss_examiner": return "👑";
            case "boss_shadow": return "👤";
            default: return "👾";
        }
    }

    async loadAndStartLevel(levelId) {
        try {
            const levelData = await window.ApiClient.getLevel(levelId);
            this.startBattle(levelData);
        } catch (e) {
            alert("Lỗi tải màn chơi: " + e.message);
        }
    }

    async startMistakeBossBattle() {
        try {
            const bossData = await window.ApiClient.getMistakeBoss();
            // Switch to campaign view and start
            document.querySelectorAll(".nav-tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".view-section").forEach(v => v.classList.remove("active"));
            document.getElementById("nav-tab-campaign").classList.add("active");
            document.getElementById("view-campaign").classList.add("active");

            this.startBattle(bossData);
        } catch (e) {
            alert("Lỗi khởi tạo Boss Luyện Sai: " + e.message);
        }
    }

    startBattle(level) {
        this.currentLevel = level;
        this.currentChallengeIndex = 0;
        this.playerHp = 3;
        this.bossHp = level.boss_hp || 100;
        this.testedWords = [];
        this.isBattleActive = true;

        // Switch to Battle Arena screen
        document.getElementById("level-selection-screen").classList.add("hidden");
        document.getElementById("battle-arena-screen").classList.remove("hidden");

        // Setup 2D Canvas Boss & Player
        this.canvasRenderer.setBoss(level.boss_name, level.boss_title, level.boss_avatar, this.bossHp);
        this.canvasRenderer.setPlayerHp(3);

        // Start Web Audio & Rhythm Engine
        window.rhythmEngine.start(level.bpm);

        // Update Battle HUD Labels
        document.getElementById("hud-level-title").textContent = level.title;
        document.getElementById("hud-bpm-display").textContent = `${level.bpm} BPM`;

        // Render first challenge
        this.nextChallenge();
    }

    nextChallenge() {
        if (!this.isBattleActive) return;

        if (this.currentChallengeIndex >= this.currentLevel.challenges.length) {
            // Completed all challenges!
            if (this.bossHp <= 0 || this.playerHp > 0) {
                this.handleVictory();
            }
            return;
        }

        const ch = this.currentLevel.challenges[this.currentChallengeIndex];
        this.challengeController.renderChallenge(ch);
    }

    handleCorrectHit(wordEn, meaningVn, phonetic = "") {
        // Damage boss by chunk (proportional to challenges count)
        const totalCh = Math.max(1, this.currentLevel.challenges.length);
        const damage = Math.ceil(this.currentLevel.boss_hp / totalCh);

        this.bossHp = Math.max(0, this.bossHp - damage);
        this.canvasRenderer.damageBoss(damage);

        // Record for Spaced Repetition (SM-2)
        this.testedWords.push({
            word_en: wordEn,
            meaning_vn: meaningVn,
            phonetic: phonetic,
            is_correct: true,
            rhythm_rating: "PERFECT",
            response_time_ms: 1800
        });

        // Register score
        const hitRes = window.rhythmEngine.registerManualHit(true, "PERFECT");
        this.canvasRenderer.spawnFloatingText(`+${hitRes.points} PTS! (Combo x${hitRes.combo})`, this.canvasRenderer.canvas.width / 2, 260, "#00ffcc");

        // Check if boss died
        if (this.bossHp <= 0) {
            setTimeout(() => this.handleVictory(), 600);
        } else {
            this.currentChallengeIndex++;
            setTimeout(() => this.nextChallenge(), 700);
        }
    }

    handlePlayerHurt(reasonText) {
        this.playerHp = Math.max(0, this.playerHp - 1);
        this.canvasRenderer.setPlayerHp(this.playerHp);
        this.canvasRenderer.bossAttack();
        window.soundEngine.playPlayerHurt();

        // Record failure for Spaced Repetition
        const ch = this.currentLevel.challenges[this.currentChallengeIndex];
        if (ch) {
            this.testedWords.push({
                word_en: ch.en_target,
                meaning_vn: ch.vn_prompt,
                phonetic: (ch.extra_data && ch.extra_data.phonetic) || "",
                is_correct: false,
                rhythm_rating: "MISS",
                response_time_ms: 4500
            });
        }

        window.rhythmEngine.registerManualHit(false, "MISS");

        if (this.playerHp <= 0) {
            setTimeout(() => this.handleDefeat(), 600);
        } else {
            this.currentChallengeIndex++;
            setTimeout(() => this.nextChallenge(), 1000);
        }
    }

    updateHUDBeat() {
        const comboEl = document.getElementById("hud-combo-counter");
        const scoreEl = document.getElementById("hud-score-counter");
        const accEl = document.getElementById("hud-accuracy-counter");

        if (comboEl) {
            comboEl.textContent = `${window.rhythmEngine.combo}x`;
            comboEl.classList.add("pulse-bounce");
            setTimeout(() => comboEl.classList.remove("pulse-bounce"), 120);
        }
        if (scoreEl) scoreEl.textContent = window.rhythmEngine.score.toLocaleString();
        if (accEl) accEl.textContent = `${window.rhythmEngine.getAccuracy()}%`;
    }

    async handleVictory() {
        this.isBattleActive = false;
        window.rhythmEngine.stop();
        window.soundEngine.playVictory();

        // Submit game session to backend
        const user = window.ApiClient.getUser();
        if (user) {
            try {
                await window.ApiClient.submitSession({
                    level_id: this.currentLevel.id,
                    score: window.rhythmEngine.score,
                    accuracy: window.rhythmEngine.getAccuracy(),
                    max_combo: window.rhythmEngine.maxCombo,
                    won: true,
                    hp_remaining: this.playerHp,
                    word_results: this.testedWords
                });
            } catch (e) {
                console.error("Error submitting session:", e);
            }
        }

        // Show Modal
        this.showResultModal(true);
    }

    async handleDefeat() {
        this.isBattleActive = false;
        window.rhythmEngine.stop();
        window.soundEngine.playMiss();

        const user = window.ApiClient.getUser();
        if (user) {
            try {
                await window.ApiClient.submitSession({
                    level_id: this.currentLevel.id,
                    score: window.rhythmEngine.score,
                    accuracy: window.rhythmEngine.getAccuracy(),
                    max_combo: window.rhythmEngine.maxCombo,
                    won: false,
                    hp_remaining: 0,
                    word_results: this.testedWords
                });
            } catch (e) {
                console.error("Error submitting session:", e);
            }
        }

        this.showResultModal(false);
    }

    showResultModal(won) {
        const modal = document.getElementById("battle-result-modal");
        const title = document.getElementById("result-modal-title");
        const sub = document.getElementById("result-modal-sub");
        const scoreVal = document.getElementById("res-score");
        const comboVal = document.getElementById("res-combo");
        const accVal = document.getElementById("res-acc");
        const wordsSummary = document.getElementById("res-words-summary");

        if (won) {
            title.textContent = "🏆 HẠ GỤC BOSS THÀNH CÔNG!";
            title.className = "result-title victory";
            sub.textContent = `Bạn đã đánh bại ${this.currentLevel.boss_name} theo đúng nhịp điệu!`;
        } else {
            title.textContent = "💀 BẠN ĐÃ BỊ HẠ GỤC!";
            title.className = "result-title defeat";
            sub.textContent = `Hết 3 HP! Boss ${this.currentLevel.boss_name} đã áp đảo bạn. Hãy phục thù!`;
        }

        scoreVal.textContent = window.rhythmEngine.score.toLocaleString();
        comboVal.textContent = `${window.rhythmEngine.maxCombo}x`;
        accVal.textContent = `${window.rhythmEngine.getAccuracy()}%`;

        // Render words learned and SRS feedback
        if (wordsSummary) {
            wordsSummary.innerHTML = this.testedWords.map(w => `
                <div class="result-word-tag ${w.is_correct ? 'tag-correct' : 'tag-mistake'}">
                    <span>${w.is_correct ? '✅' : '❌'} <strong>${w.word_en}</strong>: ${w.meaning_vn}</span>
                </div>
            `).join("");
        }

        modal.classList.remove("hidden");
    }

    endBattle(showConfirm = false) {
        this.isBattleActive = false;
        window.rhythmEngine.stop();
        this.challengeController.clear();

        document.getElementById("battle-arena-screen").classList.add("hidden");
        document.getElementById("level-selection-screen").classList.remove("hidden");
    }
}

// Bootstrap on DOM load
window.addEventListener("DOMContentLoaded", () => {
    window.gameManager = new GameManager();
    window.gameManager.init();
});
