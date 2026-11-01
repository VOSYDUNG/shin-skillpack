# Shin Skill Pack

Bộ skill đóng gói một lần — nạp được vào Claude Code, Claude Desktop, claude.ai
Projects, ChatGPT, Grok, Gemini, Copilot, hoặc bất kỳ model nào nhận system prompt.

**24 skill tham khảo, 4 nhóm.** Gói Codex `shin-agentic-work` chọn 11 skill, gồm phương
thức kết quả, cầu nối NNC OSER R2 và các phương pháp chuyên môn cần thiết.

**Codex dùng trước:** xem [cách cài và sử dụng](platforms/codex.md).
Build bằng `python tools/build_codex_plugin.py`; ZIP nằm ở `dist/shin-agentic-work.zip`.
Điểm vào `shin-agentic-work` giữ ROOT gọn, giao agent theo sự kiện và cập nhật một
báo cáo hiện hành. Dữ liệu dự án và hồ sơ agent không đi vào package.

Định hướng: [Làm việc có trật tự để tạo kết quả thật](WORK-MANAGEMENT.md).
Skill mới `outcome-work-management` hướng dẫn hình thành mục tiêu, chọn phương pháp
theo câu hỏi và đầu ra cần có, rồi nối OKR quý, kế hoạch tháng/tuần/ngày,
mẫu việc tổng quát và checklist của từng lần thực hiện. Quy trình được tham khảo,
điều chỉnh và kiểm chứng qua sử dụng; không mặc định đúng chỉ vì đã được đóng gói.

| Nhóm | Skill | Làm được gì |
|---|---|---|
| **Productivity** | 5 | Nối mục tiêu với kế hoạch và kết quả thực tế; quản lý task, bộ nhớ, đồng bộ từ tracker và dashboard task đơn giản. |
| **Product Management** | 8 | Viết PRD/spec, cập nhật roadmap, lập kế hoạch sprint, tổng hợp user research, brief đối thủ, review chỉ số, cập nhật stakeholder. |
| **Operations** | 9 | Báo cáo tình hình, SOP & sơ đồ quy trình, runbook vận hành, đánh giá rủi ro, review nhà cung cấp, change request, kế hoạch năng lực, theo dõi tuân thủ, tối ưu quy trình. |
| **Artifact Toolkit** | 2 | Runtime capabilities của Artifact (kèm 12 file `.d.ts` bản 0.2.52) và quy tắc vẽ sơ đồ SVG. |

## Bắt đầu nhanh

**Claude Code / Claude Desktop** — repo này *chính là* một plugin marketplace:

```
/plugin marketplace add VOSYDUNG/shin-skillpack
/plugin install operations@shin-skillpack
```

**ChatGPT / Grok / Gemini** — dán file đã dẹt sẵn trong `portable/`:

- Ô instructions chật (Custom GPT giới hạn 8.000 ký tự) → dán `portable/ROUTER-ONLY.md`,
  tải các `*.bundle.md` lên làm knowledge file.
- Ô instructions rộng (Claude Project, system prompt) → dán thẳng một
  `portable/<nhóm>.bundle.md`.

Chi tiết từng nền tảng: [`platforms/`](platforms/).

## Cấu trúc

```
shin-skillpack/
├── .claude-plugin/marketplace.json   ← biến repo thành marketplace của Claude Code
├── plugins/                          ← NGUỒN. Sửa ở đây.
│   ├── productivity/                 (gốc v1.3.1 + bản chưng cất · 5 skill · dashboard.html)
│   ├── product-management/           (v1.2.0 · 8 skill · 1 command)
│   ├── operations/                   (v1.3.0 · 9 skill)
│   └── artifact-toolkit/             (contract 0.2.52 · 2 skill · 12 .d.ts)
├── portable/                         ← SINH RA. Đừng sửa tay.
│   ├── ROUTER-ONLY.md                (bảng định tuyến, không kèm quy trình)
│   ├── productivity.bundle.md
│   ├── product-management.bundle.md
│   ├── operations.bundle.md
│   ├── artifact-toolkit.bundle.md
│   └── SHIN-ALL-IN-ONE.bundle.md
├── platforms/                        ← hướng dẫn nạp cho từng nền tảng
├── tools/
│   ├── build_portable.py             ← dựng lại portable/ từ plugins/
│   └── make_zip.ps1                  ← đóng gói dist/shin-skillpack-<ngày>.zip
├── WORK-MANAGEMENT.md                ← thiết kế bản chưng cất và ví dụ
└── dist/                             ← file zip (không commit)
```

