import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.title("新歓感想投稿")

# Google Sheets 認証
creds_dict = st.secrets["gcp_service_account"]
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_info(creds_dict, scopes=scopes)
client = gspread.authorize(credentials)

# スプレッドシートを開く
spreadsheet = client.open("新歓予約フォーム")
sheet = spreadsheet.worksheet("感想")

# secrets.toml からリスト取得
targets = st.secrets["names"]["list"]
users = st.secrets["users"]["list"]

# ユーザー入力欄
selected_user = st.selectbox("あなたの名前を選択してください", users)
selected_target = st.selectbox("感想を書きたい人を選んでください", targets)
date = st.date_input("日付を選んでください")
comment = st.text_area("感想を入力してください")

# 送信処理
if st.button("送信"):
    if not comment.strip():
        st.warning("感想が空です。入力してください。")
    else:
        datetime_str = f"{date.strftime('%Y-%m-%d')}"
        sheet.append_row([datetime_str, selected_user, selected_target, comment])
        st.success("感想を送信しました！")
