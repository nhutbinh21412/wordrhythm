// WordRhythm Teacher Level Editor
class LevelEditor {
    constructor() {
        this.container = document.getElementById("editor-view");
        this.teacherLevels = [];
        this.selectedLevelId = null;
    }

    async init() {
        const user = window.ApiClient.getUser();
        const editorGuard = document.getElementById("editor-role-guard");
        const editorContent = document.getElementById("editor-main-content");

        if (!user || (user.role !== "teacher" && user.role !== "admin")) {
            if (editorGuard) editorGuard.classList.remove("hidden");
            if (editorContent) editorContent.classList.add("hidden");
            return;
        }

        if (editorGuard) editorGuard.classList.add("hidden");
        if (editorContent) editorContent.classList.remove("hidden");

        await this.loadTeacherLevels();
        this.bindCreateLevelForm();
    }

    async loadTeacherLevels() {
        try {
            this.teacherLevels = await window.ApiClient.getTeacherLevels();
            const listEl = document.getElementById("editor-levels-list");
            if (!listEl) return;

            if (this.teacherLevels.length === 0) {
                listEl.innerHTML = `<div class="empty-state">Bạn chưa tạo màn chơi tùy chỉnh nào. Hãy tạo màn đầu tiên bên dưới!</div>`;
                return;
            }

            listEl.innerHTML = this.teacherLevels.map(lvl => `
                <div class="teacher-level-row animate-fade-in" data-id="${lvl.id}">
                    <div class="level-meta">
                        <h4>${lvl.title}</h4>
                        <div class="sub-meta">Boss: <strong>${lvl.boss_name}</strong> | ${lvl.bpm} BPM | HP: ${lvl.boss_hp} | ${lvl.challenges_count} câu hỏi</div>
                    </div>
                    <div class="actions">
                        <button class="btn-sm-danger btn-del-lvl" data-id="${lvl.id}">🗑️ Xóa</button>
                    </div>
                </div>
            `).join("");

            listEl.querySelectorAll(".btn-del-lvl").forEach(btn => {
                btn.addEventListener("click", async (e) => {
                    e.stopPropagation();
                    const id = parseInt(btn.getAttribute("data-id"));
                    if (confirm("Bạn có chắc chắn muốn xóa màn chơi này?")) {
                        await window.ApiClient.deleteLevel(id);
                        await this.loadTeacherLevels();
                    }
                });
            });
        } catch (e) {
            console.error("Failed to load teacher levels:", e);
        }
    }

    bindCreateLevelForm() {
        const form = document.getElementById("form-create-level");
        const bpmSlider = document.getElementById("editor-bpm-slider");
        const bpmValue = document.getElementById("editor-bpm-value");
        const btnBpmPreview = document.getElementById("btn-bpm-preview");

        if (bpmSlider && bpmValue) {
            bpmSlider.addEventListener("input", () => {
                bpmValue.textContent = `${bpmSlider.value} BPM`;
            });
        }

        if (btnBpmPreview) {
            let isPreviewing = false;
            btnBpmPreview.addEventListener("click", (e) => {
                e.preventDefault();
                if (!isPreviewing) {
                    const bpm = parseInt(bpmSlider.value);
                    window.soundEngine.startRhythmTrack(bpm);
                    btnBpmPreview.textContent = "⏹️ Dừng Nghe Thử";
                    isPreviewing = true;
                } else {
                    window.soundEngine.stopRhythmTrack();
                    btnBpmPreview.textContent = "🎵 Nghe Thử Nhịp";
                    isPreviewing = false;
                }
            });
        }

        // Challenge type dynamic fields
        const challengeTypeSelect = document.getElementById("editor-challenge-type");
        const challengeFieldsContainer = document.getElementById("challenge-dynamic-fields");

        if (challengeTypeSelect && challengeFieldsContainer) {
            challengeTypeSelect.addEventListener("change", () => {
                this.renderDynamicFields(challengeTypeSelect.value, challengeFieldsContainer);
            });
            this.renderDynamicFields(challengeTypeSelect.value, challengeFieldsContainer);
        }

        if (form) {
            form.addEventListener("submit", async (e) => {
                e.preventDefault();
                await this.handleCreateLevelSubmit();
            });
        }
    }

