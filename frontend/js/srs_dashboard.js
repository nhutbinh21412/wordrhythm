// WordRhythm Spaced Repetition (SRS) Dashboard & Weak Words Analytics
class SRSDashboard {
    constructor() {
        this.container = document.getElementById("srs-view");
        this.dueItems = [];
        this.weakWords = [];
        this.currentCardIndex = 0;
        this.isCardFlipped = false;
    }

    async init() {
        if (!window.ApiClient.getUser() && window.authManager) {
            await window.authManager.ensureSession();
        }
        await this.loadStats();
        await this.loadWeakWords();
        await this.loadDueCards();
    }

    async loadStats() {
        try {
            const stats = await window.ApiClient.getSRSStats();
            document.getElementById("stat-total-cards").textContent = stats.total_cards;
            document.getElementById("stat-due-today").textContent = stats.due_today;
            document.getElementById("stat-mastered").textContent = stats.mastered_count;
            document.getElementById("stat-weak").textContent = stats.weak_count;
        } catch (e) {
            console.error("Failed to load SRS stats:", e);
            if (String(e).includes("401") && window.authManager) {
                await window.authManager.ensureSession();
                const retryStats = await window.ApiClient.getSRSStats().catch(() => null);
                if (retryStats) {
                    document.getElementById("stat-total-cards").textContent = retryStats.total_cards;
                    document.getElementById("stat-due-today").textContent = retryStats.due_today;
                    document.getElementById("stat-mastered").textContent = retryStats.mastered_count;
                    document.getElementById("stat-weak").textContent = retryStats.weak_count;
                }
            }
        }
    }

    async loadWeakWords() {
        try {
            this.weakWords = await window.ApiClient.getWeakWords();
            const listEl = document.getElementById("weak-words-list");
            if (!listEl) return;

            if (this.weakWords.length === 0) {
                listEl.innerHTML = `
                    <div class="empty-state">
                        🎉 Tuyệt vời! Bạn chưa có từ vựng yếu nào. Hãy tiếp tục chiến boss để giữ vững phong độ!
                    </div>
                `;
                return;
            }

            listEl.innerHTML = `
                <div class="weak-words-grid">
                    ${this.weakWords.map(w => `
                        <div class="weak-word-card animate-fade-in">
                            <div class="card-header-row">
                                <span class="word-badge-error">${w.mistake_rate}% Lỗi</span>
                                <span class="ef-tag">EF: ${w.ease_factor}</span>
                            </div>
                            <div class="card-body-content">
                                <h3 class="weak-en">${w.word_en}</h3>
                                <div class="weak-phonetic">${w.phonetic || ""}</div>
                                <div class="weak-vn">${w.meaning_vn}</div>
                            </div>
                            <div class="card-footer-stats">
                                <span>Sai: ${w.total_mistakes}/${w.total_reviews} lần</span>
                                <button class="btn-sm-audio" data-word="${w.word_en}">🔊 Nghe</button>
                            </div>
                        </div>
                    `).join("")}
                </div>
            `;

            listEl.querySelectorAll(".btn-sm-audio").forEach(btn => {
                btn.addEventListener("click", () => {
                    const word = btn.getAttribute("data-word");
                    window.soundEngine.speakWord(word);
                });
            });
        } catch (e) {
            console.error("Failed to load weak words:", e);
        }
    }

    async loadDueCards() {
        try {
            this.dueItems = await window.ApiClient.getSRSDue();
            const cardArea = document.getElementById("srs-card-container");
            if (!cardArea) return;

            if (this.dueItems.length === 0) {
                cardArea.innerHTML = `
                    <div class="empty-review-banner">
                        <span class="icon">✨</span>
                        <h3>Hôm nay bạn đã ôn tập hết các từ cần ôn!</h3>
                        <p>Hệ thống Spaced Repetition (SM-2) sẽ tự động tính toán và nhắc lại khi đến chu kỳ tối ưu.</p>
                    </div>
                `;
                return;
            }

            this.currentCardIndex = 0;
            this.renderCurrentCard();
        } catch (e) {
            console.error("Failed to load due cards:", e);
        }
    }

