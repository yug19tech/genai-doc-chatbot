import os
import sys
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

# Build the database automatically if it doesn't exist (needed for deployment)
if not os.path.exists("chroma_db"):
    from ingest import ingest
    ingest()

from answer import answer_question

st.set_page_config(page_title="Document Q&A Chatbot", page_icon="📄")
st.title("📄 Document Q&A Chatbot")
st.caption("Ask questions about the uploaded documents. Answers include sources.")

question = st.text_input("Your question:")

if st.button("Ask") and question.strip():
    with st.spinner("Searching documents..."):
        answer, chunks = answer_question(question)

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Sources used"):
        for c in chunks:
            st.markdown(f"**{c['source']}, page {c['page']}**")
            st.write(c["text"])
            st.divider()