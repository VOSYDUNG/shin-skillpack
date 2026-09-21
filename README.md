# Shin Skill Pack

Bộ skill đóng gói một lần — nạp được vào Claude Code, Claude Desktop, claude.ai
Projects, ChatGPT, Grok, Gemini, Copilot, hoặc bất kỳ model nào nhận system prompt.

**23 skill, 4 nhóm.**

| Nhóm | Skill | Làm được gì |
|---|---|---|
| **Productivity** | 4 | Quản lý việc trong `TASKS.md`, dựng bộ nhớ hai tầng về người/dự án/thuật ngữ nội bộ, đồng bộ việc từ project tracker, dashboard HTML. |
| **Product Management** | 8 | Viết PRD/spec, cập nhật roadmap, lập kế hoạch sprint, tổng hợp user research, brief đối thủ, review chỉ số, cập nhật stakeholder. |
| **Operations** | 9 | Báo cáo tình hình, SOP & sơ đồ quy trình, runbook vận hành, đánh giá rủi ro, review nhà cung cấp, change request, kế hoạch năng lực, theo dõi tuân thủ, tối ưu quy trình. |
| **Artifact Toolkit** | 2 | Runtime capabilities của Artifact (kèm 12 file `.d.ts` bản 0.2.52) và quy tắc vẽ sơ đồ SVG. |

## Bắt đầu nhanh

**Claude Code / Claude Desktop** — repo này *chính là* một plugin marketplace:

```
/plugin marketplace add <github-user>/shin-skillpack
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
│   ├── productivity/                 (v1.3.1 · 4 skill · dashboard.html)
│   ├── product-management/           (v1.2.0 · 8 skill · 1 command)
│   ├── operations/                   (v1.3.0 · 9 skill)
│   └── artifact-toolkit/             (contract 0.2.52 · 2 skill · 12 .d.ts)
├── portable/                         ← SINH RA. Đừng sửa tay.
│   ├── ROUTER-ONLY.md                (~6 KB — bảng định tuyến, không kèm quy trình)
│   ├── productivity.bundle.md        (~24 KB)
│   ├── product-management.bundle.md  (~111 KB)
│   ├── operations.bundle.md          (~27 KB)
│   ├── artifact-toolkit.bundle.md    (~22 KB)
│   └── SHIN-ALL-IN-ONE.bundle.md      (~184 KB)
├── platforms/                        ← hướng dẫn nạp cho từng nền tảng
├── tools/
│   ├── build_portable.py             ← dựng lại portable/ từ plugins/
│   └── make_zip.ps1                  ← đóng gói dist/shin-skillpack-<ngày>.zip
└── dist/                             ← file zip (không commit)
```

Mỗi plugin giữ nguyên cấu trúc chuẩn của Claude Code:
`.claude-plugin/plugin.json`, `.mcp.json`, `CONNECTORS.md`, `README.md`,
`skills/<tên>/SKILL.md`, và `commands/` nếu có.

## Quy trình sửa đổi

Chỉ sửa trong `plugins/`, rồi dựng lại:

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

Xem [`NOTICE.md`](NOTICE.md). Tóm tắt: nội dung skill do Anthropic viết, phát hành theo
Apache-2.0; bộ này đóng gói lại, không sửa nội dung skill. Ảnh chụp ngày 2026-09-21 từ
marketplace `knowledge-work-plugins` và Claude Code 2.1.275.
