from cProfile import label

from pandas import options
import streamlit as st

fruit = st.selectbox("좋아하는 과일을 선택하세요", ["사과", "바나나", "체리"])
st.write("선택한 과일:", fruit)

users = [{"id": 1, "name": "홍길동"}, {"id": 2, "name": "이몽룡"}]
selected_user = st.selectbox(
    "사용자 선택",
    users,
    format_func=lambda x: f"{x['name']} (ID: {x['id']})"
)
st.write("선택한 사용자 ID:", selected_user['id'])
선택값 = st.multiselect(
    label,              # 사용자에게 보여질 라벨 (문자열)
    options,            # 선택 가능한 항목 리스트
    default=None        # (선택) 기본 선택값, 하나 또는 여러 개
)

