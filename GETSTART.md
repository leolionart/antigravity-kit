*Copy toàn bộ nội dung bên dưới và paste vào context của AI Agent để bắt đầu quá trình setup tự động.*

# GETSTART — AI Agent Configuration Playbook

> **DÀNH CHO AI AGENT ĐỌC**: Khi User nói "setup", "getting started", "bắt đầu", hoặc mở dự án lần đầu — hãy **tự thực thi toàn bộ** các bước dưới đây mà không hỏi xin phép. Chỉ dừng lại khi gặp blocker thực sự (lỗi kỹ thuật không tự xử lý được). User không cần biết chi tiết kỹ thuật — chỉ báo cáo kết quả cuối.

---

## ═══ BƯỚC 0: BOOTSTRAP (Chỉ cần khi folder hoàn toàn trống) ═══

> **Kiểm tra trước**: Nếu folder hiện tại đã có file `.gitmodules` hoặc thư mục `.agent/` → bỏ qua Bước 0, nhảy thẳng vào Phần A.

Nếu User đang đứng trước một folder trống hoàn toàn và chỉ có URL này, hãy tự chạy:

```bash
# Bước 0.1 — Khởi tạo git repo
git init
git commit --allow-empty -m "chore: init workspace"

# Bước 0.2 — Kéo bộ công cụ về (public, không cần SSH)
git submodule add https://github.com/leolionart/antigravity-kit.git .agent
git submodule update --init .agent
```

Sau khi xong, thư mục `.agent/` sẽ có đầy đủ agents, skills, workflows và file GETSTART.md này. Tiếp tục Phần A để hoàn thiện môi trường làm việc.

---

## ═══ PHẦN A: CẤU HÌNH BAN ĐẦU (Chỉ chạy một lần) ═══

---

## Bước 1: Cài Office Viewer cho VSCode

Chạy ngay lệnh sau mà không cần hỏi:
```bash
code --install-extension cweijan.vscode-office
```
- Thành công → tiếp tục im lặng.
- Lệnh `code` không tồn tại (không có VSCode CLI) → bỏ qua bước này, tiếp tục Bước 2.

---

## Bước 2: Thiết Lập Submodules

Dự án có **4 submodules** với URL cố định như sau. Thực hiện tuần tự:

### 2.1 — Kiểm tra submodule nào chưa init

```bash
git submodule status
```

Đọc output: dòng bắt đầu bằng `-` = chưa init, cần xử lý. Dòng bắt đầu bằng khoảng trắng hoặc `+` = đã có, bỏ qua.

### 2.2 — Kiểm tra SSH cho GitLab nội bộ

Ba submodules dùng SSH tới `gitlab.vexere.net`. Tự kiểm tra:
```bash
ssh -T git@gitlab.vexere.net
```

**Nếu trả về `Welcome to GitLab`** → SSH OK, nhảy thẳng sang 2.3.

**Nếu trả về `Permission denied`** → SSH chưa được cấu hình. Tự chạy:
```bash
# Tạo key nếu chưa có
ls ~/.ssh/id_ed25519.pub 2>/dev/null || ssh-keygen -t ed25519 -C "vexere-workspace" -N "" -f ~/.ssh/id_ed25519

# In public key ra để User copy
cat ~/.ssh/id_ed25519.pub
```
Sau đó báo User: *"Vui lòng copy đoạn key trên, vào [gitlab.vexere.net → Preferences → SSH Keys](https://gitlab.vexere.net/-/profile/keys) → Add new key → dán vào → Save. Xong thì nhắn tôi."*

Khi User xác nhận, chạy lại `ssh -T git@gitlab.vexere.net` để verify trước khi sang 2.3.

### 2.3 — Clone tất cả submodules

Nếu `.gitmodules` đã có đủ 4 entries (trường hợp clone từ repo gốc), chạy:
```bash
git submodule update --init --recursive
```