    renderCurrentCard() {
        const cardArea = document.getElementById("srs-card-container");
        if (!cardArea) return;

        if (this.currentCardIndex >= this.dueItems.length) {
            cardArea.innerHTML = `
                <div class="empty-review-banner animate-fade-in">
                    <span class="icon">🏆</span>
                    <h3>Chúc mừng! Bạn đã hoàn thành tất cả thẻ ôn tập hôm nay!</h3>
                    <p>Bộ não của bạn đã được củng cố theo chu kỳ trí nhớ SuperMemo SM-2.</p>
                </div>
            `;
            this.loadStats();
            return;
        }

        const card = this.dueItems[this.currentCardIndex];
        this.isCardFlipped = false;

        cardArea.innerHTML = `
            <div class="srs-flashcard animate-pop" id="flashcard">
                <div class="card-progress">Thẻ ${this.currentCardIndex + 1} / ${this.dueItems.length}</div>
                
                <div class="card-front" id="card-front">
                    <div class="srs-prompt-label">Hãy nhớ lại nghĩa tiếng Việt của từ:</div>
                    <h2 class="srs-word-title">${card.word_en}</h2>
                    <div class="srs-phonetic">${card.phonetic || ""}</div>
                    <button id="btn-card-audio" class="btn-audio-listen">🔊 Nghe phát âm</button>
                    <button id="btn-flip-card" class="btn-primary mt-16">🔍 Xem Đáp Án</button>
                </div>

                <div class="card-back hidden" id="card-back">
                    <div class="srs-meaning-box">
                        <h3>${card.meaning_vn}</h3>
                        <div class="sm2-info">Chu kỳ hiện tại: ${card.interval_days} ngày | Hệ số EF: ${card.ease_factor}</div>
                    </div>

                    <div class="sm2-rating-actions">
                        <div class="rating-label">Đánh giá mức độ ghi nhớ của bạn (SM-2):</div>
                        <div class="rating-buttons-row">
                            <button class="btn-sm2 btn-rate-hard" data-grade="1">
                                <span>1</span> Khó / Quên
                            </button>
                            <button class="btn-sm2 btn-rate-good" data-grade="3">
                                <span>3</span> Tạm Được
                            </button>
                            <button class="btn-sm2 btn-rate-perfect" data-grade="5">
                                <span>5</span> Nhớ Hoàn Hảo
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById("btn-card-audio").addEventListener("click", () => {
            window.soundEngine.speakWord(card.word_en);
        });

        document.getElementById("btn-flip-card").addEventListener("click", () => {
            document.getElementById("card-front").classList.add("hidden");
            document.getElementById("card-back").classList.remove("hidden");
            window.soundEngine.speakWord(card.word_en);
        });

        cardArea.querySelectorAll(".btn-sm2").forEach(btn => {
            btn.addEventListener("click", async () => {
                const grade = parseInt(btn.getAttribute("data-grade"));
                await this.submitCardReview(card, grade);
            });
        });
    }

    async submitCardReview(card, grade) {
        try {
            await window.ApiClient.submitSRSReview({
                word_en: card.word_en,
                meaning_vn: card.meaning_vn,
                phonetic: card.phonetic,
                is_correct: grade >= 3,
                rhythm_rating: grade === 5 ? "PERFECT" : (grade >= 3 ? "GOOD" : "MISS"),
                response_time_ms: 1500
            });

            window.soundEngine.playHitPerfect();
            this.currentCardIndex++;
            this.renderCurrentCard();
            // Refresh stats and weak words live
            this.loadStats();
            this.loadWeakWords();
        } catch (e) {
            console.error("Error submitting SRS review:", e);
        }
    }
}

window.srsDashboard = new SRSDashboard();
