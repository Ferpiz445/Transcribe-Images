import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def transcrever_imagem(uploaded_file):
    temp_path = "temp_image.jpg"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [genai.upload_file(temp_path, mime_type="image/jpeg")],
                }
            ]
        )
        response = chat_session.send_message(
            "Transcreva o que foi escrito acima")
        return response.text
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# Interface do Streamlit
st.title("Transcrição de Texto a partir de Imagem")
st.write("Faça o upload de uma imagem para transcrever o texto escrito à mão.")

uploaded_file = st.file_uploader(
    "Envie uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    with st.spinner("Realizando a transcrição..."):
        try:
            resultado = transcrever_imagem(uploaded_file)
            st.success("Transcrição concluída!")

            num_lines = resultado.count("\n") + 1
            line_height = 20
            altura_dinamica = max(100, num_lines * line_height)

            st.text_area("Texto Transcrito:", resultado,
                         height=altura_dinamica)
        except Exception as e:
            st.error(f"Erro ao processar a imagem: {e}")
