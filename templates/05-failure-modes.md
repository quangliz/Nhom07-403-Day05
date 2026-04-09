# Top 3 failure modes

---

| # | Trigger | Hậu quả | Mitigation |
|---|---------|---------|------------|
| 1 (`Important`) | User hỏi về dị ứng/nguyên liệu; menu data thiếu hoặc AI hallucinate -> AI trả lời tự tin "không có tôm" dù chưa chắc | User bị dị ứng thực phẩm, không biết AI đã sai vì câu trả lời nghe rất chắc chắn | (a) Chỉ trả lời dựa trên grounded data từ menu merchant - không suy luận; <br>(b) Disclaimer bắt buộc cho MỌI câu về nguyên liệu: "Xin xác nhận với quán nếu bạn có dị ứng"; <br>(c) Nếu field allergen trống -> tự động nói "Quán chưa cung cấp thông tin này" |
| 2 | Menu data stale: món đã hết hàng / đã ngừng bán nhưng AI vẫn tư vấn bình thường | User thêm vào giỏ, checkout rồi mới nhận thông báo hết hàng -> bực bội, drop-off | Sync real-time inventory từ hệ thống POS của merchant trước khi AI gợi ý; đánh dấu "Hết hàng" trong context truyền vào prompt |
| 3 | User hỏi ngoài phạm vi menu: giờ mở cửa, thời gian giao, chính sách đổi trả | AI bịa câu trả lời hoặc trả lời sai lệch -> User hiểu nhầm về SLA giao hàng | Intent classification: nếu câu hỏi không liên quan menu -> route sang FAQ tĩnh hoặc hiển thị "Vui lòng liên hệ quán trực tiếp" kèm SĐT/chat support |

---

## Cách nghĩ failure modes

- Failure #1: **User không biết → nguy hiểm nhất (health risk)**
- Failure #2: **Xảy ra rồi user mới biết → cần prevention**
- Failure #3: **User không biết → nguy hiểm nhất**

→ Cả 3 đều là **high severity**

---

## Severity × likelihood matrix

            Likelihood thấp          Likelihood cao
          ┌────────────────────┬────────────────────┐
Severity  │                    │                    │
cao       │   Áp coupon sai    │  Gợi ý sai món     │
          │                    │   Bịa FAQs         │
          │    Monitor + plan  │      FIX NGAY      │
          ├────────────────────┼────────────────────┤
Severity  │                    │                    │
thấp      │   Menu data stale  │                    │
          │   Accept           │                    │
          └────────────────────┴────────────────────┘
