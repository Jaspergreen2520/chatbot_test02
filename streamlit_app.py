import streamlit as st
import requests

st.title("💬 Chatbot (Gemini 1.5 Pro 最新版)")
st.write(
    "Google Gemini 1.5 Pro-Latestモデルを使用しています。APIキー取得方法は[公式ドキュメント](https://ai.google.dev/gemini-api/docs/api-key)をご参照ください。"
)

gemini_api_key = st.text_input("Google Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するにはGoogle Gemini APIキーを入力してください。", icon="🗝️")
else:
    # 2024年6月以降の正式APIエンドポイント
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro-latest:generateContent"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("何か話しかけてください！"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        gemini_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [{"text": m["content"]}]})
            else:
                gemini_messages.append({"role": "model", "parts": [{"text": m["content"]}]})

        headers = {"Content-Type": "application/json"}
        params = {"key": gemini_api_key}
        data = {
            "contents": gemini_messages
        }
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            gemini_reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            gemini_reply = f"APIエラー: {response.status_code}\n{response.text}"

        with st.chat_message("assistant"):
            st.markdown(gemini_reply)
        st.session_state.messages.append({"role": "assistant", "content": gemini_reply})