    renderDynamicFields(type, container) {
        if (type === "sentence_assemble") {
            container.innerHTML = `
                <div class="form-group">
                    <label>Câu Tiếng Việt (Boss ra đề):</label>
                    <input type="text" id="ch-vn-prompt" class="form-input" placeholder="Ví dụ: Tôi muốn ăn một quả táo tươi ngon." required />
                </div>
                <div class="form-group">
                    <label>Câu Tiếng Anh chuẩn (Đáp án):</label>
                    <input type="text" id="ch-en-target" class="form-input" placeholder="Ví dụ: I want to eat a fresh apple" required />
                </div>
                <div class="form-group">
                    <label>Từ gây nhiễu (phân tách bằng dấu phẩy):</label>
                    <input type="text" id="ch-distractors" class="form-input" placeholder="Ví dụ: drinks, he, an, banana, fast" />
                </div>
            `;
        } else if (type === "fill_blank") {
            container.innerHTML = `
                <div class="form-group">
                    <label>Câu Tiếng Anh có chỗ khuyết (dùng ___):</label>
                    <input type="text" id="ch-blank-sentence" class="form-input" placeholder="Ví dụ: She is following a traditional Italian ___ to make pasta." required />
                </div>
                <div class="form-group">
                    <label>Từ tiếng Anh còn thiếu (Đáp án):</label>
                    <input type="text" id="ch-en-target" class="form-input" placeholder="Ví dụ: recipe" required />
                </div>
                <div class="form-group">
                    <label>Nghĩa tiếng Việt & Gợi ý:</label>
                    <input type="text" id="ch-vn-prompt" class="form-input" placeholder="Ví dụ: công thức nấu ăn (r______)" required />
                </div>
                <div class="form-group">
                    <label>Phiên âm Cambridge (tùy chọn):</label>
                    <input type="text" id="ch-phonetic" class="form-input" placeholder="Ví dụ: /ˈres.ə.pi/" />
                </div>
            `;
        } else if (type === "vocab_pronounce") {
            container.innerHTML = `
                <div class="form-group">
                    <label>Từ Tiếng Việt (Nghĩa):</label>
                    <input type="text" id="ch-vn-prompt" class="form-input" placeholder="Ví dụ: con người, loài người" required />
                </div>
                <div class="form-group">
                    <label>Từ Tiếng Anh chuẩn (Đáp án gõ & phát âm):</label>
                    <input type="text" id="ch-en-target" class="form-input" placeholder="Ví dụ: human" required />
                </div>
                <div class="form-group">
                    <label>Phiên âm Cambridge:</label>
                    <input type="text" id="ch-phonetic" class="form-input" placeholder="Ví dụ: /ˈhjuː.mən/" />
                </div>
            `;
        } else if (type === "paragraph_order") {
            container.innerHTML = `
                <div class="form-group">
                    <label>Yêu cầu đoạn văn:</label>
                    <input type="text" id="ch-vn-prompt" class="form-input" placeholder="Ví dụ: Sắp xếp các câu sau thành bài viết hoàn chỉnh:" required />
                </div>
                <div class="form-group">
                    <label>Câu 1 (Mở đầu):</label>
                    <input type="text" id="ch-para-1" class="form-input" placeholder="First, ..." required />
                </div>
                <div class="form-group">
                    <label>Câu 2 (Tiếp theo):</label>
                    <input type="text" id="ch-para-2" class="form-input" placeholder="Next, ..." required />
                </div>
                <div class="form-group">
                    <label>Câu 3 (Kế tiếp):</label>
                    <input type="text" id="ch-para-3" class="form-input" placeholder="Then, ..." required />
                </div>
                <div class="form-group">
                    <label>Câu 4 (Kết luận):</label>
                    <input type="text" id="ch-para-4" class="form-input" placeholder="Finally, ..." required />
                </div>
            `;
        }
    }

