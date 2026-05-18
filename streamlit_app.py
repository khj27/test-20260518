import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("data/인구수_2026.csv", header=[0, 1])
    df.columns = df.columns.map(lambda x: x[0] if x[0] == '행정구역(시군구)별' else f"{x[0]}|{x[1]}")
    df = df.melt(id_vars="행정구역(시군구)별", var_name="구분", value_name="인구수")
    df[["연도", "성별"]] = df["구분"].str.split("|", expand=True)
    df["성별"] = df["성별"].replace({
        "총인구수 (명)": "전체",
        "남자인구수 (명)": "남자",
        "여자인구수 (명)": "여자"
    })
    df["연도"] = df["연도"].str.replace(".", "-", regex=False)
    df["연도"] = df["연도"].replace({"2026-04": "2026"})
    df = df[~df["연도"].isin(["2026-01", "2026-02", "2026-03"])]
    df["인구수"] = pd.to_numeric(df["인구수"], errors="coerce")
    df = df.rename(columns={"행정구역(시군구)별": "행정구역"})
    return df

df = load_data()

# 기본 설정
st.set_page_config(layout="wide")
st.title("📊 대한민국 인구 대시보드")

# ---------------------
# 사이드바
# ---------------------
years = sorted(df["연도"].unique(), reverse=True)
genders = ["전체", "남자", "여자"]
regions = sorted(df["행정구역"].unique())

st.sidebar.header("🔧 설정")
selected_year = st.sidebar.selectbox("📅 연도 선택", years)
selected_gender = st.sidebar.radio("👥 성별 선택", genders)
selected_region = st.sidebar.selectbox("📍 행정구역 선택 (꺾은선 그래프)", regions)

# ---------------------
# 데이터 필터링
# ---------------------
df_bar = df[(df["연도"] == selected_year) & (df["성별"] == selected_gender)]
df_bar = df_bar[df_bar["행정구역"] != "전국"]

df_line = df[(df["성별"] == selected_gender) & (df["행정구역"] == selected_region)]
df_line_grouped = df_line.groupby("연도")["인구수"].sum().reset_index()

# KPI용
curr_pop = df_line[df_line["연도"] == selected_year]["인구수"].sum()
prev_year = str(int(selected_year) - 1)
prev_pop = df_line[df_line["연도"] == prev_year]["인구수"].sum() if prev_year in df_line["연도"].values else 0
delta = curr_pop - prev_pop
arrow = "↑" if delta > 0 else ("↓" if delta < 0 else "-")
formatted_curr = f"{curr_pop/1_000_000:.2f} M"
formatted_delta = f"{arrow} {abs(delta)/1_000:.1f} K"

# ---------------------
# KPI 영역 (전체 가로)
# ---------------------
st.subheader("📌 인구 요약 지표")
k1, k2 = st.columns(2)
k1.metric(f"{selected_year} 총 인구수", formatted_curr)
k2.metric(f"{prev_year} 대비 증감", formatted_delta)

# ---------------------
# 본문: 막대그래프 + 꺾은선그래프 (좌우 분할)
# ---------------------
b1, b2 = st.columns(2)

with b1:
    st.subheader(f"📊 {selected_year} 지역별 인구수")
    fig_bar = px.bar(df_bar.sort_values("인구수", ascending=True),
                     x="인구수", y="행정구역", orientation="h",
                     color="인구수", color_continuous_scale="Blues")
    st.plotly_chart(fig_bar, use_container_width=True)

with b2:
    st.subheader(f"📈 {selected_region} 연도별 인구 변화")
    fig_line = px.line(df_line_grouped, x="연도", y="인구수", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# ---------------------
# 데이터 테이블 (가로 전체)
# ---------------------
st.subheader("📋 선택 조건 데이터 테이블")
st.dataframe(df_line[df_line["연도"] == selected_year], use_container_width=True)
