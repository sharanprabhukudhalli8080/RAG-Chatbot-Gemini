import tempfile
import streamlit as st

from utils.pdf_loader import load_pdf
from utils.vector_store import create_vector_store
from utils.llm_handler import get_answer

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Gemini PDF Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "prompt" not in st.session_state:
    st.session_state.prompt = None

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

if "documents_loaded" not in st.session_state:
    st.session_state.documents_loaded = False

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #f7f7f8;
}

/* Main Width */
.block-container {
    max-width: 1200px;
    padding-top: 1rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #e5e7eb;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background: white;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    padding: 12px;
    margin-bottom: 10px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: white;
    border-radius: 16px;
    padding: 15px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

/* Buttons */
.stButton button {
    width: 100%;
    border-radius: 12px;
    font-weight: 600;
}

/* Download Button */
.stDownloadButton button {
    width: 100%;
    border-radius: 12px;
}

/* Upload */
[data-testid="stFileUploader"] {
    background: white;
    border-radius: 12px;
    padding: 10px;
}

/* Hide Footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🤖 Gemini PDF")

    st.caption("Chat with your PDFs")

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        documents = []

        with st.spinner("Processing PDFs..."):

            for uploaded_file in uploaded_files:

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp_file:

                    tmp_file.write(
                        uploaded_file.read()
                    )

                    pdf_path = tmp_file.name

                docs = load_pdf(pdf_path)

                documents.extend(docs)

            st.session_state.vector_db = (
                create_vector_store(documents)
            )

            st.session_state.documents_loaded = True

        st.success("PDFs Ready")

    st.divider()

    if st.button("🗑 New Chat"):

        st.session_state.history = []

        st.rerun()

    st.metric(
        "Chats",
        len(st.session_state.history)
    )

    st.divider()

    st.subheader("Recent Questions")

    for chat in st.session_state.history[-5:]:

        st.caption(
            chat["question"][:40]
        )

# =====================================================
# EMPTY STATE
# =====================================================

if not st.session_state.documents_loaded:

    st.markdown(
        """
        <div style='
            text-align:center;
            margin-top:150px;
        '>

        <h1 style='font-size:52px'>
        🤖 Gemini PDF Assistant
        </h1>

        <p style='
            color:#6b7280;
            font-size:20px;
        '>
        Upload PDFs and start chatting with your documents
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("🤖 Gemini PDF Assistant")

st.caption(
    "Ask questions across multiple PDFs using Gemini 2.5 Flash"
)

# =====================================================
# METRICS
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:

    try:
        pages = len(
            st.session_state.vector_db.get()["documents"]
        )
    except:
        pages = "N/A"

    st.metric(
        "Chunks",
        pages
    )

with col2:

    st.metric(
        "Model",
        "Gemini 2.5"
    )

with col3:

    st.metric(
        "Chats",
        len(st.session_state.history)
    )

st.divider()

# =====================================================
# SUGGESTED PROMPTS
# =====================================================

st.subheader("✨ Suggested Questions")

c1, c2, c3 = st.columns(3)

with c1:

    if st.button("📄 Summarize Document"):

        st.session_state.prompt = (
            "Summarize this document"
        )

with c2:

    if st.button("🎯 Key Takeaways"):

        st.session_state.prompt = (
            "What are the key takeaways?"
        )

with c3:

    if st.button("📚 Important Topics"):

        st.session_state.prompt = (
            "What are the important topics?"
        )

st.divider()

# =====================================================
# CHAT HISTORY
# =====================================================

for chat in st.session_state.history:

    with st.chat_message("user"):

        st.write(chat["question"])

    with st.chat_message("assistant"):

        st.write(chat["answer"])

# =====================================================
# CHAT INPUT
# =====================================================

question = st.chat_input(
    "Ask anything about your PDFs..."
)

if (
    not question
    and st.session_state.prompt
):

    question = st.session_state.prompt

    st.session_state.prompt = None

# =====================================================
# GENERATE ANSWER
# =====================================================

if question:

    with st.chat_message("user"):

        st.write(question)

    with st.spinner(
        "Thinking..."
    ):

        answer, docs = get_answer(
            question,
            st.session_state.vector_db,
            st.session_state.history
        )

    with st.chat_message("assistant"):

        st.write(answer)

    st.session_state.history.append(
        {
            "question": question,
            "answer": answer
        }
    )

    # =================================================
    # SOURCES
    # =================================================

    st.subheader("📚 Sources")

    for i, doc in enumerate(docs):

        page = (
            doc.metadata.get(
                "page",
                0
            ) + 1
        )

        with st.expander(
            f"📄 Page {page}"
        ):

            st.write(
                doc.page_content[:800]
            )

# =====================================================
# DOWNLOAD CHAT
# =====================================================

if st.session_state.history:

    chat_text = ""

    for chat in st.session_state.history:

        chat_text += (
            f"Question: {chat['question']}\n"
        )

        chat_text += (
            f"Answer: {chat['answer']}\n\n"
        )

    st.download_button(
        "⬇ Download Chat History",
        chat_text,
        file_name="chat_history.txt"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🚀 Powered by Gemini 2.5 Flash • ChromaDB • LangChain • Streamlit"
)