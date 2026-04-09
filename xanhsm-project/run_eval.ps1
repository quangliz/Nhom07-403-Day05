# Tệp chạy tự động cho dịch vụ Chatbot và Evaluation
$ErrorActionPreference = "Stop"

# 0. Kiểm tra API Key (OpenAI)
if (-not (Test-Path -Path ".env")) {
    Write-Host "CẢNH BÁO: Không tìm thấy file .env!" -ForegroundColor Red
    Write-Host "Hệ thống cần OPENAI_API_KEY để chạy mô hình gpt-4o-mini."
    Write-Host "Đang tự động tạo file .env mẫu cho bạn..." -ForegroundColor Yellow
    Set-Content -Path ".env" -Value "OPENAI_API_KEY=your_openai_api_key_here"
    Write-Host "Vui lòng mở file .env, nhập API Key thật của bạn vào rồi chạy lại script này." -ForegroundColor Cyan
    exit 1
}

$envContent = Get-Content -Path ".env" | Out-String
if ($envContent -match "your_openai_api_key_here") {
    Write-Host "LỖI: Trông có vẻ bạn chưa cấu hình OPENAI_API_KEY trong tệp .env." -ForegroundColor Red
    Write-Host "Vui lòng cập nhật API Key vào file .env rồi thử lại." -ForegroundColor Cyan
    exit 1
}

# 1. Khởi tạo môi trường ảo (nếu chưa có)
if (-not (Test-Path -Path "venv")) {
    Write-Host "Đang khởi tạo môi trường ảo venv..." -ForegroundColor Cyan
    python -m venv venv
}

# 2. Kích hoạt môi trường (thêm đường dẫn phù hợp cho Windows)
Write-Host "Kích hoạt môi trường ảo..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# 3. Cài đặt các thư viện cần thiết
Write-Host "Cài đặt thư viện (requirements)..." -ForegroundColor Cyan
pip install -r "services\ai-agent\requirements.txt" -q
pip install -r "services\evaluation\requirements.txt" -q

# 4. Chạy Evaluation Service ngầm trên nhánh port 8002
Write-Host "Khởi động Evaluation Service trên port 8002..." -ForegroundColor Yellow
$EvalProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "-m uvicorn main:app --app-dir services\evaluation --host 0.0.0.0 --port 8002 --reload"
Start-Sleep -Seconds 3

# 5. Chạy AI Agent Service ngầm trên nhánh port 8000
Write-Host "Khởi động AI Agent Service trên port 8000..." -ForegroundColor Yellow
$env:EVAL_SERVICE_URL="http://localhost:8002"
$AgentProcess = Start-Process -NoNewWindow -PassThru -FilePath "python" -ArgumentList "-m uvicorn main:app --app-dir services\ai-agent --host 0.0.0.0 --port 8000 --reload"
Start-Sleep -Seconds 5

# 6. Chạy Offline Eval runner code
Write-Host "`nĐang chạy kịch bản Evaluation hệ thống Offline (Anti-Game / Precision)..." -ForegroundColor Green
$env:AGENT_URL="http://localhost:8000"
$env:EVAL_URL="http://localhost:8002"
python "services\evaluation\scripts\offline_eval_runner.py"

# Dừng lại đợi
Write-Host "`n======================================================="
Write-Host "Đã hoàn thành chạy Test. Các server đang chạy ngầm."
Write-Host "Nhấn phím [ENTER] để tắt tất cả các server và thoát."
Write-Host "======================================================="
Read-Host

# 7. Tắt tiến trình
Write-Host "Đang tắt các server..." -ForegroundColor Cyan
Stop-Process -Id $EvalProcess.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $AgentProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "Đã tắt thành công." -ForegroundColor Green
