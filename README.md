# Atmos Weather Dashboard

Giao diện Streamlit phong cách dark navy dashboard, tham khảo bố cục Weather Dashboard của Yevhen Ledenov trên Dribbble:
https://dribbble.com/shots/19113627-Weather-Dashboard

## 3 chức năng
1. Thời tiết hiện tại: nhiệt độ, độ ẩm, gió, cảm giác như.
2. Dự báo 7 ngày: thẻ ngày, bảng dữ liệu, xuất CSV.
3. Phân tích xu hướng: biểu đồ nhiệt độ và xác suất mưa.

## Chạy trên Windows PowerShell (Python 3.10)
```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Mở http://localhost:8501.

Nếu không kích hoạt được venv, dùng trực tiếp:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Kiểm thử
```powershell
python -m pytest -q
```

Dữ liệu: Open-Meteo (cần Internet, không yêu cầu API key cho mục đích học tập phi thương mại).
