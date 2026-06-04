import streamlit as st

st.title("履歴書入力フォーム")

name = st.text_input("氏名")
age = st.number_input("年齢", min_value=0, max_value=100)

pr = st.text_area("自己PR")

# 文字数をカウント
count = len(pr)

st.write("文字数:", count)

if count < 100:
    st.write("文字数が足りません")
else:
    st.write("OK")