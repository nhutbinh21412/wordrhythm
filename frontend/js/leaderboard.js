// WordRhythm Leaderboard Controller
class LeaderboardView {
    constructor() {
        this.container = document.getElementById("leaderboard-list");
    }

    async init() {
        await this.loadGlobal();
    }

    async loadGlobal() {
        try {
            const data = await window.ApiClient.getGlobalLeaderboard();
            if (!this.container) return;

            if (data.length === 0) {
                this.container.innerHTML = `<tr><td colspan="5" class="empty-state">Chưa có bảng xếp hạng. Hãy là người đầu tiên chinh phục Boss!</td></tr>`;
                return;
            }

            this.container.innerHTML = data.map((item, idx) => {
                let rankBadge = `${idx + 1}`;
                if (idx === 0) rankBadge = "🥇 1";
                else if (idx === 1) rankBadge = "🥈 2";
                else if (idx === 2) rankBadge = "🥉 3";

                return `
                    <tr class="animate-fade-in ${idx < 3 ? 'top-rank-row' : ''}">
                        <td class="rank-cell"><strong>${rankBadge}</strong></td>
                        <td class="user-cell">
                            <span class="avatar-icon">🎮</span>
                            <strong>${item.username}</strong>
                        </td>
                        <td class="score-cell">${item.score.toLocaleString()} pts</td>
                        <td class="combo-cell">${item.max_combo}x Combo</td>
                        <td class="accuracy-cell">${item.accuracy}%</td>
                    </tr>
                `;
            }).join("");
        } catch (e) {
            console.error("Failed to load leaderboard:", e);
        }
    }
}

window.leaderboardView = new LeaderboardView();
