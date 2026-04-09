# User Stories — 4 Paths

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

# Transition Flow giữa các Path

- **Happy → Failure:**  
  User tin AI nói đồ ăn không chứa allergen → thực tế có → mất niềm tin

- **Low-confidence → Happy:**  
  User chọn đúng món từ gợi ý → lần sau AI tăng confidence

- **Failure → Correction → Happy:**  
  User sửa gợi ý món → system học → lần sau gợi ý đúng hơn

- **Failure → Bỏ dùng:**  
  AI sai nhiều lần (liên tục gợi ý sai món) → user mất kiên nhẫn → churn

---

# Edge Cases

| Edge case | Dự đoán AI xử lý | UX nên phản ứng |
|----------|----------------|----------------|
| Input tiếng Anh (“no spicy food”) | Có thể hiểu sai | Hiển thị confirm: “Bạn muốn không cay?” |
| Input mơ hồ (“ăn gì cũng được”) | AI random gợi ý | Hiển thị popular + filter |
| Input quá ngắn (“ăn”) | Không đủ context | Yêu cầu user chọn thêm preference |
| User cố tình spam input | AI phản hồi sai lệch | Rate limit + fallback rule-based |
| Input quá dài (đoạn mô tả dài) | AI bỏ sót ý chính | Highlight keyword đã hiểu + cho edit |
| User đổi ý liên tục | AI bị nhiễu preference | Reset suggestion + hỏi lại nhu cầu chính |
| Hết món sau khi user chọn | AI vẫn recommend | Hiển thị “Hết hàng” + suggest thay thế |
| Coupon hết hạn nhưng vẫn hiển thị | AI không cập nhật real-time | Validate lại khi apply + thông báo rõ |
| Nhiều coupon conflict | AI chọn sai mã tốt nhất | Hiển thị so sánh giảm giá → user chọn |
| User có dị ứng (không khai báo trước) | AI không biết | Prompt hỏi thêm: “Bạn có dị ứng gì không?” |
| Menu thay đổi (giá / món) | AI dùng data cũ | Sync real-time + fallback server check |
| Network chậm / mất kết nối | AI timeout | Hiển thị loading + retry + fallback manual |
| User mới (không có history) | AI không cá nhân hóa được | Dùng popular items + onboarding hỏi nhanh |
| User cũ nhưng behavior thay đổi | AI vẫn dùng pattern cũ | Detect drift → giảm weight data cũ |
| Nhiều người dùng chung 1 account | Preference bị lệch | Cho chọn “Ai đang đặt món?” |
| User không để ý AI auto apply | Không hiểu vì sao giá thay đổi | Hiển thị breakdown giá + lý do |

---

# Câu hỏi mở rộng

- Nếu user sửa AI 5 lần liên tiếp → nên chuyển sang **augmentation mode** (chỉ gợi ý, không auto)
- User mới vs user cũ:
  - User mới → dùng rule-based + popular items
  - User cũ → dùng personalization
- Conflict data:
  - Nếu nhiều user có hành vi khác nhau → ưu tiên **user-specific data** hơn global model