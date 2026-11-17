# 🚀 Hướng Dẫn Deploy WordRhythm Lên Render.com (Miễn Phí 100%)

Tài liệu này hướng dẫn bạn từng bước từ đẩy code lên GitHub đến việc kích hoạt ứng dụng trên **Render.com** để có đường link URL online công khai nộp bài hoặc chia sẻ.

---

## 📋 Danh Sách File Đã Chuẩn Bị Sẵn Cho Render
- [`.gitignore`](.gitignore): Bỏ qua file rác, cache `__pycache__`, database cục bộ `.db`, virtualenv `.venv` để repo luôn nhẹ và sạch.
- [`render.yaml`](render.yaml): Cấu hình Blueprint tự động cho Render (khởi chạy Python 3.12, tự tạo `SECRET_KEY`, tự cài thư viện qua `requirements.txt`).
- [`Procfile`](Procfile): Khai báo lệnh chạy web server cho Render / Heroku / Railway.
- [`runtime.txt`](runtime.txt): Chỉ định phiên bản Python chuẩn `python-3.12.0`.
- [`.env.example`](.env.example): Mẫu biến môi trường.
- [`requirements.txt`](requirements.txt): Các thư viện chuẩn sản phẩm.

---

## 🛠️ Bước 1: Đẩy Mã Nguồn Lên GitHub

Mở PowerShell tại thư mục `c:\GroupProjects\WordRhythm_new` và chạy các lệnh sau:

```powershell
# 1. Khởi tạo Git
git init

# 2. Thêm tất cả các file vào Git (nhờ .gitignore nên code sẽ cực kỳ gọn)
git add .

# 3. Tạo commit đầu tiên
git commit -m "Deploy WordRhythm full-stack to Render"

# 4. Đổi tên nhánh chính thành main
git branch -M main

# 5. Liên kết tới GitHub Repository của bạn (Thay URL bên dưới bằng link repo GitHub của bạn)
git remote add origin https://github.com/<tai-khoan-cua-ban>/WordRhythm.git

# 6. Đẩy code lên GitHub
git push -u origin main
```

*(Lưu ý: Bạn tạo trước 1 repository trống trên [GitHub.com](https://github.com/new) tên là `WordRhythm`).*

---

## 🌐 Bước 2: Deploy Lên Render.com

Có 2 cách deploy, bạn chọn cách nào cũng được (Cách 1 là nhanh nhất):

### 👉 Cách 1: Dùng Blueprint (Khuyên dùng - 1 Click tự động)
1. Đăng nhập vào [Render.com](https://dashboard.render.com/).
2. Nhấn vào nút **New +** ở góc trên bên phải $\rightarrow$ Chọn **Blueprint**.
3. Kết nối với tài khoản GitHub của bạn và chọn repository **WordRhythm**.
4. Render sẽ tự động phát hiện file `render.yaml` và cấu hình sẵn toàn bộ.
5. Nhấn **Apply**. Render sẽ tự động:
   - Cài đặt `requirements.txt`.
   - Tạo khóa `SECRET_KEY` bảo mật.
   - Chạy lệnh `python run_server.py`.
   - Kiểm tra trạng thái `/health`.
6. Sau khoảng 1-2 phút, bạn sẽ nhận được đường link URL dạng:  
   `https://wordrhythm-game.onrender.com`

---

### 👉 Cách 2: Tạo Web Service Thủ Công
Nếu không dùng Blueprint, bạn có thể tạo thủ công:
1. Trên Render Dashboard, nhấn **New +** $\rightarrow$ Chọn **Web Service**.
2. Chọn repo GitHub **WordRhythm**.
3. Điền các thông số:
   - **Name**: `wordrhythm` (hoặc tên tùy thích)
   - **Region**: Singapore (hoặc Oregon)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run_server.py`
   - **Instance Type**: `Free`
4. Mở rộng phần **Environment Variables**, thêm:
   - `PYTHON_VERSION` = `3.12.0`
   - `ENVIRONMENT` = `production`
5. Nhấn **Create Web Service**.

---

## 🔍 Bước 3: Kiểm Tra Sau Khi Deploy

1. Mở đường link do Render cấp: `https://<ten-app-cua-ban>.onrender.com`.
2. Kiểm tra các tính năng:
   - Giao diện 2D Rhythm Game tải mượt mà.
   - Nhấn **🎓 Học Viên** hoặc **👨‍🏫 Giáo Viên** để đăng nhập 1 chạm.
   - Vào chiến thử 1 trận Boss để kiểm tra âm thanh metronome và thanh máu.
   - Vào tab **📖 Kho Từ Vựng** tra cứu và bấm nghe phát âm.
   - Vào tab **🧠 Spaced Repetition** xem các thẻ ôn tập SM-2.
