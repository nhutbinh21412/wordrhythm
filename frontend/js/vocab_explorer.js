// WordRhythm Cambridge Vocabulary Explorer Controller
class VocabExplorer {
    constructor() {
        this.container = document.getElementById("vocab-explorer-grid");
        this.words = [];
        this.currentFilterCEFR = "ALL";
        this.currentFilterTopic = "ALL";
        this.searchQuery = "";
    }

    async init() {
        await this.loadWords();
        this.bindEvents();
    }

    async loadWords() {
        try {
            const data = await window.ApiClient.request("/api/cambridge/all");
            this.words = data;
            this.render();
        } catch (e) {
            console.error("Failed to load vocabulary bank:", e);
        }
    }

    bindEvents() {
        const searchInput = document.getElementById("vocab-search-input");
        if (searchInput) {
            searchInput.addEventListener("input", (e) => {
                this.searchQuery = e.target.value.trim().toLowerCase();
                this.render();
            });
        }

        const cefrPills = document.querySelectorAll(".cefr-filter-pills .pill-filter");
        cefrPills.forEach(pill => {
            pill.addEventListener("click", () => {
                cefrPills.forEach(p => p.classList.remove("active"));
                pill.classList.add("active");
                this.currentFilterCEFR = pill.getAttribute("data-cefr");
                this.render();
            });
        });
    }

    render() {
        if (!this.container) return;

        let filtered = this.words.filter(w => {
            // CEFR filter
            if (this.currentFilterCEFR !== "ALL" && w.cefr.toUpperCase() !== this.currentFilterCEFR) {
                return false;
            }
            // Search query
            if (this.searchQuery) {
                const matchWord = w.word.toLowerCase().includes(this.searchQuery);
                const matchVn = (w.meaning_vn || "").toLowerCase().includes(this.searchQuery);
                const matchDef = (w.definition || "").toLowerCase().includes(this.searchQuery);
                const matchTopic = (w.topic || "").toLowerCase().includes(this.searchQuery);
                if (!matchWord && !matchVn && !matchDef && !matchTopic) return false;
            }
            return true;
        });

        if (filtered.length === 0) {
            this.container.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-tertiary);">
                    Không tìm thấy từ vựng nào khớp với bộ lọc "${this.searchQuery}".
                </div>
            `;
            return;
        }

        this.container.innerHTML = filtered.map(w => `
            <div class="vocab-card animate-fade-in">
                <div>
                    <div class="vocab-card-header">
                        <div class="vocab-word-title">
                            ${w.word}
                            <span class="cefr-tag cefr-${w.cefr}">${w.cefr}</span>
                        </div>
                        <span style="font-size: 11px; color: var(--text-tertiary); text-transform: uppercase;">${w.topic || 'General'}</span>
                    </div>

                    <div class="vocab-card-phonetic">${w.phonetic || ''} • <span style="color: var(--text-tertiary); font-style: italic;">${w.pos || 'noun'}</span></div>
                    <div class="vocab-card-meaning">🇻🇳 ${w.meaning_vn}</div>
                    <div class="vocab-card-definition">${w.definition || ''}</div>

                    ${w.example ? `<div class="vocab-card-example">"${w.example}"</div>` : ''}
                </div>

                <div class="vocab-card-footer">
                    <div style="font-size: 11.5px; color: var(--text-tertiary);">
                        ${w.collocations && w.collocations.length > 0 ? `Collocations: <strong>${w.collocations.slice(0, 2).join(', ')}</strong>` : ''}
                    </div>
                    <button class="btn-sm-audio" data-word="${w.word}">🔊 Nghe</button>
                </div>
            </div>
        `).join("");

        this.container.querySelectorAll(".btn-sm-audio").forEach(btn => {
            btn.addEventListener("click", () => {
                const word = btn.getAttribute("data-word");
                window.soundEngine.speakWord(word);
            });
        });
    }
}

window.vocabExplorer = new VocabExplorer();
