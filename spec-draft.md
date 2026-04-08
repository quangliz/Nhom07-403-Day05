# SPEC - AI Product Hackathon

**Nhóm:** 7
**Track:** XanhSM
**Problem statement (1 câu):** Khách hàng đặt đồ ăn thường có nhu cầu hỏi chi tiết về món ăn (vị có cay không, nguyên liệu có gây dị ứng không, còn hàng không) trước khi chốt đơn. Hiện tại XanhSM Food thiếu kênh kết nối trực tiếp, khiến khách dễ bỏ giỏ hàng. Việc dùng nhân sự trực chat tốn kém và chậm (2-3 phút/phản hồi). AI có thể đóng vai trò “nhân viên ảo” của quán, trả lời tức thì dựa trên dữ liệu menu và mô tả món ăn có sẵn.

---

## 1. AI Product Canvas

|             | **Value**                                                                                                                                                | **Trust**                                                                                                                                                                         | **Feasibility**                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **Trả lời** | **User:** Giải đáp thắc mắc ngay lập tức (<10s), tăng tự tin khi đặt hàng.<br>**Merchant:** Giảm tỉ lệ bỏ giỏ hàng, không tốn chi phí nhân sự trực chat. | AI bịa về nguyên liệu của món ăn và cho rằng nó không gây dị ứng với 1 người bị dị ứng -> người dùng bị dị ứng khi ăn. Luôn phải có câu "AI có thể có lỗi, vui lòng kiểm tra kỹ." | API call ~$0.005/lượt, latency <10s.<br>**Risk:** người dùng cung cấp thiếu thông tin. |

**Auto hay aug?** **Augmentation** - AI hỗ trợ tư vấn và giải đáp, quyết định đặt hàng vẫn ở người dùng.

**Learning signal:** Tỉ lệ khách hàng bấm “Thêm vào giỏ” ngay sau khi AI trả lời.

---

## 2. User Stories - 4 paths

Mỗi feature chính = 1 bảng. AI trả lời xong -> chuyện gì xảy ra?

### Feature: AI Tư Vấn Menu Thời Gian Thực

**Trigger:** User gõ câu hỏi vào chat box — có thể là về 1 món cụ thể ("Món này có cay không?") hoặc cross-menu ("Quán có món cơm nào không có thịt bò không?") -> AI tra cứu dữ liệu menu -> phản hồi trong <10s.

| Path | Câu hỏi thiết kế | Mô tả |
| --- | --- | --- |
| Happy - AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | User hỏi "Tôi bị dị ứng bò, quán có món cơm nào không có thịt bò không?" -> AI lọc menu: nhận diện allergen = bò + category = cơm -> trả lời "Các món cơm không có thịt bò: Cơm gà nướng, Cơm heo quay, Cơm tấm sườn. AI có thể có lỗi, vui lòng xác nhận với quán nếu dị ứng nặng." -> User chọn 1 món, bấm "Thêm vào giỏ". |
| Low-confidence - AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | Một số món cơm trong menu chưa có field nguyên liệu đầy đủ -> AI không thể xác nhận 100% -> Hiển thị: "Tôi tìm thấy Cơm chiên dương châu nhưng chưa có thông tin đầy đủ về nguyên liệu. Vì bạn bị dị ứng, hãy gọi quán xác nhận trước khi đặt: [SĐT]." -> User có lựa chọn an toàn. |
| Failure - AI sai | User biết AI sai bằng cách nào? Recover ra sao? | "Cơm bò lúc lắc" có tên gây nhầm, menu ghi "sốt bò" ở mô tả phụ -> AI bỏ sót -> Trả lời "Cơm bò lúc lắc không có thịt bò" -> User đặt, ăn, bị dị ứng. User không thể biết AI sai vì câu trả lời nghe hợp lý. <br>**Recover:** App hiển thị banner "Bạn có vấn đề với đơn này?" sau khi giao -> User báo cáo sự cố -> Merchant được notify ngay, món bị flag để review -> AI tạm thời trả lời "không chắc" cho món đó cho đến khi data được xác thực lại. Mitigation gốc: tìm kiếm cả trong mô tả phụ, không chỉ tên món. |
| Correction - user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | User bấm "Báo sai thông tin" -> chọn lý do "Món này có thịt bò" -> Ghi vào correction log kèm món + allergen bị sai -> Merchant nhận alert, review và cập nhật field nguyên liệu -> AI dùng data đã xác thực cho lần sau. |

### Feature: Gợi Ý Món Theo Sở Thích

