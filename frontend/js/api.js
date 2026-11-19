// WordRhythm API Client
const API_BASE = window.location.origin;

class ApiClient {
    static getToken() {
        return localStorage.getItem("wordrhythm_token");
    }

    static setToken(token) {
        localStorage.setItem("wordrhythm_token", token);
    }

    static removeToken() {
        localStorage.removeItem("wordrhythm_token");
        localStorage.removeItem("wordrhythm_user");
    }

    static getUser() {
        try {
            return JSON.parse(localStorage.getItem("wordrhythm_user"));
        } catch (e) {
            return null;
        }
    }

    static setUser(user) {
        localStorage.setItem("wordrhythm_user", JSON.stringify(user));
    }

    static async request(endpoint, options = {}) {
        const url = `${API_BASE}${endpoint}`;
        const headers = {
            "Content-Type": "application/json",
            ...options.headers
        };

        const token = this.getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            if (response.status === 401) {
                // Token expired or invalid - clear invalid token from localStorage
                console.warn("Unauthorized request (401), clearing stale token.");
                this.removeToken();
                if (window.authManager) {
                    window.authManager.updateNavUser();
                }
            }

            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.detail || "Có lỗi xảy ra từ máy chủ.");
            }
            return data;
        } catch (err) {
            console.error(`API Error [${endpoint}]:`, err);
            throw err;
        }
    }

    // Auth endpoints
    static login(username, password) {
        return this.request("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({ username, password })
        });
    }

    static register(username, email, password, role = "student") {
        return this.request("/api/auth/register", {
            method: "POST",
            body: JSON.stringify({ username, email, password, role })
        });
    }

    static getMe() {
        return this.request("/api/auth/me");
    }

    // Game endpoints
    static getLevels() {
        return this.request("/api/game/levels");
    }

    static getLevel(id) {
        return this.request(`/api/game/levels/${id}`);
    }

    static submitSession(data) {
        return this.request("/api/game/submit-session", {
            method: "POST",
            body: JSON.stringify(data)
        });
    }

    // SRS endpoints
    static getSRSStats() {
        return this.request("/api/srs/stats");
    }

    static getSRSDue() {
        return this.request("/api/srs/due");
    }

    static getWeakWords() {
        return this.request("/api/srs/weak-words");
    }

    static submitSRSReview(data) {
        return this.request("/api/srs/review", {
            method: "POST",
            body: JSON.stringify(data)
        });
    }

    static getMistakeBoss() {
        return this.request("/api/srs/mistake-boss");
    }

    // Leaderboard
    static getGlobalLeaderboard() {
        return this.request("/api/leaderboard/global");
    }

    static getLevelLeaderboard(levelId) {
        return this.request(`/api/leaderboard/level/${levelId}`);
    }

    // Teacher Editor
    static getTeacherLevels() {
        return this.request("/api/editor/levels");
    }

    static createLevel(levelData) {
        return this.request("/api/editor/levels", {
            method: "POST",
            body: JSON.stringify(levelData)
        });
    }

    static deleteLevel(levelId) {
        return this.request(`/api/editor/levels/${levelId}`, {
            method: "DELETE"
        });
    }

    static addChallenge(levelId, challengeData) {
        return this.request(`/api/editor/levels/${levelId}/challenges`, {
            method: "POST",
            body: JSON.stringify(challengeData)
        });
    }

    static deleteChallenge(challengeId) {
        return this.request(`/api/editor/challenges/${challengeId}`, {
            method: "DELETE"
        });
    }

    // Cambridge Lookup
    static lookupCambridge(word) {
        return this.request(`/api/cambridge/lookup?q=${encodeURIComponent(word)}`);
    }
}

window.ApiClient = ApiClient;
