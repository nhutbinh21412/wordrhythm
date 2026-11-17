# 🎵 WordRhythm: 2D Rhythm Boss Battle Language Learning Platform
> **Game Rhythm Luyện Từ Vựng Có Spaced Repetition (SuperMemo SM-2) Và Level Editor Cho Giáo Viên**

WordRhythm là nền tảng game hóa học ngoại ngữ 2D kết hợp giữa lối chơi nhịp điệu (Rhythm Game) dồn dập theo BPM, kho từ vựng học thuật chuẩn khảo thí **Cambridge English (A1 - C1)** và thuật toán ghi nhớ chu kỳ ngắt quãng **SuperMemo SM-2**. Giao diện được thiết kế theo phong cách tối giản, hiện đại và chuyên nghiệp (Modern Dark Minimalist UI).

---

## 🌟 Tính Năng Mới & Nâng Cấp Toàn Diện

### 1. 📖 Kho Từ Vựng Chuẩn Cambridge (Cambridge Vocabulary Explorer)
- Mở rộng kho từ vựng học thuật đa dạng cấp độ từ **A1 đến C1** phân theo 7 chủ đề lớn:
  - **Food & Nutrition** (recipe, ingredient, nutrition, beverage, delicious...)
  - **Technology & AI** (human, algorithm, cybersecurity, automation, innovation, database...)
  - **Nature & Environment** (biodiversity, sustainable, ecosystem, extinction, renewable...)
  - **Business & Economics** (entrepreneur, investment, monopoly, revenue, strategy...)
  - **Travel & Culture** (itinerary, destination, heritage, hospitality...)
  - **Academic & IELTS Mastery** (pivotal, unprecedented, paradigm, comprehensive, hypothesis...)
  - **Health & Mindset** (symptom, resilience, vaccine...)
- **Tính năng tra cứu thông minh**:
  - Tìm kiếm thời gian thực theo từ vựng, nghĩa tiếng Việt hoặc định nghĩa.
  - Bộ lọc nhanh theo khung năng lực Châu Âu **CEFR (A1, A2, B1, B2, C1)**.
  - Nghe phát âm chuẩn bản xứ Anh/Mỹ trực tiếp bằng Web Audio / Speech Synthesis.
  - Hiển thị đầy đủ phiên âm quốc tế IPA, định nghĩa Anh - Anh, collocations thông dụng và câu ví dụ thực tế.

### 2. 🎨 Giao Diện Tinh Gọn, Hiện Đại & Chuyên Nghiệp (Clean & Minimalist UI)
- Loại bỏ các hiệu ứng đèn neon chói gắt, thay bằng bảng màu tối tinh tế (Deep Obsidian `#090d16` & Slate `#0f172a`), điểm xuyết bằng ngọc lục bảo Emerald `#10b981`, xanh Cyan `#06b6d4` và hổ phách Amber `#f59e0b`.
- Phông chữ hiện đại chuẩn quốc tế: **Plus Jakarta Sans** cho giao diện, **JetBrains Mono** cho phiên âm IPA và chỉ số BPM.
- Bố cục thẻ bài (Card-based Layout) với khoảng cách thoáng đãng, các phím bấm chọn từ kèm phím tắt `[1]`, `[2]`, `[3]` trực quan.
- Đấu trường 2D Canvas được tối ưu 60 FPS mượt mà với thanh máu Boss thanh mảnh, 3 trái tim người chơi dạng ngọc hồng lựu và hiệu ứng sóng nhịp thanh lịch.

### 3. ⚔️ Cơ Chế Đấu Boss Theo Nhịp & 4 Kiểu Thử Thách
- **Nhịp nền (BPM)**: Nhịp điệu dồn dập từ 105 đến 140 BPM đồng bộ hóa với Web Audio API.
- **Quy tắc chiến đấu**: Người chơi có **3 HP** (mỗi câu sai hoặc hết giờ bị trừ 1 HP, hết 3 HP thì thua). Trả lời đúng sẽ tung đòn laser rút máu Boss, rút cạn máu Boss thì thắng cuộc.
- **4 Kiểu thử thách**:
  1. **Ghép câu (Sentence Assembly)**: Boss ra câu tiếng Việt, các từ tiếng Anh kèm từ gây nhiễu xuất hiện theo nhịp. Người chơi chọn theo đúng cú pháp câu.
  2. **Câu khuyết (Fill-in-the-blank)**: Xem câu khuyết, gợi ý Cambridge và phiên âm IPA rồi gõ từ còn thiếu.
  3. **Từ vựng & Phát âm (Themed Vocab & Audio)**: Nghe phát âm bản xứ và gõ từ tiếng Anh tương ứng.
  4. **Sắp xếp đoạn văn (Paragraph Ordering)**: Sắp xếp các câu luận học thuật theo thứ tự mạch lạc logic.

### 4. 🧠 Thuật Toán Spaced Repetition (SuperMemo SM-2)
- Tự động ghi nhận tốc độ và độ chính xác để quy đổi ra điểm chất lượng $q \in [0, 5]$.
- Tự động điều chỉnh hệ số dễ dàng $EF$ và tính toán ngày cần ôn tập tiếp theo ($1 \rightarrow 6 \rightarrow I \times EF'$ ngày).
- **Sổ tay từ vựng hay sai & Chế độ Luyện Sai (Mistake Slayer)**: Tự động gom các từ yếu nhất của người chơi để tạo màn đấu Boss tùy chỉnh riêng biệt giúp khắc phục lỗ hổng kiến thức.

### 5. 🛠️ Level Editor Dành Cho Giáo Viên & Quản Lý User
- Phân quyền: **Học viên (`student`)** và **Giáo viên (`teacher`)**.
- Cho phép giáo viên tạo màn chơi riêng: Tùy chỉnh tên Boss, Avatar, thanh trượt BPM có nút **"Nghe Thử Nhịp"**, nhập câu hỏi cho cả 4 kiểu thử thách và xuất bản cho học sinh.

---

## 🚀 Hướng Dẫn Chạy & Deploy

```bash
# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Khởi chạy Web App & Backend
python run_server.py
```
👉 Truy cập: **`http://localhost:8000`**

### Tài khoản thử nghiệm 1 chạm:
- **Học viên**: `student` / `student123`
- **Giáo viên**: `teacher` / `teacher123`

### Chạy bản Pygame thuần:
```bash
python pygame_app/main.py
```
### Đóng gói WebAssembly:
```bash
pygbag pygame_app
```
