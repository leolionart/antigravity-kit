---
name: jira-task-manager
description: Create and manage Jira tasks for the AI project, assign tasks to correct team members, assign to sprints, and link to appropriate Epics. Use when user wants to create, update, or manage Jira tickets.
---

# Jira Workflow — Tạo task và quản lý trên Jira

## Khi tạo task mới cho một sprint, bạn cần thực hiện đầy đủ các bước sau:

### Bước 1: Tạo Jira issue
- Dùng tool `mcp__MCP_DOCKER__jira_create_issue` với project_key `AI`.
- Điền đầy đủ thông tin: `summary`, `description` (dùng format Jira markup), `priority`, `labels`.
- **Quy tắc Assignee**:
  - Gán cho **Thiện** (`thien.lai@vexere.com`): Các tasks liên quan đến Langfuse, Logfire, truy cập Log, Tracing, Debug, Input/Output context metadata, hoặc Token.
  - Gán cho **Khánh** (`khanh.huynh@vexere.com`): Các tasks liên quan đến Knowledge Base, Article, Content, SOP, OmniAgent UI, tính năng giao diện người dùng (edit/xoá).

### Bước 2: Gán task vào đúng sprint trên Jira
- Dùng `mcp__MCP_DOCKER__jira_get_sprints_from_board` để tìm sprint ID hiện hành. Board ID của dự án AI thường là `168` (dùng `jira_get_agile_boards` nếu cần xác nhận lại).
- Lọc các sprint có `state: "active"` hoặc `state: "future"` để chọn đúng sprint (ví dụ: Sprint 17).
- Gán Sprint khi tạo task (thông qua `additional_fields` với `customfield_10107: <Sprint ID>`) hoặc cập nhật sau đó bằng `jira_update_issue`.
- **QUAN TRỌNG**: Chỉ tạo issue trên Jira mà KHÔNG gán vào sprint là chưa đủ. Phải đảm bảo task đã vào đúng Sprint (active) đang chạy.

### Bước 3: Link task vào Epic tương ứng
- Dùng `mcp__MCP_DOCKER__jira_search` để tìm các Epics đang mở trong dự án: `project = AI AND issuetype = Epic AND status != Done AND status != Closed`.
- Xác định Epic phù hợp dựa theo chủ đề task. Ví dụ hiện tại:
  - Các tasks về **Langfuse, Tracing, Log, Debug** -> Gán vào Epic liên quan tới "Debug & Tracing" (ví dụ: AI-439).
  - Các tasks về **Knowledge Base, SOP, Content** -> Gán vào Epic liên quan tới "Knowledge Deduplication" hoặc "Knowledge Enhancement" (ví dụ: AI-265).
- Sử dụng tool `mcp__MCP_DOCKER__jira_update_issue` với field `customfield_10103: <Epic_Key>` để gán vào Epic phù hợp (Không sử dụng `jira_link_to_epic` vì sẽ không đúng định dạng Epic Link của Jira).

### Bước 4: Cập nhật tài liệu Sprint Goal (Nếu cần)
- Thêm task vào file `docs/roadmaps/q1-2026/sprint-{N}-goal.md` (Tuỳ theo thư mục hiện tại).
- Cập nhật cả ở section "Việc mới" VÀ section "Tasks Details".

## Các lưu ý khác
- Luôn hỏi user muốn đưa vào sprint nào nếu có nhiều tuỳ chọn tương lai.
- Khi link issues (block, relate) với nhau dùng `jira_create_issue_link` — chú ý có thể fail nếu issue target chưa tồn tại.
- Board ID (168) và Sprint ID: luôn luôn nên query để lấy số liệu thực tế tại thời điểm đó thay vì hardcode chết số ID vì nó thay đổi hàng tuần.