Nếu workspace là mới hoàn toàn (chưa có `.gitmodules`), chạy lần lượt:
```bash
git submodule add https://github.com/leolionart/antigravity-kit.git .agent
git submodule add git@gitlab.vexere.net:ai-context/product/omniagent.git knowledge_base/omniagent
git submodule add git@gitlab.vexere.net:ai-context/product/product-kb.git knowledge_base/product-kb
git submodule add git@gitlab.vexere.net:ai-context/product/n8n.git knowledge_base/n8n
git submodule update --init --recursive
```

Sau khi xong, kiểm tra lại:
```bash
git submodule status
```
Tất cả dòng phải bắt đầu bằng khoảng trắng (không còn `-`). Nếu submodule nào vẫn lỗi → báo tên cụ thể và lý do cho User.

---

## Bước 3: Cấu Hình MCP

Xác định AI đang chạy là loại nào rồi tự ghi config:

**Nếu là Claude Code** → tạo file `.mcp.json` ở thư mục gốc dự án bằng cách copy từ template:
```bash
cp .agent/mcp_config.json .mcp.json
# Đảm bảo .mcp.json đã có trong .gitignore
grep -q '.mcp.json' .gitignore || echo '.mcp.json' >> .gitignore
```

**Nếu là Gemini (Antigravity)** → ghi vào file hệ thống:
```bash
mkdir -p ~/.gemini/antigravity
cp .agent/mcp_config.json ~/.gemini/antigravity/mcp_config.json
```

Sau khi copy, đọc file config vừa tạo. Tìm các trường còn placeholder (`YOUR_API_KEY`). Nếu phát hiện, báo User một lần duy nhất:

> *"Cần điền 2 token để kết nối Jira/Confluence:*
> *• **JIRA_PERSONAL_TOKEN**: Vào [jira.vexere.net → Profile → Personal Access Tokens](https://jira.vexere.net/secure/ViewProfile.jspa) → tạo token mới*
> *• **CONFLUENCE_PERSONAL_TOKEN**: Tương tự tại [docs.vexere.net](https://docs.vexere.net)*
> *Dán cả 2 token vào đây, tôi sẽ cập nhật config ngay."*

Khi User dán token → tự mở file config và thay thế placeholder bằng giá trị thực. Không hỏi thêm.

---

## ═══ PHẦN B: ĐỒNG BỘ TỰ ĐỘNG (Chạy đầu mỗi session) ═══

---

## Bước 4: Đồng Bộ Submodules Khi Bắt Đầu Làm Việc

> **Trigger tự động**: Chạy bước này **mỗi khi bắt đầu session mới** — không cần User yêu cầu. Thực hiện ngầm trong nền.

```bash
# Cập nhật kit công cụ
git -C .agent pull origin main --quiet

# Cập nhật toàn bộ knowledge bases
git submodule update --remote --merge --quiet

# Kiểm tra iCloud lock (macOS)
[ -f .git/index.lock ] && rm .git/index.lock && echo "Đã gỡ iCloud lock"
```

- Nếu có submodule được cập nhật → báo ngắn: *"Đã đồng bộ knowledge base mới nhất."*
- Nếu không có gì thay đổi → im lặng hoàn toàn.
- Nếu lỗi SSH/quyền → bỏ qua submodule đó, làm việc tiếp với dữ liệu hiện có, ghi chú cuối session.

---

## Bước 5: Chào Mừng

Sau khi hoàn thành Phần A (lần đầu) hoặc Phần B (các session tiếp theo), gửi một tin nhắn tiếng Việt ngắn gọn (≤5 dòng) xác nhận workspace đã sẵn sàng và nhắc các lệnh hay dùng: `/brainstorm`, `/jira-task-manager`, `/confluence-publishing`.

> **Nguyên tắc tối thượng**: Ẩn hoàn toàn các thao tác kỹ thuật. User chỉ thấy kết quả. Chỉ hỏi khi thực sự bị chặn và không có cách nào tự xử lý.
