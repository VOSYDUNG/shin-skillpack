---
name: nnc-ai-oser
description: Con trỏ ngắn tới NNC OSER trên Codex — dùng khi người dùng nhắc NNC OSER/AI OSer, cần thành lập Mission, xúc tiến kết quả hoặc giữ Mission, quyền, bằng chứng bền qua nhiều phiên. Phương pháp nằm ở nguồn NNC OSER; skill này chỉ chỉ đường và ghi chú cài/MCP riêng của Codex.
---

# NNC OSER trên Codex — con trỏ

Phương pháp, Mission, quyền, bằng chứng, delegation native và điều phối theo sự kiện
nằm ở [NNC OSER](https://github.com/VOSYDUNG/nnc-claude-plugins). Đọc tại nguồn; skill
này không chép lại. Khi khác nguồn, nguồn thắng. Xem [nguồn và lịch sử thay thế](references/provenance.md).

| Cần | Đọc |
|---|---|
| Tuyên bố chung, cổng `MISSION_READY` | [docs/DECLARATION.md](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/DECLARATION.md) |
| Thành lập Mission (Workflow A) | [mission-formation](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/mission-formation/SKILL.md) + [qa-qc-mission](../qa-qc-mission/SKILL.md) |
| Xúc tiến kết quả (Workflow B) | [adaptive-delivery](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/adaptive-delivery/SKILL.md) |
| Kernel: trạng thái, quyền, bằng chứng | [ai-oser](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/plugins/nnc/skills/ai-oser/SKILL.md) |
| Thực thi việc như một agent | [shin-agentic-work](../shin-agentic-work/SKILL.md) |

## Ghi chú riêng Codex

- Trên máy có NNC OSER, đọc Mission bằng `oser status --json`, hoặc công cụ MCP
  `oser_mission_read` khi đã cấu hình theo
  [tài liệu tích hợp host](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/oser-r1/INTEGRATIONS.md).
  Không có công cụ OSER thì nói rõ Mission chưa được ghi bền; không giả vờ có checkpoint.
- Subagent/custom agent dùng đúng như
  [tài liệu Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents) và phiên
  hiện tại thực sự cung cấp. `.codex/agents/*.toml` là cấu hình của Codex, không phải
  yêu cầu đội của NNC.

## Công cụ đi kèm (tùy chọn, không thuộc kernel)

- `scripts/sync_repos.py --manifest ABS_MANIFEST --workspace ABS_DIR`: xem trước kiểm kê
  repo GitHub; chỉ thêm `--apply` (clone/fast-forward thận trọng) khi pull nằm trong yêu
  cầu. Không stash/reset/rebase/push; repo bẩn, sai origin/nhánh hay lệch thì chặn.
- `scripts/measure_tokens.py SESSION_JSONL ...`: đếm token đã báo cáo trong transcript
  Codex được chỉ định, không xuất nội dung chat, không suy ra tiền hay phần trăm quota.
  Dữ liệu thiếu là unknown, không là 0.
