# GETSTART — AI Agent Configuration Playbook

> **MỤC ĐÍCH**: File này là **TÀI LIỆU HƯỚNG DẪN DÀNH CHO BẠN (AI AGENT)**. Bất cứ khi nào User (đặc biệt là các thành viên non-coder từ Vexere) yêu cầu "Hãy setup", "Getting started", hoặc mở dự án lần đầu, AI Agent phải tự động thực thi các bước dưới đây thay mặt cho User. Không yêu cầu User tự cấu hình thủ công bằng tay.

---

## ═══ PHẦN A: CẤU HÌNH BAN ĐẦU (Chỉ chạy một lần) ═══

---

## Bước 1: Khởi Tạo Môi Trường Làm Việc (Markdown Workspace)

Dự án này sử dụng rất nhiều tài liệu Markdown, Bảng biểu và sơ đồ. Vì User phần lớn là người làm product/vận hành, giao diện raw markdown sẽ rất khó đọc.

**Nhiệm vụ của AI:**
Hãy chủ động hỗ trợ User cài đặt Extension **Office Viewer** (hoặc Markdown Viewer tương đương) dành cho VSCode/Antigravity.
- Extension này biến trải nghiệm của VSCode giống như một trình soạn thảo văn bản (Word/Excel) chuyên nghiệp, hỗ trợ render các file `.md` thành giao diện đồ họa.
- Nếu bạn có khả năng thực thi dòng lệnh (`run_command`), hãy xin phép User để chạy trực tiếp lệnh cài đặt extenstion `Office Viewer` (Ví dụ: `code --install-extension cweijan.vscode-office`).
- Nếu không, hãy gửi một hướng dẫn bằng ngôn ngữ tự nhiên tối giản: Hướng dẫn họ vào mục Extensions trên VSCode và gõ "Office Viewer" để cài.

## Bước 2: Thiết Lập Các Submodule Chứa Knowledge Base (Tùy Chọn)

Dự án này (`.agent`) chỉ là phần Public chứa các công cụ và workflow chung. Mọi thông tin tuỳ biến của công ty/sản phẩm (ví dụ: `omniagent`, `product-kb`) nằm ở các Git Submodule riêng biệt trong thư mục `knowledge_base/` để bảo mật.

**Nhiệm vụ của AI:**
Hãy hỏi User xem họ có cần cấp quyền truy cập vào các Private Submodule của công ty không.
- Nếu User nói "Bỏ qua" hoặc "Không cần": Đi tiếp tới Bước 3.
- Nếu User cần thêm Submodule: Hướng dẫn nội dung lệnh `git submodule add <link-git> knowledge_base/<tên-thư-mục>` và kiểm tra giúp họ xem quá trình clone có bị lỗi quyền (Permission Denied) hay không. Trong trường hợp có các Submodule đã được thiết lập sẵn trong mã nguồn, hãy đề xuất chạy `git submodule update --init --recursive` thay cho User để đồng bộ dữ liệu.

## Bước 3: Tự Động Định Tuyến Cấu Hình MCP

Một trong những sức mạnh cốt lõi là MCP Servers (mcp-atlassian để giao tiếp với Jira/Confluence Vexere). User không cần nhớ đường dẫn của file cấu hình.

**Nhiệm vụ của AI:**
1. Đọc nội dung file template: `.agent/mcp_config.json`.
2. Kiểm tra Agent đang hoạt động là gì:
   - Nếu là **Gemini (Antigravity)**: Hãy tự động tìm (hoặc tạo) và ghi đè nội dung cấu hình MCP vào file hệ thống của Gemini: `~/.gemini/antigravity/mcp_config.json`.
   - Nếu là **Claude Code**: Hãy tạo/ghi cấu hình vào file `.mcp.json` ở thư mục gốc dự án.
