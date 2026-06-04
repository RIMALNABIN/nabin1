import streamlit as st

# タイトル
st.title("MY PROFILE")

# 説明
st.write("THIS IS MY WEBSide。")

# 入力フォーム
name = st.text_input("名前を入力してください")
country = st.text_input("出身国を入力してください")
hobby = st.text_input("趣味を入力してください")

# 入力されたら表示
if name and country and hobby:
    st.header("入力内容")

    st.write("名前：", name)
    st.write("出身国：", country)
    st.write("趣味：", hobby)