**Trigger:** User chat "Tôi muốn ăn gì đó không cay, dưới 100k" -> AI lọc menu theo điều kiện -> trả về 2-3 gợi ý kèm ảnh & giá.

| Path | Câu hỏi thiết kế | Mô tả |
| --- | --- | --- |
| Happy - AI đúng, tự tin | User thấy gì? Flow kết thúc ra sao? | User chat "Tôi muốn ăn gì đó không cay, dưới 100k" -> AI trả về 3 card: mỗi card có ảnh món, tên, giá, tag "Không cay" + nút "Thêm vào giỏ" ngay trong chat -> User bấm thêm 1 món, không cần rời khỏi chat. |
| Low-confidence - AI không chắc | System báo "không chắc" bằng cách nào? User quyết thế nào? | Yêu cầu quá chung ("Cho tôi ăn ngon") -> AI hỏi lại 1 câu làm rõ: "Bạn thích cơm, bún hay mì? Ngân sách khoảng bao nhiêu?" -> User trả lời -> AI gợi ý lần 2 với đủ thông tin. Không hiển thị gợi ý mờ nhạt khi chưa đủ điều kiện lọc. |
| Failure - AI sai | User biết AI sai bằng cách nào? Recover ra sao? | AI gợi ý món đã hết hàng (inventory sync chậm) -> User bấm "Thêm vào giỏ" **ngay trong chat** -> Nhận thông báo lỗi "Món này tạm hết hàng" tại chỗ, không phải lúc checkout -> AI tự động gợi ý món thay thế tương tự còn hàng trong cùng response. <br>**Recover:** User chọn món thay thế ngay, không bị gián đoạn flow. |
| Correction - user sửa | User sửa bằng cách nào? Data đó đi vào đâu? | User bỏ qua cả 3 gợi ý, tự tìm và chọn món khác -> Implicit signal: {bỏ qua gợi ý, chọn món X} được ghi lại kèm context (điều kiện lọc) -> Dùng để re-rank gợi ý cho user tương tự sau này. |

---

## 3. Eval metrics + threshold

**Optimize precision hay recall?** Precision
Tại sao? Câu trả lời sai về nguyên liệu/dị ứng có thể gây hại sức khỏe người dùng. Thà nói "Tôi không chắc, hãy hỏi quán" còn hơn tự tin trả lời sai. Với bài toán tư vấn thực phẩm, false positive (AI nói "không có tôm" nhưng thực ra có) nguy hiểm hơn false negative (AI nói "không chắc" dù thực ra biết).
Nếu sai ngược lại thì chuyện gì xảy ra? Nếu chọn recall cao -> AI trả lời nhiều hơn nhưng hay sai -> User mất tin tưởng hoặc bị ảnh hưởng sức khỏe -> Merchant mất uy tín, XanhSM bị phản ánh.

| Metric | Threshold | Red flag (dừng khi) |
| --- | --- | --- |
| Accuracy câu trả lời về menu (so với ground truth từ merchant) | ≥92% | <80% trong 3 ngày liên tiếp |
| Response latency (end-to-end) | <10s (p95) | >15s thường xuyên |
| Cart conversion rate sau khi chat với AI | ≥30% | <15% sau 2 tuần |
| User satisfaction (thumbs up / tổng phản hồi) | ≥75% | <60% trong 1 tuần |
| Tỉ lệ AI tự nhận "không chắc" thay vì bịa | ≥95% với câu hỏi ngoài data | Phát hiện hallucination về allergen -> dừng ngay |

---

## 4. Top 3 failure modes

Liệt kê cách product có thể fail - không phải list features. "Failure mode nào user KHÔNG BIẾT bị sai? Đó là cái nguy hiểm nhất."

| # | Trigger | Hậu quả | Mitigation |
| --- | --- | --- | --- |
| 1 (`Important`) | User hỏi về dị ứng/nguyên liệu; menu data thiếu hoặc AI hallucinate -> AI trả lời tự tin "không có tôm" dù chưa chắc | User bị dị ứng thực phẩm, không biết AI đã sai vì câu trả lời nghe rất chắc chắn | (a) Chỉ trả lời dựa trên grounded data từ menu merchant - không suy luận; <br>(b) Disclaimer bắt buộc cho MỌI câu về nguyên liệu: "Xin xác nhận với quán nếu bạn có dị ứng"; <br>(c) Nếu field allergen trống -> tự động nói "Quán chưa cung cấp thông tin này" |
| 2 | Menu data stale: món đã hết hàng / đã ngừng bán nhưng AI vẫn tư vấn bình thường | User thêm vào giỏ, checkout rồi mới nhận thông báo hết hàng -> bực bội, drop-off | Sync real-time inventory từ hệ thống POS của merchant trước khi AI gợi ý; đánh dấu "Hết hàng" trong context truyền vào prompt |
| 3 | User hỏi ngoài phạm vi menu: giờ mở cửa, thời gian giao, chính sách đổi trả | AI bịa câu trả lời hoặc trả lời sai lệch -> User hiểu nhầm về SLA giao hàng | Intent classification: nếu câu hỏi không liên quan menu -> route sang FAQ tĩnh hoặc hiển thị "Vui lòng liên hệ quán trực tiếp" kèm SĐT/chat support |