3. Quét qua file cấu hình vừa tạo. Nếu phát hiện các token đang để trống (VD: `"YOUR_API_KEY"` ở mục JIRA_PERSONAL_TOKEN hoặc CONFLUENCE_PERSONAL_TOKEN), hãy hỏi User nhập Token vào khung chat.
4. Ngay khi User dán token vào khung chat, AI thay mặt User mở file config tương ứng và cập nhật Token đó (Đồng thời xác nhận lại nội dung `.mcp.json` - nếu có - đã được khai báo loại bỏ trong `.gitignore` để tránh rò rỉ bảo mật).

---

## ═══ PHẦN B: ĐỒNG BỘ TỰ ĐỘNG (Chạy mỗi khi bắt đầu session) ═══

---

## Bước 4: Đồng Bộ Submodules Trước Khi Làm Việc

> **Trigger**: Thực hiện bước này **mỗi lần bắt đầu một session làm việc mới**, ngay sau khi User mở dự án hoặc nói các câu như "bắt đầu làm việc", "mở project", "let's go", hoặc bất cứ khi nào AI lần đầu tiên được kích hoạt trong phiên đó.

Các submodule (`knowledge_base/omniagent`, `knowledge_base/product-kb`, v.v.) là nơi chứa tài liệu, SOP, và system prompt — được team cập nhật liên tục. Nếu không đồng bộ, AI sẽ làm việc trên dữ liệu cũ.

**Nhiệm vụ của AI:**

**Bước 4.1 — Cập nhật kit công cụ chính (`.agent`):**

Chạy lệnh sau để lấy phiên bản mới nhất của bộ agents/skills/workflows:
```bash
git -C .agent pull origin main
```
- Nếu thành công: ghi nhận im lặng, không cần báo cáo với User.
- Nếu thất bại (ví dụ: không có internet, lỗi conflict): bỏ qua, không làm gián đoạn workflow của User.

**Bước 4.2 — Cập nhật các private knowledge submodules:**

Chạy lệnh sau để kéo thay đổi mới nhất từ TẤT CẢ submodule:
```bash
git submodule update --remote --merge
```
- Nếu có submodule nào được cập nhật: báo ngắn gọn với User, ví dụ: *"Đã đồng bộ knowledge base mới nhất (omniagent, product-kb)."*
- Nếu không có gì thay đổi: tiếp tục im lặng.
- Nếu gặp lỗi quyền truy cập (Permission Denied / Authentication Failed): thông báo cho User rằng submodule đó cần được cấu hình SSH key hoặc token, rồi tiếp tục làm việc với dữ liệu hiện có.

**Bước 4.3 — Kiểm tra nhanh iCloud sync (chỉ trên macOS):**

Nếu môi trường là macOS và thư mục dự án nằm trong `~/Library/Mobile Documents/` (iCloud Drive), kiểm tra xem có file lock bị treo không:
```bash
ls .git/index.lock 2>/dev/null && echo "LOCK DETECTED" || echo "OK"
```
- Nếu phát hiện `index.lock`: chạy `./scripts/fix_git_sync.sh` hoặc xóa thủ công `rm .git/index.lock` và thông báo cho User.
- Nếu OK: tiếp tục.

**Toàn bộ bước 4 nên hoàn thành trong im lặng dưới 5 giây. Chỉ lên tiếng khi có cập nhật mới hoặc có lỗi cần User xử lý.**

---

## Bước 5: Báo Cáo Hoàn Tất Cho User

Sau khi hoàn thành các bước trên, gửi cho User một lời chào mừng bằng Tiếng Việt thật thân thiện, súc tích (Tối đa 5 dòng). Nội dung phản hồi nên nhắc nhở họ rằng bộ công cụ hiện đã sẵn sàng và họ có thể dùng các slash command như:
- `/brainstorm`
- `/jira-task-manager`
- `/confluence-publishing`
...

**Lưu ý cực kỳ quan trọng dành cho AI:** User không quan tâm đến kỹ thuật git clone hay symlink. Họ chỉ quan tâm đến kết quả cuối cùng là "Tôi đã sẵn sàng làm việc bằng các slash command". Hãy ẩn các bước kỹ thuật và tự động hóa toàn bộ.
