# API Contract — XanhSM Chatbot

> ⚠️ File này phải được toàn bộ nhóm đồng ý TRƯỚC khi bắt đầu code service.
> Mọi thay đổi cần tạo PR và được ít nhất 2 người review.

## Endpoints

### 1. POST /api/chat (ai-agent:8000)

**Request:**
```json
{
  "session_id": "string",
  "user_id": "string",
  "message": "string",
  "store_id": "string"
}
```

**Response:**
```json
{
  "log_id": "string",
  "message": "string",
  "confidence": "high | low | unsure",
  "disclaimer": "string | null",
  "cards": [
    {
      "item_id": "string",
      "name": "string",
      "price": 75000,
      "image_url": "string",
      "tags": ["Không cay", "Còn hàng"],
      "is_available": true
    }
  ],
  "action_buttons": []
}
```

### 2. POST /eval/log (evaluation:8002)
Ghi EvalLog — gọi NGAY sau khi AI Agent build xong response.

### 3. POST /eval/outcome (evaluation:8002)
Ghi user action sau khi nhận response.

### 4. POST /eval/correction (evaluation:8002)
Ghi báo sai thông tin từ user → trigger merchant alert.

## Schema xem tại: packages/shared/types/
