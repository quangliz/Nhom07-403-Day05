# XanhSM Food AI Chatbot

AI-powered chatbot cho ứng dụng XanhSM Food — tư vấn menu, allergen, gợi ý món theo sở thích.

## Cấu trúc dự án

```
/
├── frontend/                     # Next.js 16 (UX/UI Team)
│   ├── src/
│   │   ├── app/                  # App Router pages
│   │   ├── components/           # React components
│   │   ├── data/                 # Frontend mock data
│   │   ├── lib/                  # Utilities
│   │   └── types/                # Frontend-specific types
│   └── public/                   # Static assets
├── backend/                      # Single FastAPI app (:8000)
│   ├── main.py                   # App entrypoint
│   ├── config.py                 # Centralized path config
│   ├── agent/                    # LangGraph AI Agent (Agent Team)
│   │   ├── core.py
│   │   └── tools/                # Tool functions (menu, faq, order)
│   ├── routes/                   # API endpoints
│   │   ├── chat.py               # POST /chat, GET /merchants
│   │   ├── analytics.py          # GET /merchant/{id}/analytics
│   │   ├── feedback.py           # POST /feedback
│   │   ├── menu.py               # POST /merchant/{id}/menu/update
│   │   └── eval.py               # /eval/* endpoints
│   ├── eval/                     # Eval & logging (Eval Team)
│   │   ├── logger.py
│   │   ├── metrics/
│   │   └── scripts/
│   └── data/mock/                # Mock data JSON (Data Team)
├── packages/shared/              # Shared TypeScript types — KHÔNG tự sửa
├── docs/                         # Flowcharts, API contract
└── docker-compose.yml
```

## Khởi động local

```bash
docker-compose up --build
```

## API Endpoints chính

| Endpoint | Mô tả |
|---|---|
| `POST /chat` | Gửi câu hỏi → nhận ChatResponse |
| `GET /merchants` | Danh sách quán |
| `GET /merchant/{id}/analytics` | Dashboard metrics cho quán |
| `POST /feedback` | Ghi feedback từ user |
| `POST /eval/log` | Ghi EvalLog |
| `POST /eval/outcome` | Ghi kết quả conversion/ignored |
| `POST /eval/correction` | Ghi báo sai → alert merchant |
| `GET /eval/dashboard` | Dashboard tổng hợp metrics |

## Quy tắc Git

- Không push thẳng lên `main` hoặc `develop`
- `packages/shared/` → cần PR + 1 reviewer approve
- Mock Data Team phải done `data/mock/` trước Tuần 1
