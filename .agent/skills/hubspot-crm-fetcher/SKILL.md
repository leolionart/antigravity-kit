---
name: hubspot-crm-fetcher
description: Skill dùng để fetch trực tiếp dữ liệu contacts (leads) và tasks từ HubSpot CRM sử dụng CLI token.
---

# hubspot-crm-fetcher

Skill này cho phép Antigravity tự động trích xuất cấu hình auth từ HubSpot CLI config (`~/.hscli/config.yml`) để gọi vào REST API của HubSpot, từ đó lấy được danh sách Leads (Contacts) và Tasks.

## Cấu trúc Scripts
- `hs_auth_parser.py`: Đọc token từ file cấu hình của Local HubSpot CLI.
- `fetch_leads.py`: In ra Terminal danh sách Leads (Contact). Hỗ trợ param `--limit N` (mặc định 10).
- `fetch_tasks.py`: In ra Terminal danh sách Tasks. Hỗ trợ param `--limit N` (mặc định 10).

## Cách gọi (Usage)
Mỗi khi User yêu cầu: "lấy dữ liệu leads" hoặc "kiểm tra tasks ở hubspot", Agent gọi tool `run_command` tương ứng:
- Liệt kê Leads:
  `python3 .agent/skills/hubspot-crm-fetcher/scripts/fetch_leads.py --limit 10`
- Liệt kê Tasks:
  `python3 .agent/skills/hubspot-crm-fetcher/scripts/fetch_tasks.py --limit 10`

Thao tác này KHÔNG đòi hỏi Socratic Gate chặn lại nếu User đã ra lệnh trực tiếp lấy dữ liệu. Quá trình lấy dữ liệu Read-Only hoạt động tự động.

**Lưu ý cho AI:**
Luôn đảm bảo chạy từ thư mục Root Project.
Cần cài đặt `pyyaml` và `requests` trên máy trước khi chạy bằng lệnh: `pip3 install pyyaml requests`