Mỗi plugin giữ nguyên cấu trúc chuẩn của Claude Code:
`.claude-plugin/plugin.json`, `.mcp.json`, `CONNECTORS.md`, `README.md`,
`skills/<tên>/SKILL.md`, và `commands/` nếu có.

## Quy trình sửa đổi

Sửa nguồn skill trong `plugins/` (chính sách đóng gói ở `tools/build_portable.py`), rồi dựng lại:

```bash
python tools/build_portable.py
```

Mọi file trong `portable/` là sản phẩm sinh ra — sửa tay sẽ mất ở lần build kế tiếp.

Đóng gói zip để gửi đi:

```powershell
.\tools\make_zip.ps1
```

Chạy được trên Windows PowerShell 5.1 lẫn PowerShell 7. Script build lại `portable/`, ghi
`SHA256SUMS.txt`, rồi nén ra `dist/`.

## Điều nên biết trước khi dùng

**Skill là quy trình, không phải dữ liệu.** Chúng nói cách viết một PRD, cách chấm rủi ro,
cách bố cục một status report. Chúng **không** biết gì về tổ chức của bạn: không biết cơ cấu kênh,
không biết quy tắc phạm vi số liệu, không biết yêu cầu ngôn ngữ. Nạp bối cảnh tổ chức
**song song** với bộ này, đừng thay thế.

**Placeholder `~~`.** Các skill cố ý không gắn với sản phẩm cụ thể: `~~project tracker` nghĩa
là Asana, Jira, Linear — cái nào bạn nối thì là cái đó. Trên nền tảng không có connector, skill
sẽ hỏi bạn dán dữ liệu vào. Xem `CONNECTORS.md` của từng plugin.

**Repo này không cấp quyền truy cập gì cả.** `.mcp.json` chỉ khai báo server nào skill mong
đợi. Mỗi connector vẫn phải tự OAuth riêng.

**Mất tính năng nạp-theo-nhu-cầu khi ra ngoài Claude.** Claude Code chỉ nạp skill khi cần;
nơi khác thì cả bundle nằm trong context mọi lượt, tốn token. Đó là cái giá của tính di động —
vì vậy hãy nạp đúng một nhóm cần dùng, đừng nạp all-in-one nếu không thật sự cần.

**`artifact-capabilities` không chạy ngoài Claude.** Nó mô tả runtime `window.claude` chỉ tồn
tại trong claude.ai Artifacts. Ngoài Claude, đọc như tài liệu tham khảo thiết kế —
xem [`PORTABILITY.md`](plugins/artifact-toolkit/skills/artifact-capabilities/PORTABILITY.md)
để biết cách quy đổi sang hạ tầng web thông thường.

## Nguồn gốc & giấy phép

Xem [`NOTICE.md`](NOTICE.md). Bộ gốc gồm các skill của Anthropic, ảnh chụp ngày
2026-09-21 từ marketplace `knowledge-work-plugins` và Claude Code 2.1.275.
Bản này bổ sung phương thức quản lý kết quả theo yêu cầu của Shin và điều chỉnh
các điểm tích hợp Productivity cùng chính sách bundle. Nguồn gốc và thay đổi
được ghi riêng; bản bổ sung chưa được chứng minh qua vận hành thực tế.
