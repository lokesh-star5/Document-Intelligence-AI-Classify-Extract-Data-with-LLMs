# app.py
import streamlit as st
from main import classify_document, structured_output
from utils import read_pdf, read_docx, read_txt, rag_answer

st.set_page_config(page_title="📄 Document Classifier & AI Q&A", layout="wide")
st.title("📄 Document Classifier & AI Q&A (Structured Output + Confidence)")

uploaded_file = st.file_uploader("Upload PDF, DOCX, TXT", type=["pdf", "docx", "txt"])

if uploaded_file:
    # Read file
    with st.spinner("Reading document..."):
        if uploaded_file.name.endswith(".pdf"):
            text = read_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            text = read_docx(uploaded_file)
        else:
            text = read_txt(uploaded_file)

    # Display document preview
    with st.expander("Document Preview"):
        st.text(text[:1000] + "..." if len(text) > 1000 else text)

    # Classification
    with st.spinner("Classifying document..."):
        classification = classify_document(text)

    st.subheader("Classification")
    st.json(classification)

    # Show all predictions if low confidence
    if classification['confidence'] < 0.5:
        st.warning(f"Low confidence in classification ({classification['confidence']:.2f}). Top predictions:")
        for label, confidence in classification.get('all_predictions', []):
            st.write(f"- {label}: {confidence:.2f}")

    # Structured Output
    with st.spinner("Extracting information..."):
        output = structured_output(text, classification['label'])

    st.subheader("Structured Output")
    st.json(output)

    # Q&A Section
    st.subheader("Ask about this document")
    question = st.text_input("Enter a question about the document content")

    if question:
        with st.spinner("Generating answer..."):
            answer = rag_answer(question, text)

        st.subheader("Answer")
        st.write(answer)

        if "couldn't generate" in answer or "No content" in answer:
            st.info(
                "Try asking about specific content in the document, like 'What is the main topic?' or 'What technologies are discussed?'")

