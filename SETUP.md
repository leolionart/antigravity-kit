# Hướng Dẫn Cấu Hình Đăng Nhập

Tài liệu này hướng dẫn cách cấu hình xác thực cho:
- Jira
- Confluence

Mục tiêu là để user có thể tự đăng nhập hoặc tự điền token mà không cần sửa nhiều trong repo.

## Tổng Quan Nhanh

Trong workspace này sử dụng token và lưu trong file cấu hình local của workspace để xác thực Jira/Confluence.

## 1. Cấu Hình Jira Và Confluence

Helper Jira trong repo này đọc cấu hình từ file local:

```bash
./.agent/mcp_config.json
```

Đây là file cấu hình riêng của máy đang dùng, không nên commit lên git.

### Bước 1: Tạo file cấu hình local

Copy file mẫu (nếu chưa có):

```bash
cp .agent/mcp_config.example.json .agent/mcp_config.json
```

### Bước 2: Mở file và điền token

Mở file:

```bash
./.agent/mcp_config.json
```

Điền các giá trị sau:

- `JIRA_PERSONAL_TOKEN`
- `CONFLUENCE_PERSONAL_TOKEN`

Các URL mặc định đã được điền sẵn:

- `https://jira.vexere.net/`
- `https://docs.vexere.net/`

### Lấy token ở đâu

#### Jira

Truy cập:

```text
https://jira.vexere.net/secure/ViewProfile.jspa
```

Sau đó tạo `Personal Access Token` mới.

#### Confluence

Truy cập:

```text
https://docs.vexere.net
```

Sau đó vào phần hồ sơ cá nhân và tạo `Personal Access Token`.

### Kiểm tra đã cấu hình Jira thành công chưa

Sau khi điền token xong, chạy:

```bash
./.agent/skills/jira-task-manager/helpers/jira-mcp jira-search --jql "project = AI ORDER BY updated DESC" --limit 5 --output json
```

Nếu lệnh trả về danh sách issue dạng JSON thì cấu hình Jira đã hoạt động.

## 2. Nếu Đang Dùng Claude Code Hoặc Gemini

File `./.agent/mcp_config.json` là file local để các helper trong repo này sử dụng.

Nếu cần đồng bộ cấu hình đó sang công cụ đang dùng, làm như sau:

### Claude Code

```bash
cp .agent/mcp_config.json .mcp.json
```

### Gemini

```bash
mkdir -p ~/.gemini/antigravity
cp .agent/mcp_config.json ~/.gemini/antigravity/mcp_config.json
```
