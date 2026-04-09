# AI Product Canvas — XanhSM Food AI Chatbot

## Canvas

|   | Value | Trust | Feasibility |
|---|-------|-------|-------------|
| **Câu hỏi guide** | User nào? Pain gì? AI giải quyết gì mà cách hiện tại không giải được? | Khi AI sai thì user bị ảnh hưởng thế nào? User biết AI sai bằng cách nào? User sửa bằng cách nào? | Cost bao nhiêu/request? Latency bao lâu? Risk chính là gì? |
| **Trả lời** | **User:** Khách đặt đồ ăn trên XanhSM Food.<br>**Pain:** Không biết món có phù hợp (cay, dị ứng, còn hàng), phải chờ quán trả lời 2–3 phút → dễ bỏ giỏ.<br>**AI giải quyết:** Chatbot trả lời tức thì (<10s) dựa trên menu → giảm friction, tăng tỉ lệ đặt hàng. | **Sai nguy hiểm:** AI trả lời sai về nguyên liệu/dị ứng → user có thể bị ảnh hưởng sức khỏe.<br>**User biết sai:** Khó phát hiện ngay vì câu trả lời nghe hợp lý.<br>**Mitigation:** Luôn có disclaimer + fallback "không chắc".<br>**Correction:** User bấm "Báo sai" → log → merchant cập nhật → AI cải thiện. | **Cost:** ~$0.005 / request (~3 request/user).<br>**Latency:** <10s (p95).<br>**Risk:** hallucination về allergen, dữ liệu menu thiếu hoặc stale (hết hàng nhưng vẫn gợi ý). |

---

## Automation hay augmentation?

☑ Augmentation — AI gợi ý, user quyết định cuối cùng  

**Justify:**  
AI chỉ tư vấn và trả lời câu hỏi. User vẫn là người chọn món và đặt hàng.  
Nếu AI sai, user vẫn có cơ hội kiểm tra lại hoặc chọn phương án khác → giảm rủi ro so với automation.

---

## Learning signal

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | User correction đi vào đâu? | User bấm "Báo sai" → ghi vào correction log → merchant review → cập nhật menu → AI dùng data đã xác thực |
| 2 | Product thu signal gì để biết tốt lên hay tệ đi? | Implicit: tỉ lệ thêm vào giỏ sau chat<br>Explicit: thumbs up/down<br>Correction: user báo sai hoặc bỏ qua gợi ý |
| 3 | Data thuộc loại nào? | ☑ Domain-specific · ☑ Real-time · ☑ Human-judgment |

---

### Có marginal value không?

Có.  
- Dữ liệu về menu + hành vi chọn món sau chat là dữ liệu riêng của hệ thống  
- Đối thủ khó có vì phụ thuộc merchant + user interaction thực tế  
- Model chung không biết được pattern như: user hỏi gì → chọn món nào  

Đây là data có giá trị dài hạn (data flywheel)

---

## Cách dùng

1. Điền Value trước — chưa rõ pain thì chưa điền Trust/Feasibility  
2. Trust: trả lời 4 câu UX (đúng → sai → không chắc → user sửa)  
3. Feasibility: ước lượng cost, không cần chính xác — order of magnitude đủ  
4. Learning signal: nghĩ về vòng lặp dài hạn, không chỉ demo ngày mai  
5. Đánh [?] cho chỗ chưa biết — Canvas là hypothesis, không phải đáp án