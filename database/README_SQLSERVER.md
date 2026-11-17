# 🗄️ Hướng Dẫn Sử Dụng Database SQL Server Management Studio (SSMS) Cho WordRhythm

Dự án đã được tích hợp đầy đủ file script cơ sở dữ liệu T-SQL chuẩn hóa cho **Microsoft SQL Server** và **SQL Server Management Studio (SSMS)** (hỗ trợ SQL Server 2016, 2019, 2022 và Azure SQL Database).

---

## 📂 File Script SQL
- Đường dẫn file: [`database/wordrhythm_sqlserver.sql`](wordrhythm_sqlserver.sql)
- Kích thước: ~44 KB (Đầy đủ cấu trúc bảng DDL, khóa ngoại FK, Index, Views báo cáo và 100% dữ liệu mẫu Tiếng Việt Unicode UTF-8).

---

## 🚀 Các Bước Chạy Trong SQL Server Management Studio (SSMS)

### Bước 1: Mở SQL Server Management Studio (SSMS)
1. Mở phần mềm **SQL Server Management Studio (SSMS)** trên máy tính.
2. Đăng nhập vào SQL Server instance của bạn (ví dụ: `.` hoặc `localhost` hoặc `SQLEXPRESS` bằng Windows Authentication hoặc tài khoản `sa`).

### Bước 2: Mở và thực thi Script
1. Chọn menu **File** $\rightarrow$ **Open** $\rightarrow$ **File...** (hoặc phím tắt `Ctrl + O`).
2. Điều hướng và chọn file:
   ```
   c:\GroupProjects\WordRhythm_new\database\wordrhythm_sqlserver.sql
   ```
3. Nhấn nút **Execute** (hoặc phím **`F5`**).
4. Bạn sẽ thấy thông báo:
   ```
   ✅ WordRhythmDB initialized and seeded successfully for SQL Server Management Studio!
   ```

---

## 📊 Cấu Trúc Các Bảng Trong Database (`WordRhythmDB`)

| Tên Bảng | Ý nghĩa | Mô tả các trường chính |
| :--- | :--- | :--- |
| `dbo.users` | Quản lý người dùng & phân quyền | `id`, `username`, `email`, `hashed_password` (Bcrypt), `role` ('student', 'teacher', 'admin') |
| `dbo.levels` | Danh sách màn chơi Boss | `id`, `title`, `theme`, `boss_name`, `boss_title`, `boss_avatar`, `bpm`, `boss_hp`, `difficulty` |
| `dbo.challenges` | 4 Kiểu thử thách của Boss | `id`, `level_id`, `challenge_type` (sentence_assemble, fill_blank, vocab_pronounce, paragraph_order), `vn_prompt`, `en_target`, `extra_data` (JSON) |
| `dbo.srs_reviews` | Trí nhớ Spaced Repetition SM-2 | `id`, `user_id`, `word_en`, `meaning_vn`, `repetition_n`, `ease_factor` ($EF$), `interval_days` ($I$), `next_review_date`, `total_mistakes`, `total_reviews` |
| `dbo.game_sessions` | Lịch sử các trận đấu Boss | `id`, `user_id`, `level_id`, `score`, `accuracy`, `max_combo`, `won`, `hp_remaining`, `completed_at` |
| `dbo.leaderboard_entries`| Bảng xếp hạng điểm số | `id`, `user_id`, `level_id`, `score`, `accuracy`, `max_combo`, `created_at` |
| `dbo.cambridge_vocabulary` | Kho từ điển Cambridge A1-C1 | `id`, `word`, `phonetic` (IPA), `cefr_level`, `topic`, `meaning_vn`, `definition`, `example`, `collocations` |

---

## 🔍 Các View Báo Cáo Có Sẵn Cho Giáo Viên & Giám Khảo

Script đã tạo sẵn 2 View phân tích dữ liệu rất hữu ích:

### 1. Xem thống kê những từ vựng học sinh hay làm sai nhất:
```sql
SELECT * FROM dbo.vw_WeakWordsAnalysis
ORDER BY mistake_percentage DESC, total_mistakes DESC;
```

### 2. Xem bảng xếp hạng điểm số theo từng màn Boss:
```sql
SELECT * FROM dbo.vw_LevelLeaderboardOverview
ORDER BY score DESC;
```

---

## 🔗 Cách Kết Nối FastAPI Trực Tiếp Vào SQL Server (Tùy chọn)

Nếu bạn muốn FastAPI kết nối thẳng tới Microsoft SQL Server thay vì SQLite:
1. Cài driver:
   ```bash
   pip install pymssql
   # Hoặc dùng pyodbc
   pip install pyodbc
   ```
2. Đặt biến môi trường `DATABASE_URL` trong file `.env` hoặc hệ thống:
   ```env
   # Nếu dùng SQL Server xác thực tài khoản sa:
   DATABASE_URL=mssql+pymssql://sa:YourPassword123@localhost/WordRhythmDB

   # Hoặc nếu dùng Windows Authentication với ODBC Driver 17:
   DATABASE_URL=mssql+pyodbc://localhost/WordRhythmDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
   ```
3. Chạy lại `python run_server.py`. Hệ thống sẽ tự động dùng SQL Server!
