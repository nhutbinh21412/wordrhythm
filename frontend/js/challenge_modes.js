// WordRhythm Challenge Modes Engine (4 Boss Challenge Types)
class ChallengeController {
    constructor(gameManager) {
        this.game = gameManager;
        this.container = document.getElementById("challenge-area");
        this.currentChallenge = null;
        this.timer = null;
        this.beatTimerBeats = 16; // 16 beats countdown per challenge
        this.beatsRemaining = 16;
        this.assembledWords = [];
        this.expectedWords = [];
        this.paragraphOrder = [];
    }

    renderChallenge(challenge) {
        this.currentChallenge = challenge;
        this.clear();
        this.startBeatTimer(this.game.currentLevel.bpm);

        switch (challenge.challenge_type) {
            case "sentence_assemble":
                this.renderSentenceAssemble(challenge);
                break;
            case "fill_blank":
                this.renderFillBlank(challenge);
                break;
            case "vocab_pronounce":
                this.renderVocabPronounce(challenge);
                break;
            case "paragraph_order":
                this.renderParagraphOrder(challenge);
                break;
            default:
                console.error("Unknown challenge type:", challenge.challenge_type);
        }
    }

    clear() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        this.container.innerHTML = "";
    }

    startBeatTimer(bpm) {
        this.beatsRemaining = 24; // 24 beats to answer
        const beatMs = (60 / bpm) * 1000;

        this.timer = setInterval(() => {
            this.beatsRemaining--;
            const timerBar = document.getElementById("rhythm-countdown-fill");
            const timerText = document.getElementById("rhythm-countdown-text");
            if (timerBar) {
                const percent = Math.max(0, (this.beatsRemaining / 24) * 100);
                timerBar.style.width = `${percent}%`;
            }
            if (timerText) {
                timerText.textContent = `⏳ Nhịp đếm ngược: ${this.beatsRemaining} beats`;
            }

            if (this.beatsRemaining <= 0) {
                clearInterval(this.timer);
                this.timer = null;
                this.handleTimeout();
            }
        }, beatMs);
    }

    handleTimeout() {
        window.soundEngine.playMiss();
        this.game.handlePlayerHurt("Hết giờ theo nhịp! Boss phản công!");
    }

    // ==========================================
    // 1. THỬ THÁCH 1: GHÉP CÂU THEO NHỊP
    // ==========================================
    renderSentenceAssemble(ch) {
        const targetWords = ch.en_target.trim().split(/\s+/);
        this.expectedWords = targetWords;
        this.assembledWords = [];

        // Mix in distractors
        const distractors = (ch.extra_data && ch.extra_data.distractors) || ["not", "also", "very"];
        const pool = [...targetWords, ...distractors];
        // Shuffle pool
        pool.sort(() => Math.random() - 0.5);

        this.container.innerHTML = `
            <div class="challenge-card animate-fade-in">
                <div class="challenge-badge">🎯 Thử Thách 1: Ghép Câu Theo Nhịp</div>
                <div class="vn-prompt-banner">
                    <span class="prompt-icon">🗣️ Boss ra đề:</span>
                    <h3 class="vn-prompt-text">"${ch.vn_prompt}"</h3>
                </div>

                <div class="assembled-sentence-box" id="assembled-box">
                    <span class="placeholder-text">Chọn các từ rơi theo nhịp bên dưới để ghép thành câu...</span>
                </div>

                <div class="rhythm-countdown-container">
                    <div class="rhythm-countdown-bar">
                        <div id="rhythm-countdown-fill" class="rhythm-countdown-fill" style="width: 100%;"></div>
                    </div>
                    <span id="rhythm-countdown-text" class="rhythm-countdown-text">⏳ Nhịp đếm: 24 beats</span>
                </div>

                <div class="word-rhythm-tracks" id="word-tracks">
                    ${pool.map((w, idx) => `
                        <button class="rhythm-word-btn" data-word="${w}" data-idx="${idx}">
                            <span class="key-hint">${idx + 1}</span>
                            <span class="word-label">${w}</span>
                        </button>
                    `).join("")}
                </div>

                <div class="action-buttons-row">
                    <button class="btn-secondary" id="btn-reset-words">🔄 Xếp lại</button>
                    <button class="btn-primary" id="btn-submit-sentence">⚡ Tung Đòn Tấn Công</button>
                </div>
            </div>
        `;

        // Event Listeners for Word Buttons
        const buttons = this.container.querySelectorAll(".rhythm-word-btn");
        buttons.forEach(btn => {
            btn.addEventListener("click", () => {
                const word = btn.getAttribute("data-word");
                btn.classList.add("used");
                btn.disabled = true;
                this.addWordToSentence(word, btn);
            });
        });

        // Reset
        document.getElementById("btn-reset-words").addEventListener("click", () => {
            this.assembledWords = [];
            buttons.forEach(b => {
                b.classList.remove("used");
                b.disabled = false;
            });
            this.updateAssembledBox();
        });

        // Submit Sentence
        document.getElementById("btn-submit-sentence").addEventListener("click", () => {
            this.checkSentenceResult();
        });

        // Keyboard hotkeys 1-9
        this.keyListener = (e) => {
            const num = parseInt(e.key);
            if (!isNaN(num) && num >= 1 && num <= buttons.length) {
                const targetBtn = buttons[num - 1];
                if (targetBtn && !targetBtn.disabled) {
                    targetBtn.click();
                }
            } else if (e.key === "Enter") {
                this.checkSentenceResult();
            }
        };
        window.addEventListener("keydown", this.keyListener);
    }

    addWordToSentence(word, btnRef) {
        this.assembledWords.push({ word, btnRef });
        this.updateAssembledBox();
        window.soundEngine.playHitGreat();
    }

    updateAssembledBox() {
        const box = document.getElementById("assembled-box");
        if (!box) return;
        if (this.assembledWords.length === 0) {
            box.innerHTML = `<span class="placeholder-text">Chọn các từ rơi theo nhịp bên dưới để ghép thành câu...</span>`;
        } else {
            box.innerHTML = this.assembledWords.map((item, idx) => `
                <span class="assembled-tag animate-pop" data-tag-idx="${idx}">
                    ${item.word}
                    <span class="remove-x">×</span>
                </span>
            `).join(" ");

            // Allow clicking tag to remove
            box.querySelectorAll(".assembled-tag").forEach(tag => {
                tag.addEventListener("click", () => {
                    const idx = parseInt(tag.getAttribute("data-tag-idx"));
                    const removed = this.assembledWords.splice(idx, 1)[0];
                    if (removed && removed.btnRef) {
                        removed.btnRef.classList.remove("used");
                        removed.btnRef.disabled = false;
                    }
                    this.updateAssembledBox();
                });
            });
        }
    }

    checkSentenceResult() {
        if (this.timer) clearInterval(this.timer);
        if (this.keyListener) window.removeEventListener("keydown", this.keyListener);

        const currentSentence = this.assembledWords.map(w => w.word).join(" ").trim().toLowerCase();
        const expectedSentence = this.expectedWords.join(" ").trim().toLowerCase();

        const isCorrect = currentSentence === expectedSentence;
        if (isCorrect) {
            window.soundEngine.playHitPerfect();
            this.game.handleCorrectHit(this.currentChallenge.en_target, this.currentChallenge.vn_prompt);
        } else {
            window.soundEngine.playMiss();
            this.game.handlePlayerHurt(`Sai thứ tự! Đáp án đúng: "${this.currentChallenge.en_target}"`);
        }
    }

    // ==========================================
    // 2. THỬ THÁCH 2: CÂU KHUYẾT THEO NHỊP
    // ==========================================
    renderFillBlank(ch) {
        const extra = ch.extra_data || {};
        const sentenceWithBlank = extra.sentence_with_blank || `Sentence missing ___ word.`;
        const hint = extra.hint || "";
        const phonetic = extra.phonetic || "";

        this.container.innerHTML = `
            <div class="challenge-card animate-fade-in">
                <div class="challenge-badge">📝 Thử Thách 2: Điền Từ Khuyết Vào Câu</div>
                <div class="vn-prompt-banner">
                    <span class="prompt-icon">⚔️ Câu hỏi:</span>
                    <h3 class="blank-sentence-display">${sentenceWithBlank.replace("___", `<span class="blank-highlight">___</span>`)}</h3>
                </div>

                <div class="hint-card">
                    <span class="hint-title">💡 Gợi ý Cambridge:</span> ${hint}
                    ${phonetic ? `<span class="phonetic-tag">${phonetic}</span>` : ""}
                </div>

                <div class="rhythm-countdown-container">
                    <div class="rhythm-countdown-bar">
                        <div id="rhythm-countdown-fill" class="rhythm-countdown-fill" style="width: 100%;"></div>
                    </div>
                    <span id="rhythm-countdown-text" class="rhythm-countdown-text">⏳ Nhịp đếm: 24 beats</span>
                </div>

                <div class="fill-input-wrapper">
                    <input type="text" id="blank-input" class="rhythm-text-input" placeholder="Gõ từ còn thiếu tại đây..." autocomplete="off" autofocus />
                    <button id="btn-submit-blank" class="btn-primary">⚡ Xác Nhận (Enter)</button>
                </div>
            </div>
        `;

        const input = document.getElementById("blank-input");
        setTimeout(() => input.focus(), 100);

        const submit = () => {
            const val = input.value.trim().toLowerCase();
            const target = ch.en_target.trim().toLowerCase();
            if (this.timer) clearInterval(this.timer);

            if (val === target) {
                window.soundEngine.playHitPerfect();
                this.game.handleCorrectHit(ch.en_target, extra.meaning_vn || ch.vn_prompt, phonetic);
            } else {
                window.soundEngine.playMiss();
                this.game.handlePlayerHurt(`Sai từ! Từ đúng là: "${ch.en_target}" (${phonetic})`);
            }
        };

        document.getElementById("btn-submit-blank").addEventListener("click", submit);
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") submit();
        });
    }

    // ==========================================
    // 3. THỬ THÁCH 3: TỪ VỰNG THEO CHỦ ĐỀ & PHÁT ÂM
    // ==========================================
    renderVocabPronounce(ch) {
        const extra = ch.extra_data || {};
        const phonetic = extra.phonetic || "";
        const targetWord = ch.en_target.trim();

        this.container.innerHTML = `
            <div class="challenge-card animate-fade-in">
                <div class="challenge-badge">🎧 Thử Thách 3: Từ Vựng Theo Chủ Đề & Phát Âm</div>
                <div class="vn-prompt-banner">
                    <span class="prompt-icon">🇻🇳 Nghĩa tiếng Việt:</span>
                    <h2 class="vn-vocab-display">${ch.vn_prompt}</h2>
                </div>

                <div class="audio-pronounce-box">
                    <button id="btn-play-audio" class="btn-audio-listen pulse-btn">
                        🔊 Nghe Phát Âm Lại (Phím Space)
                    </button>
                    ${phonetic ? `<span class="phonetic-badge">${phonetic}</span>` : ""}
                </div>

                <div class="rhythm-countdown-container">
                    <div class="rhythm-countdown-bar">
                        <div id="rhythm-countdown-fill" class="rhythm-countdown-fill" style="width: 100%;"></div>
                    </div>
                    <span id="rhythm-countdown-text" class="rhythm-countdown-text">⏳ Nhịp đếm: 24 beats</span>
                </div>

                <div class="fill-input-wrapper">
                    <input type="text" id="vocab-input" class="rhythm-text-input" placeholder="Nghe và gõ từ tiếng Anh tương ứng..." autocomplete="off" autofocus />
                    <button id="btn-submit-vocab" class="btn-primary">⚡ Tung Đòn (Enter)</button>
                </div>
            </div>
        `;

        // Automatically play pronunciation on beat!
        setTimeout(() => {
            window.soundEngine.speakWord(targetWord);
        }, 300);

        const btnAudio = document.getElementById("btn-play-audio");
        btnAudio.addEventListener("click", () => {
            window.soundEngine.speakWord(targetWord);
            input.focus();
        });

        const input = document.getElementById("vocab-input");
        setTimeout(() => input.focus(), 100);

        const submit = () => {
            const val = input.value.trim().toLowerCase();
            const target = targetWord.toLowerCase();
            if (this.timer) clearInterval(this.timer);
            if (this.keyListener) window.removeEventListener("keydown", this.keyListener);

            if (val === target) {
                window.soundEngine.playHitPerfect();
                this.game.handleCorrectHit(targetWord, ch.vn_prompt, phonetic);
            } else {
                window.soundEngine.playMiss();
                this.game.handlePlayerHurt(`Sai rồi! Từ vựng đúng là: "${targetWord}" ${phonetic}`);
            }
        };

        document.getElementById("btn-submit-vocab").addEventListener("click", submit);
        input.addEventListener("keydown", (e) => {
            if (e.key === "Enter") submit();
        });

        this.keyListener = (e) => {
            if (e.code === "Space" && document.activeElement !== input) {
                e.preventDefault();
                window.soundEngine.speakWord(targetWord);
            }
        };
        window.addEventListener("keydown", this.keyListener);
    }

    // ==========================================
    // 4. THỬ THÁCH 4: SẮP XẾP ĐOẠN VĂN
    // ==========================================
    renderParagraphOrder(ch) {
        const extra = ch.extra_data || {};
        const originalSentences = extra.sentences || [
            { id: 1, text: "First, eat well." },
            { id: 2, text: "Next, work hard." },
            { id: 3, text: "Finally, sleep tight." }
        ];

        // Shuffle sentences
        this.paragraphOrder = [...originalSentences].sort(() => Math.random() - 0.5);

        this.container.innerHTML = `
            <div class="challenge-card animate-fade-in">
                <div class="challenge-badge">📜 Thử Thách 4: Sắp Xếp Đoạn Văn Hoàn Chỉnh</div>
                <div class="vn-prompt-banner">
                    <span class="prompt-icon">⚔️ Nhiệm vụ:</span>
                    <h3 class="vn-prompt-text">${ch.vn_prompt}</h3>
                </div>

                <div class="rhythm-countdown-container">
                    <div class="rhythm-countdown-bar">
                        <div id="rhythm-countdown-fill" class="rhythm-countdown-fill" style="width: 100%;"></div>
                    </div>
                    <span id="rhythm-countdown-text" class="rhythm-countdown-text">⏳ Nhịp đếm: 24 beats</span>
                </div>

                <div class="paragraph-order-list" id="paragraph-list">
                    ${this.paragraphOrder.map((s, idx) => `
                        <div class="paragraph-sentence-item" data-id="${s.id}" data-idx="${idx}">
                            <div class="order-controls">
                                <button class="btn-move-up" data-idx="${idx}">▲</button>
                                <span class="order-number">${idx + 1}</span>
                                <button class="btn-move-down" data-idx="${idx}">▼</button>
                            </div>
                            <div class="sentence-text">${s.text}</div>
                        </div>
                    `).join("")}
                </div>

                <div class="action-buttons-row">
                    <button id="btn-submit-paragraph" class="btn-primary full-width">⚡ Giải Phóng Nhịp Điệu (Kiểm Tra Đoạn Văn)</button>
                </div>
            </div>
        `;

        this.bindParagraphEvents();
    }

    bindParagraphEvents() {
        const list = document.getElementById("paragraph-list");

        list.querySelectorAll(".btn-move-up").forEach(btn => {
            btn.addEventListener("click", () => {
                const idx = parseInt(btn.getAttribute("data-idx"));
                if (idx > 0) {
                    const temp = this.paragraphOrder[idx];
                    this.paragraphOrder[idx] = this.paragraphOrder[idx - 1];
                    this.paragraphOrder[idx - 1] = temp;
                    this.refreshParagraphView();
                }
            });
        });

        list.querySelectorAll(".btn-move-down").forEach(btn => {
            btn.addEventListener("click", () => {
                const idx = parseInt(btn.getAttribute("data-idx"));
                if (idx < this.paragraphOrder.length - 1) {
                    const temp = this.paragraphOrder[idx];
                    this.paragraphOrder[idx] = this.paragraphOrder[idx + 1];
                    this.paragraphOrder[idx + 1] = temp;
                    this.refreshParagraphView();
                }
            });
        });

        document.getElementById("btn-submit-paragraph").addEventListener("click", () => {
            if (this.timer) clearInterval(this.timer);
            // Check if ids are strictly sorted ascending 1, 2, 3, 4
            const isCorrect = this.paragraphOrder.every((s, i) => s.id === i + 1);

            if (isCorrect) {
                window.soundEngine.playHitPerfect();
                this.game.handleCorrectHit("Paragraph Mastery", "Sắp xếp đoạn văn hoàn hảo");
            } else {
                window.soundEngine.playMiss();
                this.game.handlePlayerHurt("Sai thứ tự đoạn văn! Các câu chưa tạo thành mạch logic.");
            }
        });
    }

    refreshParagraphView() {
        const list = document.getElementById("paragraph-list");
        if (!list) return;
        list.innerHTML = this.paragraphOrder.map((s, idx) => `
            <div class="paragraph-sentence-item" data-id="${s.id}" data-idx="${idx}">
                <div class="order-controls">
                    <button class="btn-move-up" data-idx="${idx}">▲</button>
                    <span class="order-number">${idx + 1}</span>
                    <button class="btn-move-down" data-idx="${idx}">▼</button>
                </div>
                <div class="sentence-text">${s.text}</div>
            </div>
        `).join("");
        this.bindParagraphEvents();
    }
}

window.ChallengeController = ChallengeController;
