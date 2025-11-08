"""UI de Streamlit para el chatbot Lazarus."""

import streamlit as st
from dotenv import load_dotenv
from lazarus_core import LazarusChatbot
from lazarus_kb import FAQKnowledgeBase

load_dotenv()

st.set_page_config(
    page_title="Lazarus Chatbot",
    page_icon="bot",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .assistant-message {
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .metadata-badge {
        display: inline-block;
        background-color: #e0e0e0;
        padding: 5px 10px;
        border-radius: 3px;
        font-size: 12px;
        margin-right: 5px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializar estado de sesion de Streamlit."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = LazarusChatbot()
    if "kb" not in st.session_state:
        st.session_state.kb = FAQKnowledgeBase()

initialize_session_state()

with st.sidebar:
    st.title("Informacion de la KB")
    
    kb = st.session_state.kb
    all_faqs = kb.get_all_faqs()
    
    st.metric("Total de FAQs", len(all_faqs))
    
    categories = {}
    for faq in all_faqs:
        cat = faq.get('categoria', 'General')
        categories[cat] = categories.get(cat, 0) + 1
    
    st.subheader("FAQs por Categoria")
    for cat, count in sorted(categories.items()):
        st.write(f"- {cat}: {count}")
    
    with st.expander("Ver todas las FAQs"):
        for i, faq in enumerate(all_faqs, 1):
            st.write(f"**{i}. {faq['pregunta']}**")
            st.write(f"Respuesta: {faq['respuesta']}")
            st.write(f"Categoria: {faq['categoria']}")
            st.divider()

st.title("Chatbot Grupo Lazarus")
st.write("Bienvenido al asistente virtual de Grupo Lazarus. Puedo ayudarte con preguntas sobre nuestros servicios.")

for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'><strong>Tu:</strong> {message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'><strong>Asistente:</strong> {message['content']}</div>", unsafe_allow_html=True)
        
        if "metadata" in message:
            meta = message["metadata"]
            cols = st.columns(3)
            with cols[0]:
                st.caption(f"Fuente: {meta.get('source', 'N/A')}")
            with cols[1]:
                if meta.get('transfer_to_agent'):
                    st.caption("Marca de transferencia: Si")
            with cols[2]:
                if meta.get('transfer_reason'):
                    st.caption(f"Razon: {meta['transfer_reason']}")

user_input = st.chat_input("Escribe tu pregunta aqui...")

if user_input:
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = st.session_state.chatbot.answer(user_input)
    
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response['answer'],
        "metadata": {
            "source": response['source'],
            "transfer_to_agent": response['transfer_to_agent'],
            "transfer_reason": response['transfer_reason']
        }
    })
    
    st.rerun()
