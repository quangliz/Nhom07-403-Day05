## ROI 3 kịch bản

|   | Conservative | Realistic | Optimistic |
|---|-------------|-----------|------------|
| **Assumption** | 200 user chat/ngày, giảm cart abandonment 3%, satisfaction 65% | 800 user chat/ngày, giảm cart abandonment 8%, satisfaction 78% | 2.500 user chat/ngày, giảm cart abandonment 15%, satisfaction 88% |
| **Cost AI** | 200 × 3 × $0.005 = $3/ngày (~75k VND) | 800 × 3 × $0.005 = $12/ngày (~300k VND) | 2.500 × 3 × $0.005 = $37.5/ngày (~940k VND) |
| **Benefit** | Tiết kiệm 200k/ngày nhân sự + 3% × (giả sử 500 visit) × 120k = +1.8tr/ngày | Tiết kiệm 200k + 8% × 2.000 visit × 120k = +19.4tr/ngày | Tiết kiệm 200k + 15% × 5.000 visit × 120k = +90.2tr/ngày |
| **Net/ngày** | ~+1.725tr (~+$69) | ~+19.1tr (~+$764) | ~+89.3tr (~+$3.570) |
| **Break-even** | Ngay từ ngày đầu | Ngay từ ngày đầu | Ngay từ ngày đầu |

---

**Kill criteria:** Dừng triển khai nếu: 

(a) cart conversion rate sau chat <15% sau 4 tuần liên tiếp, 

HOẶC (b) xảy ra sự cố allergen nghiêm trọng có thể quy kết về AI, 

HOẶC (c) merchant phàn nàn về data sai >10 lần/tuần mà chưa có fix.

---

## Cost breakdown chi tiết

| Hạng mục | Cách tính | Ước lượng |
|----------|-----------|-----------|
| API inference | $0.005 × 3 lượt × số user/ngày | $3 → $37.5/ngày |
| Infrastructure | hosting + DB nhẹ | ~50k–200k/ngày |
| Nhân lực monitor | ~5–10 giờ/tuần | ~500k–1tr/tuần |
| Data correction | merchant update menu | thấp (manual) |
| **Tổng cost/ngày** | | ~100k → ~1tr |

---

## Benefit không quy đổi trực tiếp ra tiền

| Benefit | Đo bằng gì | Tại sao quan trọng |
|---------|-----------|-------------------|
| UX tốt hơn | Satisfaction score, session time | Giữ user ở lại app |
| Trust vào platform | % user quay lại dùng chat | Tránh churn |
| Data từ user interaction | correction log, click behavior | Tạo data flywheel |
| Merchant satisfaction | số complaint giảm | Giữ supply side |

---

## Time-to-value


Mất bao lâu từ khi deploy đến khi thấy benefit?

```
Tuần 1–2: User thử nghiệm, chưa tin AI → conversion chưa tăng rõ
Tuần 3–4: User quen → bắt đầu dùng thường xuyên → conversion tăng
Tháng 2+: Data correction tích lũy → AI chính xác hơn → ROI tăng mạnh
```

→ Stakeholder cần chấp nhận **delay ~2–4 tuần** trước khi thấy rõ impact

### Competitive moat

- Có moat nhẹ → data từ:
  - user hỏi gì
  - user sửa gì
  - user chọn món nào sau khi chat

- Nhưng:
  - Không hoàn toàn unique (platform khác cũng có thể thu)
  - Moat phụ thuộc vào **volume + tốc độ cải thiện data**

→ Nếu scale nhanh → có lợi thế  
→ Nếu không → dễ bị copy

### Câu hỏi mở rộng

- Nếu API cost giảm 10x → lợi nhuận tăng mạnh nhất ở **optimistic case**
- Product **cần critical mass (~500–800 user/ngày)** để thấy rõ benefit
- Kill criteria hiện tại là hợp lý — tập trung vào:
  - **conversion**
  - **trust (allergen risk)**

→ Đây là 2 yếu tố quyết định sống còn của product
