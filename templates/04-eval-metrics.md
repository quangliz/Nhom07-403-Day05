# Eval metrics + threshold

## Precision hay recall?

☑ Precision — khi AI gợi ý/áp dụng thì phải đúng  
☐ Recall — tìm được hết mọi khả năng

**Tại sao?**  
Trong food ordering:
- Gợi ý sai món (cay → user không ăn được) → trải nghiệm xấu ngay
- Gợi ý món có chứa allergen → user không ăn được → trải nghiệm nguy hiểm
→ **False positive (gợi ý sai)** tệ hơn false negative

**Nếu sai ngược lại thì sao?**  
- Nếu optimize recall:
  - AI gợi ý quá nhiều món không cần biết phù hợp hay không → user mất niềm tin

---

## Metrics table

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| Accuracy câu trả lời về menu (so với ground truth từ merchant) | ≥92% | <80% trong 3 ngày liên tiếp |
| Response latency (end-to-end) | <10s (p95) | >15s thường xuyên |
| Cart conversion rate sau khi chat với AI | ≥30% | <15% sau 2 tuần |
| User satisfaction (thumbs up / tổng phản hồi) | ≥75% | <60% trong 1 tuần |
| Tỉ lệ AI tự nhận "không chắc" thay vì bịa | ≥95% với câu hỏi ngoài data | Phát hiện hallucination về allergen -> dừng ngay |

---

## Giải thích nhanh

- **Cart conversion rate** = metric quan trọng nhất → đo AI có “hiểu user” không  
- **User satisfaction** = tín hiệu trực tiếp của failure

---

## User-facing metrics vs internal metrics

| Metric | User thấy? | Dùng để làm gì |
|--------|-----------|-----------------|
| Accuracy câu trả lời về menu | ☐ Không | Internal kiểm soát độ đúng so với dữ liệu merchant |
| Response latency (end-to-end) | ☐ Không | Theo dõi performance, đảm bảo không vượt ngưỡng |
| Cart conversion rate | ☐ Không | Đo hiệu quả business của AI |
| User satisfaction (thumbs up) | ☑ Có | Thu feedback trực tiếp từ user |
| Confidence / "Không chắc" signal | ☑ Có | Tăng trust, tránh hallucination |

---

## Offline eval vs online eval

| Loại | Khi nào | Đo gì | Ví dụ |
|------|---------|-------|-------|
| **Offline** | Trước khi deploy | Accuracy trên data menu thật | So sánh câu trả lời AI vs menu merchant |
| **Online** | Sau khi deploy | Hành vi user thật | User có add vào cart sau khi chat không? |

**Nhận xét:**
- Offline accuracy cao nhưng conversion thấp → AI đúng nhưng không hữu ích
- Thiếu:
  - Feedback loop từ thumbs up/down
  - Tracking các case AI trả lời “không chắc”

---

## A/B test design

| Test | Variant A | Variant B | Metric theo dõi | Kết quả mong đợi |
|------|-----------|-----------|------------------|-------------------|
| Hiển thị trạng thái "không chắc" | Có hiển thị | Không hiển thị | Satisfaction, hallucination rate | Hiển thị → giảm hallucination |
| Tốc độ phản hồi | <10s | ~15s | Conversion rate | Nhanh hơn → tăng conversion |
| CTA sau trả lời AI | Có nút “Thêm vào giỏ” | Không có | Cart conversion rate | Có CTA → tăng chuyển đổi |

---

## Câu hỏi mở rộng

**Metric đo sớm nhất (day 1):**
- Response latency  
- Accuracy trên test set  

**Metric cần thời gian:**
- Cart conversion rate  
- User satisfaction  

---

**Nếu chỉ chọn 1 metric:**
→ **Cart conversion rate**

**Lý do:**
- Phản ánh trực tiếp AI có tạo ra giá trị kinh doanh hay không  
- Bao gồm cả: đúng + hữu ích + dễ dùng  

---

**Metric có bị “game” không?**

Có:
- AI trả lời “không chắc” quá nhiều → tránh sai nhưng vô dụng  
- AI trả lời chung chung → accuracy cao nhưng không giúp user quyết định  

→ Cần cân bằng:
- Accuracy + Conversion  
- “Không chắc” rate + User satisfaction  

---

## Threshold & Red flags

| Metric | Threshold | Red flag (dừng khi) |
|--------|-----------|---------------------|
| Accuracy câu trả lời về menu | ☐ Không | Internal kiểm soát độ đúng so với dữ liệu merchant |
| Response latency (end-to-end) | ☐ Không | Theo dõi performance, đảm bảo không vượt ngưỡng |
| Cart conversion rate | ☐ Không | Đo hiệu quả business của AI |
| User satisfaction (thumbs up) | ☑ Có | Thu feedback trực tiếp từ user |
| Confidence / "Không chắc" signal | ☑ Có | Tăng trust, tránh hallucination |