    async handleCreateLevelSubmit() {
        const title = document.getElementById("editor-level-title").value.trim();
        const theme = document.getElementById("editor-level-theme").value.trim();
        const bossName = document.getElementById("editor-boss-name").value.trim();
        const bossTitle = document.getElementById("editor-boss-title").value.trim();
        const bossAvatar = document.getElementById("editor-boss-avatar").value;
        const bpm = parseInt(document.getElementById("editor-bpm-slider").value);
        const bossHp = parseInt(document.getElementById("editor-boss-hp").value);
        const difficulty = document.getElementById("editor-difficulty").value;

        const type = document.getElementById("editor-challenge-type").value;
        let challenge = null;

        if (type === "sentence_assemble") {
            const vnPrompt = document.getElementById("ch-vn-prompt").value.trim();
            const enTarget = document.getElementById("ch-en-target").value.trim();
            const rawDistractors = document.getElementById("ch-distractors").value.trim();
            const distractors = rawDistractors ? rawDistractors.split(",").map(s => s.trim()) : [];
            challenge = {
                challenge_type: "sentence_assemble",
                vn_prompt: vnPrompt,
                en_target: enTarget,
                extra_data: { distractors }
            };
        } else if (type === "fill_blank") {
            const sentenceWithBlank = document.getElementById("ch-blank-sentence").value.trim();
            const enTarget = document.getElementById("ch-en-target").value.trim();
            const vnPrompt = document.getElementById("ch-vn-prompt").value.trim();
            const phonetic = document.getElementById("ch-phonetic").value.trim();
            challenge = {
                challenge_type: "fill_blank",
                vn_prompt: "Điền từ còn thiếu vào câu:",
                en_target: enTarget,
                extra_data: {
                    sentence_with_blank: sentenceWithBlank,
                    hint: vnPrompt,
                    phonetic: phonetic,
                    meaning_vn: vnPrompt
                }
            };
        } else if (type === "vocab_pronounce") {
            const vnPrompt = document.getElementById("ch-vn-prompt").value.trim();
            const enTarget = document.getElementById("ch-en-target").value.trim();
            const phonetic = document.getElementById("ch-phonetic").value.trim();
            challenge = {
                challenge_type: "vocab_pronounce",
                vn_prompt: vnPrompt,
                en_target: enTarget,
                extra_data: { phonetic, meaning_vn: vnPrompt }
            };
        } else if (type === "paragraph_order") {
            const vnPrompt = document.getElementById("ch-vn-prompt").value.trim();
            const p1 = document.getElementById("ch-para-1").value.trim();
            const p2 = document.getElementById("ch-para-2").value.trim();
            const p3 = document.getElementById("ch-para-3").value.trim();
            const p4 = document.getElementById("ch-para-4").value.trim();
            challenge = {
                challenge_type: "paragraph_order",
                vn_prompt: vnPrompt,
                en_target: "1|2|3|4",
                extra_data: {
                    sentences: [
                        { id: 1, text: p1 },
                        { id: 2, text: p2 },
                        { id: 3, text: p3 },
                        { id: 4, text: p4 }
                    ]
                }
            };
        }

        try {
            await window.ApiClient.createLevel({
                title,
                theme,
                boss_name: bossName,
                boss_title: bossTitle,
                boss_avatar: bossAvatar,
                bpm,
                boss_hp: bossHp,
                difficulty,
                is_published: true,
                challenges: [challenge]
            });

            alert("Tạo màn chơi Boss mới thành công!");
            document.getElementById("form-create-level").reset();
            await this.loadTeacherLevels();
        } catch (err) {
            alert("Lỗi khi tạo màn chơi: " + err.message);
        }
    }
}

window.levelEditor = new LevelEditor();
