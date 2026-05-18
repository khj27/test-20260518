import streamlit as st

st.title("📋 사용자 정보 입력 폼")

# 1. 사용자 입력 위젯
name = st.text_input("🧑 이름을 입력하세요")
age = st.number_input("🎂 나이를 입력하세요", min_value=0, max_value=120, step=1)
gender = st.radio("🚻 성별을 선택하세요", ["남자", "여자", "기타"])
interests = st.multiselect("💡 관심 있는 주제를 선택하세요", ["인공지능", "데이터 분석", "웹 개발", "금융", "디자인"])
description = st.text_area("📘 자기소개 또는 하고 싶은 말")
agree = st.checkbox("✅ 개인정보 수집 및 이용에 동의합니다")

# 2. 제출 버튼
if st.button("제출"):
    if not name:
        st.warning("이름을 입력하세요.")
    elif not agree:
        st.error("개인정보 수집 동의가 필요합니다.")
    else:
        # 3. 결과 출력
        st.success("입력이 완료되었습니다! 🎉")
        st.markdown("---")
        st.subheader("📄 제출 내용 요약")
        st.write(f"**이름:** {name}")
        st.write(f"**나이:** {age}세")
        st.write(f"**성별:** {gender}")
        st.write(f"**관심 주제:** {', '.join(interests) if interests else '없음'}")
        st.write("**소개글:**")
        st.info(description if description else "작성하지 않음")

