"""Weather Dashboard — Streamlit UI inspired by modern weather dashboard layouts."""
from __future__ import annotations

from datetime import datetime
from html import escape

import altair as alt
import pandas as pd
import requests
import streamlit as st

from weather_service import CITIES, daily_rows, describe_weather, get_forecast

st.set_page_config(
    page_title="Atmos • Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
html, body, [class*="css"], [data-testid="stApp"] {font-family:'DM Sans',sans-serif;}
[data-testid="stApp"] {background:linear-gradient(130deg,#0a1428 0%,#101d35 60%,#0b1629 100%);color:#f0f5ff;}
[data-testid="stSidebar"] {background:#0b172b;border-right:1px solid #263550;}
[data-testid="stSidebar"] * {color:#e7edfa;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1480px;padding:2rem 3.2rem 3rem;}
h1,h2,h3 {color:#f5f7ff!important;letter-spacing:-.035em;}
p, label {color:#b7c6df;}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {color:#aebed8;}
/* Sidebar select: dark background and readable text */
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color:#1e3352 !important;
    border:1px solid #47658c !important;
    border-radius:10px !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] span {
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
    opacity:1 !important;
}
.location-title {background:#1e3352;color:#fff;font-size:1.17rem;font-weight:700;padding:8px 12px;border-radius:10px;margin:12px 0 8px;}
.stButton>button {background:#263b5b;border:1px solid #405579;color:#fff;border-radius:13px;}
.stButton>button:hover {background:#355078;color:#fff;border-color:#5e7aa7;}
[data-testid="stTabs"] button {color:#b8c9e5;font-weight:700;}
[data-testid="stTabs"] button[aria-selected="true"] {color:#87bbff;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {background:#74aaff;}
[data-testid="stDataFrame"] {border-radius:15px;overflow:hidden;}
div[data-testid="stAlert"] {border-radius:14px;}
.hero {background:radial-gradient(circle at 88% 12%,rgba(153,207,255,.26),transparent 34%),linear-gradient(115deg,#3168b2,#203c7b 65%,#162c58);
 border:1px solid #5276b3;border-radius:26px;padding:32px 36px;box-shadow:0 18px 55px #050d1c40;min-height:275px;}
.eyebrow {font-size:12px;text-transform:uppercase;letter-spacing:.16em;color:#bcd7ff;font-weight:800;}
.hero-location {font-size:29px;font-weight:800;margin:8px 0 3px;color:#fff;}
.hero-temp {font-size:77px;line-height:1.15;font-weight:800;letter-spacing:-.07em;color:#fff;}
.hero-status {font-size:17px;color:#e4efff;}
.hero-symbol {font-size:84px;text-align:center;padding-top:40px;filter:drop-shadow(0 12px 20px #102d6477);}
.panel {background:#15243c;border:1px solid #2b3d58;border-radius:20px;padding:21px 23px;margin:9px 0 16px;}
.panel-title {color:#aabbd5;font-size:13px;font-weight:700;letter-spacing:.03em;}
.panel-value {font-size:29px;color:#fff;font-weight:800;margin-top:8px;}
.panel-sub {color:#9aacca;font-size:12px;margin-top:5px;}
.day-card {background:#15243c;border:1px solid #30435f;border-radius:18px;padding:18px 10px;text-align:center;min-height:181px;}
.day-name {font-size:13px;color:#bdcce3;font-weight:700;}
.day-icon {font-size:34px;margin:12px 0;}
.day-high {font-size:19px;color:white;font-weight:800;}
.day-low {font-size:13px;color:#9db1cd;}
.day-rain {font-size:12px;color:#8cc4ff;margin-top:8px;}
.section-label {font-size:19px;font-weight:800;color:#f5f7ff;margin:20px 0 12px;}
.small-note {color:#91a6c4;font-size:12px;}
.brand {font-size:28px;font-weight:800;color:#f3f7ff;letter-spacing:-.05em;margin:0 0 12px;}
.brand span {color:#83b9ff;}
div[data-testid="stVegaLiteChart"] {background:#15243c;border:1px solid #2b3d58;border-radius:18px;padding:10px;}
@media(max-width:800px){.block-container{padding:1rem}.hero{padding:20px;min-height:240px}.hero-temp{font-size:60px}.hero-symbol{font-size:56px}}
</style>
""", unsafe_allow_html=True)


def safe(value: object) -> str:
    return escape(str(value))


def number(value: object, digits: int = 0) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "—"


@st.cache_data(ttl=900, show_spinner=False)
def load_weather(lat: float, lon: float) -> dict:
    return get_forecast(lat, lon, days=7)


with st.sidebar:
    st.markdown('<div class="brand">☁️ at<span>mos.</span></div>', unsafe_allow_html=True)
    st.caption("WEATHER INTELLIGENCE")
    st.divider()
    st.markdown('<div class="location-title">📍 Địa điểm</div>', unsafe_allow_html=True)
    city = st.selectbox("Chọn thành phố", list(CITIES), label_visibility="collapsed")
    st.markdown("### ⚙️ Tùy chọn")
    if st.button("↻  Làm mới dự báo", use_container_width=True):
        load_weather.clear()
        st.rerun()
    st.divider()


st.markdown("## Weather Dashboard")
st.caption("Tổng quan thời tiết • Dự báo và phân tích trong một giao diện")

try:
    with st.spinner("Đang cập nhật thời tiết..."):
        payload = load_weather(*CITIES[city])
        rows = daily_rows(payload)
        current = payload["current"]
except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
    st.error(f"Không thể tải dữ liệu thời tiết: {exc}")
    st.info("Hãy kiểm tra kết nối Internet và nhấn 'Làm mới dự báo' để thử lại.")
    st.stop()

status, icon = describe_weather(current.get("weather_code"))
updated = current.get("time", "")
try:
    updated = datetime.fromisoformat(updated).strftime("%H:%M • %d/%m/%Y")
except ValueError:
    updated = "Không xác định"

left, right = st.columns([3, 1], vertical_alignment="center")
with left:
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">THỜI TIẾT HIỆN TẠI · {safe(updated)}</div>
      <div class="hero-location">📍 {safe(city)}</div>
      <div class="hero-temp">{number(current.get('temperature_2m'))}°</div>
      <div class="hero-status">{safe(status)} · Cảm giác như {number(current.get('apparent_temperature'))}°C</div>
    </div>
    """, unsafe_allow_html=True)
with right:
    st.markdown(f'<div class="hero" style="text-align:center"><div class="eyebrow">ĐIỀU KIỆN</div><div class="hero-symbol">{icon}</div><div class="hero-status">{safe(status)}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">Chỉ số thời tiết</div>', unsafe_allow_html=True)
metrics = [
    ("🌡️ Nhiệt độ", number(current.get("temperature_2m"), 1) + " °C", "Nhiệt độ đo gần mặt đất"),
    ("💧 Độ ẩm", number(current.get("relative_humidity_2m")) + " %", "Độ ẩm tương đối"),
    ("🌬️ Tốc độ gió", number(current.get("wind_speed_10m"), 1) + " km/h", "Gió ở độ cao 10 m"),
    ("☀️ Cảm giác như", number(current.get("apparent_temperature"), 1) + " °C", "Nhiệt độ cảm nhận"),
]
for col, (title, value, note) in zip(st.columns(4), metrics):
    with col:
        st.markdown(f'<div class="panel"><div class="panel-title">{title}</div><div class="panel-value">{safe(value)}</div><div class="panel-sub">{note}</div></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠  Tổng quan", "📅  Dự báo 7 ngày", "📈  Phân tích xu hướng"])

with tab1:
    st.markdown('<div class="section-label">Dự báo 7 ngày tới</div>', unsafe_allow_html=True)
    for col, row in zip(st.columns(7), rows):
        date = datetime.strptime(row["Ngày"], "%d/%m/%Y")
        icon_day = row["Tình trạng"].split(" ", 1)[0]
        rain = number(row["Khả năng mưa (%)"])
        with col:
            st.markdown(f"""<div class="day-card">
            <div class="day-name">{date.strftime('%d/%m')}</div>
            <div class="day-icon">{icon_day}</div>
            <div class="day-high">{number(row['Cao nhất (°C)'])}°</div>
            <div class="day-low">{number(row['Thấp nhất (°C)'])}° thấp</div>
            <div class="day-rain">💧 {rain}%</div></div>""", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Điểm nổi bật trong tuần</div>', unsafe_allow_html=True)
    hottest = max(rows, key=lambda r: r["Cao nhất (°C)"] if r["Cao nhất (°C)"] is not None else -999)
    rainiest = max(rows, key=lambda r: r["Khả năng mưa (%)"] if r["Khả năng mưa (%)"] is not None else -1)
    a, b = st.columns(2)
    with a:
        st.info(f"☀️ Nhiệt độ cao nhất: **{number(hottest['Cao nhất (°C)'], 1)}°C** vào {hottest['Ngày']}.")
    with b:
        st.info(f"🌧️ Khả năng mưa cao nhất: **{number(rainiest['Khả năng mưa (%)'])}%** vào {rainiest['Ngày']}.")

with tab2:
    st.markdown('<div class="section-label">Chi tiết dự báo theo ngày</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.caption("Xác suất mưa và lượng mưa là các giá trị dự báo, không phải số liệu quan trắc thực tế.")
    csv_data = pd.DataFrame(rows).to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ Xuất dự báo CSV", csv_data, file_name="du_bao_7_ngay.csv", mime="text/csv")

with tab3:
    df = pd.DataFrame(rows)
    df["Ngày"] = pd.to_datetime(df["Ngày"], format="%d/%m/%Y")
    st.markdown('<div class="section-label">Xu hướng nhiệt độ 7 ngày</div>', unsafe_allow_html=True)
    temp = df.melt("Ngày", value_vars=["Cao nhất (°C)", "Thấp nhất (°C)"], var_name="Loại", value_name="Nhiệt độ")
    chart = alt.Chart(temp).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X("Ngày:T", title="Ngày", axis=alt.Axis(format="%d/%m", labelColor="#b6c7e1", titleColor="#b6c7e1")),
        y=alt.Y("Nhiệt độ:Q", title="°C", scale=alt.Scale(zero=False), axis=alt.Axis(labelColor="#b6c7e1", titleColor="#b6c7e1")),
        color=alt.Color("Loại:N", scale=alt.Scale(domain=["Cao nhất (°C)", "Thấp nhất (°C)"], range=["#ffbd70", "#80b9ff"]), legend=alt.Legend(labelColor="#dce8fc", title=None)),
        tooltip=["Ngày:T", "Loại:N", alt.Tooltip("Nhiệt độ:Q", format=".1f")]
    ).properties(height=310).configure_view(stroke=None).configure(background="transparent")
    st.altair_chart(chart, use_container_width=True)
    st.markdown('<div class="section-label">Khả năng mưa từng ngày</div>', unsafe_allow_html=True)
    rain_chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#75b6ff").encode(
        x=alt.X("Ngày:T", axis=alt.Axis(format="%d/%m", labelColor="#b6c7e1", titleColor="#b6c7e1"), title="Ngày"),
        y=alt.Y("Khả năng mưa (%):Q", scale=alt.Scale(domain=[0, 100]), title="Xác suất (%)", axis=alt.Axis(labelColor="#b6c7e1", titleColor="#b6c7e1")),
        tooltip=["Ngày:T", "Khả năng mưa (%):Q"]
    ).properties(height=240).configure_view(stroke=None).configure(background="transparent")
    st.altair_chart(rain_chart, use_container_width=True)


