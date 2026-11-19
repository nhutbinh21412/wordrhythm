// WordRhythm Authentication & User Session Manager
class AuthManager {
    constructor() {
        this.currentUser = window.ApiClient.getUser();
        this.initUI();
        if (!this.currentUser) {
            this.ensureSession();
        }
    }

    async ensureSession() {
        if (!window.ApiClient.getToken() || !window.ApiClient.getUser()) {
            try {
                // Auto-login as default demo student so SRS tracking and battles work immediately out-of-the-box
                await this.performLogin("student", "student123");
            } catch (e) {
                console.log("Auto student session initialization:", e);
            }
        }
    }

    initUI() {
        this.updateNavUser();
        this.bindEvents();
    }

    updateNavUser() {
        const user = window.ApiClient.getUser();
        const userNav = document.getElementById("nav-user-area");
        if (!userNav) return;

        if (user) {
            userNav.innerHTML = `
                <div class="user-badge animate-fade-in">
                    <span class="role-tag ${user.role}">${user.role === 'teacher' ? '👨‍🏫 Giáo Viên' : '🎓 Học Viên'}</span>
                    <span class="username">${user.username}</span>
                    <button id="btn-logout" class="btn-logout" title="Đăng xuất">Đăng Xuất</button>
                </div>
            `;
            document.getElementById("btn-logout").addEventListener("click", () => {
                this.logout();
            });
        } else {
            userNav.innerHTML = `
                <div class="auth-btn-group">
                    <button id="btn-open-login" class="btn-secondary">Đăng Nhập</button>
                    <button id="btn-open-register" class="btn-primary">Đăng Ký</button>
                </div>
            `;
            document.getElementById("btn-open-login").addEventListener("click", () => {
                this.showAuthModal("login");
            });
            document.getElementById("btn-open-register").addEventListener("click", () => {
                this.showAuthModal("register");
            });
        }

        // Toggle Teacher tab in navigation
        const tabEditor = document.getElementById("nav-tab-editor");
        if (tabEditor) {
            if (user && (user.role === "teacher" || user.role === "admin")) {
                tabEditor.classList.remove("hidden");
            } else {
                tabEditor.classList.add("hidden");
            }
        }
    }

    bindEvents() {
        // Quick Demo Login buttons
        const btnDemoStudent = document.getElementById("btn-demo-student");
        const btnDemoTeacher = document.getElementById("btn-demo-teacher");

        if (btnDemoStudent) {
            btnDemoStudent.addEventListener("click", async () => {
                await this.performLogin("student", "student123");
            });
        }

        if (btnDemoTeacher) {
            btnDemoTeacher.addEventListener("click", async () => {
                await this.performLogin("teacher", "teacher123");
            });
        }

        // Modal Close
        const modal = document.getElementById("auth-modal");
        const closeModal = document.getElementById("btn-close-modal");
        if (closeModal && modal) {
            closeModal.addEventListener("click", () => {
                modal.classList.add("hidden");
            });
        }

        // Form Submit
        const authForm = document.getElementById("auth-form");
        if (authForm) {
            authForm.addEventListener("submit", async (e) => {
                e.preventDefault();
                const mode = authForm.getAttribute("data-mode");
                const username = document.getElementById("auth-username").value.trim();
                const password = document.getElementById("auth-password").value.trim();

                if (mode === "login") {
                    await this.performLogin(username, password);
                } else {
                    const email = document.getElementById("auth-email").value.trim();
                    const role = document.getElementById("auth-role").value;
                    await this.performRegister(username, email, password, role);
                }
            });
        }
    }

    showAuthModal(mode = "login") {
        const modal = document.getElementById("auth-modal");
        const form = document.getElementById("auth-form");
        const title = document.getElementById("auth-modal-title");
        const emailGroup = document.getElementById("auth-email-group");
        const roleGroup = document.getElementById("auth-role-group");
        const submitBtn = document.getElementById("btn-auth-submit");

        form.setAttribute("data-mode", mode);

        if (mode === "login") {
            title.textContent = "Đăng Nhập Tài Khoản";
            emailGroup.classList.add("hidden");
            roleGroup.classList.add("hidden");
            submitBtn.textContent = "Đăng Nhập";
        } else {
            title.textContent = "Đăng Ký Tài Khoản Mới";
            emailGroup.classList.remove("hidden");
            roleGroup.classList.remove("hidden");
            submitBtn.textContent = "Tạo Tài Khoản";
        }

        modal.classList.remove("hidden");
    }

    async performLogin(username, password) {
        try {
            const res = await window.ApiClient.login(username, password);
            window.ApiClient.setToken(res.access_token);
            window.ApiClient.setUser(res.user);
            this.currentUser = res.user;
            this.updateNavUser();
            document.getElementById("auth-modal").classList.add("hidden");
            alert(`Chào mừng trở lại, ${res.user.username}!`);
            window.location.reload();
        } catch (err) {
            alert("Lỗi đăng nhập: " + err.message);
        }
    }

    async performRegister(username, email, password, role) {
        try {
            const res = await window.ApiClient.register(username, email, password, role);
            window.ApiClient.setToken(res.access_token);
            window.ApiClient.setUser(res.user);
            this.currentUser = res.user;
            this.updateNavUser();
            document.getElementById("auth-modal").classList.add("hidden");
            alert(`Đăng ký thành công tài khoản: ${res.user.username}!`);
            window.location.reload();
        } catch (err) {
            alert("Lỗi đăng ký: " + err.message);
        }
    }

    logout() {
        window.ApiClient.removeToken();
        this.currentUser = null;
        this.updateNavUser();
        alert("Đã đăng xuất tài khoản.");
        window.location.reload();
    }
}

window.authManager = new AuthManager();
