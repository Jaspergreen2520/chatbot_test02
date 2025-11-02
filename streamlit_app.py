import streamlit as st
import requests

# Show title and description.
st.title("💬 Chatbot (Gemini 2.5 Pro)")
st.write(
    "このチャットボットはGoogle Gemini 2.5 Proモデルを使用して応答を生成します。 "
    "利用にはGoogle Gemini APIキーが必要です。[APIキー取得方法](https://ai.google.dev/gemini-api/docs/api-key)。 "
    "StreamlitでGeminiを使うチュートリアルは[こちら](https://ai.google.dev/gemini-api/docs/get-started-python)。"
)

# Ask user for Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Google Gemini API Key", type="password")
if not gemini_api_key:
    st.info("続行するにはGoogle Gemini APIキーを入力してください。", icon="🗝️")
else:
    # Gemini APIエンドポイント
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("何か話しかけてください！"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gemini APIのリクエスト用メッセージリスト (user/assistantで構築)
        gemini_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                gemini_messages.append({"role": "user", "parts": [{"text": m["content"]}]})
            else:
                gemini_messages.append({"role": "model", "parts": [{"text": m["content"]}]})

        # Gemini APIへリクエスト
        headers = {"Content-Type": "application/json"}
        params = {"key": gemini_api_key}
        data = {
            "contents": gemini_messages
        }
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
        if response.status_code == 200:
            result = response.json()
            # Geminiの返答取得
            gemini_reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            gemini_reply = f"APIエラー: {response.status_code}\n{response.text}"

        # Show Gemini reply and update session state
        with st.chat_message("assistant"):
            st.markdown(gemini_reply)
        st.session_state.messages.append({"role": "assistant", "content": gemini_reply})
