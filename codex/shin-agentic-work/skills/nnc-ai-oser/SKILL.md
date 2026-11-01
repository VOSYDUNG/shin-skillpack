---
name: nnc-ai-oser
description: Áp phương pháp NNC OSER R2 trên Codex — thành lập Mission (mission-formation), xúc tiến kết quả (adaptive-delivery) và kernel ai-oser cho trạng thái, quyền, bằng chứng, checkpoint. Dùng khi người dùng nhắc NNC OSER/AI OSer, cần giữ Mission bền qua nhiều phiên hoặc phối hợp nhiều luồng việc. Không dựng đội, vai, model hay trần luồng cố định; Codex tự chọn làm trực tiếp hay subagent native.
---

# NNC OSER R2 trên Codex

Skill này là cầu nối mỏng tới phương pháp NNC OSER R2, không phải bản sao và không phải
bộ sinh đội. Nguồn chuẩn là [NNC OSER](https://github.com/VOSYDUNG/nnc-claude-plugins);
xem [nguồn và lý do thay thế](references/provenance.md). Khi nội dung ở đây khác nguồn
chuẩn, nguồn chuẩn thắng.

## Chọn đúng phần của phương pháp

- **Thành lập — `mission-formation`**: người dùng mới có ý tưởng mơ hồ, chưa rõ nên
  cấu hình, mua, tích hợp, tái dùng hay tự xây. Làm rõ việc thật → hiện trạng → tìm
  giải pháp có sẵn trước khi tự xây → thẻ quyết định → bản nháp Mission có thẩm quyền
  và tiêu chí nghiệm thu. Đề xuất không phải phê duyệt.
- **Xúc tiến — `adaptive-delivery`**: Mission đã rõ hoặc đã duyệt; cần xây, cấu hình,
  thử, phát hành, vận hành hay sửa. Chỉ chọn những cổng mà sản phẩm thật cần; nghiệm
  thu theo kết quả, không theo số task. Thay đổi hành vi hoặc acceptance đã duyệt là
  một Delta Mission rõ ràng.
- **Kernel — `ai-oser`**: khi cần trạng thái Mission bền, nguồn thẩm quyền, bằng chứng,
  checkpoint, Health/usage hoặc admission năng lực. Trên máy có NNC OSER, đọc Mission
  bằng `oser status --json` (hoặc công cụ MCP `oser_mission_read` nếu đã cấu hình theo
  tài liệu tích hợp Codex của OSER). Kernel ghi Mission, tham chiếu thực thi và biên
  nhận; nó không cấp quyền và không thay host điều phối agent.

Không có công cụ OSER trên máy thì vẫn áp phương pháp, nhưng nói rõ trạng thái Mission
chưa được ghi bền; không giả vờ đã có checkpoint.

## Thực thi bằng khả năng native của Codex

- Codex tự chọn làm trực tiếp, dùng tool, giao subagent hay chạy song song theo công
  việc và quyền đã có. Dùng cơ chế subagent/custom agent đúng như
  [tài liệu Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents) mô tả
  và như phiên hiện tại thực sự cung cấp.
- Không áp danh sách vai, đội, wave, model family, effort ladder hay trần luồng toàn
  cục. Số slot, model và quyền đọc từ phiên; không đoán ID model mới nhất, không ghi đè
  lựa chọn model toàn máy. `.codex/agents/*.toml` là bề mặt cấu hình của Codex, không
  phải yêu cầu đội của NNC.
- Mỗi việc giao có mục tiêu, nguồn, phạm vi được sửa, điều không được đụng, acceptance
  và giới hạn side effect. Agent chỉ sửa phạm vi được giao; người tích hợp kiểm chứng.
- Điều phối theo sự kiện: hoàn tất/blocker mở việc phụ thuộc. Còn việc độc lập thì làm;
  hết thì dùng event wait/yield của host. Không polling, sleep-and-retry hay lịch polling.
- Không bắt buộc công cụ hỏi riêng của Claude; trình bày cùng hợp đồng quyết định qua
  giao diện Codex đang dùng.

## Bằng chứng và tài liệu hiện hành

UNKNOWN giữ là UNKNOWN. Đã yêu cầu khác đã chạy; receipt khác outcome; test pass khác sử
dụng thực tế đạt. Hoàn tất cần bằng chứng mới, phù hợp và không còn việc/blocker chưa đối
soát. Giữ một báo cáo hiện hành mỗi repo theo quy ước của repo đó; bằng chứng chi tiết ở
workspace nghiệp vụ. Không tự cấp quyền production, gửi tin, thanh toán hay publish.

## Công cụ đi kèm (tùy chọn, không thuộc kernel)

- `scripts/sync_repos.py --manifest ABS_MANIFEST --workspace ABS_DIR`: xem trước kiểm kê
  repo GitHub; chỉ thêm `--apply` (clone/fast-forward thận trọng) khi pull nằm trong yêu
  cầu. Không stash/reset/rebase/push; repo bẩn, sai origin/nhánh hay lệch thì chặn.
- `scripts/measure_tokens.py SESSION_JSONL ...`: đếm token đã báo cáo trong transcript
  Codex được chỉ định, không xuất nội dung chat, không suy ra tiền hay phần trăm quota.
  Dữ liệu thiếu là unknown, không là 0.
