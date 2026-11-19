// WordRhythm Authentication & User Session Manager
class AuthManager {
    constructor() {
        this.currentUser = window.ApiClient.getUser();
        this.initUI();
        // Only run ensureSession if user has never explicitly logged out
        if (!this.currentUser && sessionStorage.getItem("user_logged_out") !== "true") {
            this.ensureSession();
        }
    }

    async ensureSession() {
        // If user explicitly logged out, DO NOT auto-login back into student!
        if (sessionStorage.getItem("user_logged_out") === "true") {
            return;
        }
        if (!window.ApiClient.getToken() || !window.ApiClient.getUser()) {
            try {
                // Auto-login as student only on first fresh visit
                const res = await window.ApiClient.login("student", "student123");
                window.ApiClient.setToken(res.access_token);
                window.ApiClient.setUser(res.user);
                this.currentUser = res.user;
                this.updateNavUser();
            } catch (e) {
                console.log("Auto student session initialization skipped:", e);
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
        const btnDemoTeacherDemo = document.getElementById("btn-demo-teacherdemo");

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

        if (btnDemoTeacherDemo) {
            btnDemoTeacherDemo.addEventListener("click", async () => {
                await this.performLogin("teacherdemo", "123456");
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

        // Clear previous input values
        document.getElementById("auth-username").value = "";
        document.getElementById("auth-password").value = "";

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
            sessionStorage.removeItem("user_logged_out");
            const res = await window.ApiClient.login(username, password);
            window.ApiClient.setToken(res.access_token);
            window.ApiClient.setUser(res.user);
            this.currentUser = res.user;
            this.updateNavUser();
            
            const modal = document.getElementById("auth-modal");
            if (modal) modal.classList.add("hidden");

            // Re-sync UI components
            if (window.srsDashboard) window.srsDashboard.init();
            if (window.levelEditor && (res.user.role === 'teacher' || res.user.role === 'admin')) {
                window.levelEditor.init();
            }
            alert(`Đăng nhập thành công! Xin chào ${res.user.username} (${res.user.role === 'teacher' ? 'Giáo Viên' : 'Học Viên'}).`);
        } catch (err) {
            alert("Lỗi đăng nhập: " + err.message);
        }
    }

    async performRegister(username, email, password, role) {
        try {
            sessionStorage.removeItem("user_logged_out");
            const res = await window.ApiClient.register(username, email, password, role);
            window.ApiClient.setToken(res.access_token);
            window.ApiClient.setUser(res.user);
            this.currentUser = res.user;
            this.updateNavUser();
            
            const modal = document.getElementById("auth-modal");
            if (modal) modal.classList.add("hidden");

            // Re-sync UI components
            if (window.srsDashboard) window.srsDashboard.init();
            if (window.levelEditor && (res.user.role === 'teacher' || res.user.role === 'admin')) {
                window.levelEditor.init();
            }
            alert(`Đăng ký thành công tài khoản: ${res.user.username}!`);
        } catch (err) {
            alert("Lỗi đăng ký: " + err.message);
        }
    }

    logout() {
        sessionStorage.setItem("user_logged_out", "true");
        window.ApiClient.removeToken();
        this.currentUser = null;
        this.updateNavUser();
        
        // Hide teacher tab if visible
        const tabEditor = document.getElementById("nav-tab-editor");
        if (tabEditor) tabEditor.classList.add("hidden");

        // If currently in editor view, switch back to campaign
        const viewEditor = document.getElementById("view-editor");
        if (viewEditor && viewEditor.classList.contains("active")) {
            document.querySelectorAll(".nav-tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".view-section").forEach(v => v.classList.remove("active"));
            document.getElementById("nav-tab-campaign").classList.add("active");
            document.getElementById("view-campaign").classList.add("active");
        }

        alert("Đã đăng xuất tài khoản. Bạn có thể đăng nhập tài khoản khác bên dưới.");
        this.showAuthModal("login");
    }
}

window.authManager = new AuthManager();
