# Shin Agentic Work — Codex và ChatGPT

Plugin kỹ năng thuần cho agent thực thi việc thật, gồm 12 skill: `shin-agentic-work`,
`outcome-work-management`, `qa-qc-mission`, `nnc-ai-oser` và 8 phương pháp chuyên môn
chọn lọc. Không có MCP server hay connector tài khoản. Chỉ mang skill làm việc agentic;
dữ liệu và cấu hình hiện hành nằm tại repo sử dụng.

Ranh giới lớp: phương pháp, Mission, quyền, bằng chứng, delegation native và điều phối
theo sự kiện nằm ở [NNC OSER](https://github.com/VOSYDUNG/nnc-claude-plugins)
([tuyên bố chung](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/DECLARATION.md)).
Gói này dẫn link tới đó, không chép lại.

## Build

```powershell
python -X utf8 tools/build_codex_plugin.py
```

Đầu ra: `dist/codex/shin-agentic-work/` và `dist/shin-agentic-work.zip`.
ZIP gồm manifest portable `plugin.json`, manifest tương thích Codex
`.codex-plugin/plugin.json`, skills, giấy phép và checksum. Frontmatter các skill
upstream được bỏ trường chỉ dành cho Claude; link CONNECTORS được đưa về tài nguyên
cục bộ trong package. Không khai báo rằng connector đã được kết nối.

## Dùng trong Codex

Plugin được đưa vào personal marketplace và cài bằng
`codex plugin add shin-agentic-work@personal`. Bản cache đã cài mới là nguồn Codex đọc;
sau thay nguồn cần build, cập nhật bản local, cachebuster/reinstall theo plugin-creator.

Mở task mới để Codex nạp plugin. Ví dụ:

> Dùng shin-agentic-work cho Auto_ROK. Đọc docs/ROOT.md, chọn gói tiếp theo từ bằng
> chứng hiện hành, tự chọn làm trực tiếp hay giao subagent và cập nhật cùng báo cáo ROOT.

Không cần tạo lại mục tiêu đã chốt. Thí điểm hiện tại giới hạn offline; yêu cầu tiếp
theo phải có phạm vi và quyền tương ứng trước khi chạy runtime.

Skill `nnc-ai-oser` đi kèm là con trỏ ngắn tới NNC OSER, kèm ghi chú cài/MCP riêng của
Codex (`oser status --json`, `oser_mission_read`). `qa-qc-mission` lập tiêu chí nghiệm thu
kèm loại bằng chứng (tương thích `acceptance` của `oser init`), bất biến, phép kiểm QC và
điều chưa biết trước khi khóa Mission. Giao thức kích hoạt agent khác bằng ID nằm ở
`shin-agentic-work`; tài liệu khác tham chiếu skill đó thay vì chép. Bộ sinh đội cũ
`scripts/team.py` đã gỡ ngày 01/11/2026. Khối "NNC AI OSER MANAGED TEAM" còn trong repo
dự án cần xử lý riêng từng repo.

## ChatGPT

Theo [kiến trúc plugin OpenAI](https://developers.openai.com/plugins/concepts/plugins),
plugin có thể chỉ gồm skills và danh mục công khai dùng chung cho ChatGPT/Codex.
[Hướng dẫn đóng gói](https://developers.openai.com/plugins/build/plugins) phân biệt
manifest portable, tương thích Codex và nguồn local; khả năng dùng local khác nhau
theo giao diện. Package này chuẩn bị đủ hai manifest cho hướng đó.

Bản local cài trên máy không tự chứng minh đã cài trong tài khoản ChatGPT web.
Chưa submit hay publish công khai. Nếu giao diện ChatGPT của người dùng hỗ trợ import
plugin skills-only, có thể dùng ZIP này để thử. Nếu chưa có, dùng nội dung các SKILL
và ROOT brief làm tài liệu tham khảo trong Project; không giả định có quyền đọc ổ C:,
chạy shell hoặc spawn agent ở đó. Cần kiểm tra riêng trên đúng giao diện trước khi
tuyên bố ChatGPT đã dùng được plugin.