---

## 5. ROI 3 kịch bản

Giả định: AOV (giá trị đơn trung bình) = 120.000 VND. Nhân sự trực chat hiện tại: 1 người, lương ~6tr/tháng (~200k/ngày). AI cost: ~$0.005/lượt hỏi, trung bình 3 lượt/user.

|  | Conservative | Realistic | Optimistic |
| --- | --- | --- | --- |
| **Assumption** | 200 user chat/ngày, giảm cart abandonment 3%, satisfaction 65% | 800 user chat/ngày, giảm cart abandonment 8%, satisfaction 78% | 2.500 user chat/ngày, giảm cart abandonment 15%, satisfaction 88% |
| **Cost AI** | 200 × 3 × $0.005 = $3/ngày (~75k VND) | 800 × 3 × $0.005 = $12/ngày (~300k VND) | 2.500 × 3 × $0.005 = $37.5/ngày (~940k VND) |
| **Benefit** | Tiết kiệm 200k/ngày nhân sự + 3% × (giả sử 500 visit) × 120k = +1.8tr/ngày | Tiết kiệm 200k + 8% × 2.000 visit × 120k = +19.4tr/ngày | Tiết kiệm 200k + 15% × 5.000 visit × 120k = +90.2tr/ngày |
| **Net/ngày** | ~+1.725tr (~+$69) | ~+19.1tr (~+$764) | ~+89.3tr (~+$3.570) |
| **Break-even** | Ngay từ ngày đầu | Ngay từ ngày đầu | Ngay từ ngày đầu |

**Kill criteria:** Dừng triển khai nếu: 

(a) cart conversion rate sau chat <15% sau 4 tuần liên tiếp, 

HOẶC (b) xảy ra sự cố allergen nghiêm trọng có thể quy kết về AI, 

HOẶC (c) merchant phàn nàn về data sai >10 lần/tuần mà chưa có fix.

---

## 6. Mini AI spec (1 trang)

**Sản phẩm giải gì, cho ai:**
XanhSM Food AI Chatbot là "nhân viên tư vấn ảo" 24/7 ngay trong luồng đặt hàng. Khách hàng thường bỏ giỏ hàng vì không biết món có phù hợp với mình không (cay, dị ứng, khẩu phần). Chatbot giải quyết tắc nghẽn này bằng cách trả lời tức thì (<10s) dựa trên dữ liệu menu thực từ merchant, thay thế hoàn toàn cho nhân sự trực chat tốn kém và chậm (2-3 phút/phản hồi).

**AI làm gì (Auto/Aug):**
Augmentation - AI tư vấn và giải đáp, nhưng quyết định cuối cùng (đặt hay không đặt, chọn món gì) vẫn ở người dùng. AI không tự thêm món vào giỏ, không tự checkout. Merchant vẫn là nguồn truth duy nhất về menu data.

**Quality target (Precision over Recall):**
Ưu tiên precision. Với mọi câu hỏi về allergen/nguyên liệu, AI chỉ trả lời dựa trên data có trong menu - nếu không có đủ thông tin, tự nhận "không chắc" và hướng user gọi trực tiếp cho quán. Threshold: accuracy ≥92%, latency <10s p95, cart conversion sau chat ≥30%.

**Risk chính:**
Hallucination về nguyên liệu dị ứng là risk số 1 - nguy hiểm vì user không biết AI đang sai và tự tin. Mitigation: grounded retrieval từ menu data, disclaimer bắt buộc, nút "Báo sai". Risk số 2: menu data stale (hết hàng) -> cần real-time inventory sync với POS.

**Data flywheel:**
Mỗi lần user bấm "Báo sai thông tin" hoặc bỏ qua gợi ý của AI -> correction log -> merchant review -> cập nhật menu data -> AI phản hồi chính xác hơn. Learning signal chính: tỉ lệ user bấm "Thêm vào giỏ" ngay sau khi AI trả lời. Khi signal này tăng, có nghĩa AI đang thực sự giúp user tự tin hơn trong quyết định đặt hàng.
