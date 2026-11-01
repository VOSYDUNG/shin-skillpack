# Nguồn và lý do thay thế

## Nguồn chuẩn

Phương pháp là NNC OSER R2 trong https://github.com/VOSYDUNG/nnc-claude-plugins
(MIT, NNC Lao Group; giấy phép giữ trong `../LICENSE`), đối chiếu tại commit
`94ddf8b5a7cd69a65a3bf54991486da70c2a0282`:

- `plugins/nnc/skills/mission-formation/SKILL.md` — thành lập Mission.
- `plugins/nnc/skills/adaptive-delivery/SKILL.md` — xúc tiến kết quả.
- `plugins/nnc/skills/ai-oser/SKILL.md` — kernel cho trạng thái, quyền, bằng chứng.
- `docs/DECLARATION.md` — tuyên bố chung; `docs/oser-r1/INTEGRATIONS.md` — tích hợp host,
  gồm cấu hình MCP cho Codex.

Skill Codex này chỉ trỏ tới các nguồn trên và nêu cách áp trên Codex. Không chép lại
nội dung chi tiết để tránh hai nguồn cho cùng một khái niệm.

## Thay thế ngày 01/11/2026

Bản trước (chuyển thể kiểu v4 từ commit `297310dcfb14678da16db38c000c7a3a60709921`) có
`scripts/team.py` sinh khối "NNC AI OSER MANAGED TEAM" vào `AGENTS.md`,
`.codex/config.toml`, `.codex/agents/*.toml` và `.codex/team.json`, kèm danh mục vai cố
định (`references/roles.md`), schema đội (`references/team-schema.md`), profile model
và trần luồng `max_parallel_children`.

Điều đó trái với OSER R2: kernel không áp đội, vai, model hay trần luồng toàn cục; host
tự chọn làm trực tiếp hay dùng subagent native theo tài liệu hãng. Hai bản cùng tồn tại
tạo hai nguồn mâu thuẫn cho một khái niệm. CEO đã duyệt thay thế (REPLACE). Đã gỡ
`team.py`, `test_team.py`, `roles.md`, `team-schema.md`; SKILL viết lại thành cầu nối mỏng.
Giữ `sync_repos.py` và `measure_tokens.py` vì không phục vụ sinh đội.

Khối "NNC AI OSER MANAGED TEAM" đã sinh trong các repo dự án không bị gỡ bởi thay đổi
này; mỗi repo xử lý riêng, đọc và hợp nhất hướng dẫn hiện có trước khi bỏ khối cũ.

## Tài liệu Codex

- https://learn.chatgpt.com/docs/agent-configuration/agents-md — lớp hướng dẫn global/repo.
- https://learn.chatgpt.com/docs/build-skills — khám phá skill user/repo.
- https://learn.chatgpt.com/docs/agent-configuration/subagents — subagent và custom agent.

Các trang trên là nguồn tham chiếu được OSER R2 nêu; bản cập nhật này không kiểm lại
nội dung trực tiếp ngày 01/11/2026. Hành vi thực tế đọc từ phiên Codex đang chạy.
