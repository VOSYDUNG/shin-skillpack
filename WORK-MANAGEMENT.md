# Làm việc agentic để tạo kết quả thật

Tài liệu định hướng cho skill làm việc agentic, chưng cất từ Shin Skill Pack và yêu cầu của Shin.
Áp dụng có điều chỉnh theo bằng chứng; hiệu quả dài hạn còn cần thử trong thực tế.

## Kết quả và phương pháp

Mỗi việc trả lời: vì sao làm, đầu ra gì, cách nào phù hợp, ai thực hiện, biết đạt bằng
cách nào, sau đó quyết định gì. AI thực hiện gói đã giao; ROOT giữ mục tiêu và kiểm chứng.

| Điểm chưa rõ | Phương pháp có thể dùng | Đầu ra để chuyển bước |
|---|---|---|
| Cần thay đổi điều gì, cho ai? | Nhu cầu, hiện trạng, tổng hợp bằng chứng | Vấn đề/cơ hội, nguồn và điều chưa biết |
| Có hướng nào đáng thử? | Brainstorm: đặt khung, mở phương án, phản biện, thu hẹp | Các hướng, giả định, cách thử |
| Chọn mục tiêu nào? | So giá trị, phù hợp, cấp thiết, căn cứ, năng lực và đánh đổi | O đề xuất/đã chọn, lý do và phạm vi |
| Thế nào là đạt? | Phép đo/điều kiện nghiệm thu từ hiện trạng | KR có nguồn đo, hạn và người chịu trách nhiệm |
| Làm cách nào? | So giải pháp, spec, cải tiến quy trình hoặc thử giả định | Phương án/dự án/thử nghiệm có acceptance |
| Làm trong kỳ nào? | Phân rã đầu ra, phụ thuộc và năng lực | Kế hoạch quý/tháng/tuần/ngày khả thi |
| Ai làm? | Làm trực tiếp hoặc giao subagent native; chọn model/effort/context theo gói | Gói có chủ sở hữu, quyền và giới hạn |
| Đã tạo giá trị gì? | Kiểm chứng và review | Tiếp tục/đổi/dừng, bằng chứng và bước tiếp |

Brainstorm tạo phương án; chọn mục tiêu là quyết định riêng. Thiếu căn cứ thì kết quả
có thể là định hướng tạm và phép thử nhỏ. Mục tiêu đã chốt không cần khám phá lại.
Mỗi bước quan trọng ghi: câu hỏi → đầu vào → phương pháp và lý do → đầu ra → điều kiện
chuyển bước → nơi dùng đầu ra. Chỉ gọi skill chuyên môn khi cần.

## Kế hoạch và thực tế

Quý xác định kết quả và hướng ba tháng; tháng chọn deliverable và hướng từng tuần;
tuần cân đối đầu ra với năng lực; ngày sinh checklist con theo tình huống. Không lập
90 checklist khi lập quý. Các góc nhìn cùng tham chiếu một mã việc, không nhân bản.
Mẫu việc tổng quát có mục đích, trigger, đầu vào, bước mẫu, output và acceptance.

Phân biệt ý định, dự báo và thực tế. Phát sinh làm dời việc thì cập nhật forecast,
lý do và ảnh hưởng. Chưa đủ căn cứ thì ghi chưa xác định/có rủi ro. Task xong, output
được nghiệm thu và tác động KR là ba claim riêng. Routine nhỏ có thể tự báo cáo.

Công ty, Finance, bản thân và khám phá dùng chung khung nhưng có cách kiểm chứng phù
hợp. Finance tham chiếu sổ hiện có; không tạo sổ song song. Thử nghiệm có câu hỏi,
giới hạn và quyết định tiếp; thất bại có thể loại một hướng sai. Demo, code hay cuộc
gặp không tự chứng minh khách hàng hoặc tiền đã về. Không ép mọi việc phải tạo tiền.

## Workflow agentic và ROOT sạch

ROOT chọn kết quả/phương pháp → host chọn làm trực tiếp hay subagent → agent làm gói độc lập → handoff
ngắn → ROOT đối chiếu bằng chứng → cập nhật một báo cáo hiện hành.

ROOT đọc ít tài liệu khóa và một `docs/ROOT.md`. Agent có context mới, tối thiểu, tự đủ;
hồ sơ vận hành ở `workspace/agents/<package>/<role>/`. Handoff khoảng tối đa 40 dòng:
kết quả, file/output, kiểm tra thực sự chạy, evidence, giới hạn, blocker và bước tiếp.
Agent chỉ đọc trả nội dung để ROOT lưu khi cần; writer sở hữu file rõ; reviewer kiểm độc
lập sau thay đổi. Không đẩy transcript hoặc toàn bộ log lên ROOT.

Phương pháp, Mission, quyền, bằng chứng, delegation native và điều phối theo sự kiện
(không đội cố định, không polling) nằm ở [NNC OSER](https://github.com/VOSYDUNG/nnc-claude-plugins)
— xem [tuyên bố chung](https://github.com/VOSYDUNG/nnc-claude-plugins/blob/main/docs/DECLARATION.md);
tài liệu này không chép lại. Việc nhỏ hoặc phụ thuộc nối tiếp làm trực tiếp. Kích hoạt
agent khác bằng ID theo giao thức trong skill `shin-agentic-work`.

## Một tài liệu hiện hành

`docs/ROOT.md` chứa: kết quả/acceptance, nguồn khóa, facts có ngày và phạm vi, kế hoạch,
gói/chủ sở hữu/phụ thuộc, chỉ mục evidence, blocker, quyết định và bước tiếp theo.
ROOT mở bằng chứng từ đây; báo cáo không thay thế bằng chứng.

Cập nhật cùng đường dẫn. Khi thay đổi lớn, viết lại toàn bộ bố cục nhất quán, bỏ phần
lỗi thời. Không nối nhật ký sửa đổi, không v1/v2/final, không bắt lưu phiên bản quản lý
bằng tay. Số phiên bản kỹ thuật plugin chỉ phục vụ cài đặt. Log đo gốc/source identity
cần cho kiểm chứng nằm ở kho riêng; không sửa sự thật khi làm sạch phần tổng hợp.

## Gói sử dụng và thí điểm

Bộ này là skill làm việc agentic cho agent (Claude Code, Codex, Antigravity, host khác).
`shin-agentic-work` là điểm vào thực thi; `outcome-work-management` định hướng kết quả/phương
pháp và kế hoạch sau khi có Mission; `qa-qc-mission` chạy QA/QC sơ bộ trước khi khóa
Mission; `nnc-ai-oser` là con trỏ tới NNC OSER. Tám skill chuyên môn được đóng cùng: brainstorm, research synthesis, spec, sprint, metrics, process,
risk và runbook. Hướng dẫn: [platforms/codex.md](platforms/codex.md).

Nguồn package ở `codex/shin-agentic-work/`; build lấy thêm skill chuyên môn từ nguồn
trong repo. Không mang dữ liệu dự án, credentials hoặc connector tài khoản vào plugin.

Pilot Auto_ROK dùng mục tiêu và hợp đồng có sẵn; đầu mối `Auto_ROK/docs/ROOT.md`,
hồ sơ ở `workspace/agents/pilot/`. Thử luồng nghiên cứu nguồn → handoff → kiểm
độc lập → ROOT xác minh trong phạm vi offline. Kết quả chi tiết chỉ lưu tại ROOT dự án.
Pilot không tự cấp quyền live/input/mission tick/model-server/gửi tin/publish. Host thiếu
tool hoặc agent phải nói đúng giới hạn; đọc skill không có nghĩa các agent đã chạy.
