# utils.py
import spacy
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import PyPDF2
import docx
import re
import numpy as np
import json
from datetime import datetime

# SpaCy
nlp = spacy.load("en_core_web_sm")

# Embedding model for RAG
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# LLM for Q&A
qa_model = pipeline("text2text-generation", model="google/flan-t5-base")


# Read documents 
def read_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def read_docx(file):
    doc = docx.Document(file)
    text = " ".join([para.text for para in doc.paragraphs])
    return text.strip()


def read_txt(file):
    return file.read().decode("utf-8").strip()


# Extract entities with improved patterns
def extract_entities(text, doc_type):
    doc = nlp(text)
    entities = {
        "PERSON": [], "ORG": [], "DATE": [], "GPE": [],
        "EMAIL": [], "PHONE": [], "MONEY": [], "TECH": []
    }

    # Named Entities from SpaCy
    for ent in doc.ents:
        if ent.label_ in entities:
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)

    # Emails
    entities["EMAIL"] = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)

    # Phones (improved pattern)
    phone_patterns = [
        r'\+\d{1,3}[\s-]?\d{1,4}[\s-]?\d{1,4}[\s-]?\d{1,9}',
        r'\(\d{3}\)\s?\d{3}[\s-]\d{4}',
        r'\d{3}[\s-]\d{3}[\s-]\d{4}'
    ]
    entities["PHONE"] = []
    for pattern in phone_patterns:
        entities["PHONE"].extend(re.findall(pattern, text))

    # Technical terms common in whitepapers
    tech_terms = [
        "LLM", "AI", "Machine Learning", "Deep Learning", "NLP",
        "Transformer", "GPT", "BERT", "Generative AI", "Foundation Models",
        "Natural Language Processing", "Computer Vision", "Neural Network"
    ]

    entities["TECH"] = [term for term in tech_terms if re.search(r'\b' + re.escape(term) + r'\b', text, re.IGNORECASE)]

    # Money/currency amounts
    if doc_type == "invoice":
        money_pattern = r'\$?\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?(?:\s*(?:dollars|USD))?'
        entities["MONEY"] = re.findall(money_pattern, text)

    return entities


# Improved RAG-based Q&A
def rag_answer(question, document_text, k=3):
    if not document_text:
        return "No content to answer from."

    # Split document into meaningful chunks (sentences or paragraphs)
    chunks = [chunk for chunk in document_text.split('. ') if len(chunk) > 20]

    if not chunks:
        chunks = [document_text[i:i + 200] for i in range(0, len(document_text), 200)]

    doc_embeddings = embed_model.encode(chunks)
    q_embedding = embed_model.encode([question])[0]

    # Calculate cosine similarity
    norms = np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(q_embedding)
    sims = np.dot(doc_embeddings, q_embedding) / norms
    sims = np.nan_to_num(sims, nan=0)

    top_indices = sims.argsort()[-k:][::-1]
    context = " ".join([chunks[i] for i in top_indices])

    input_text = f"Answer this question based only on the context: {question}\nContext: {context}"

    try:
        answer = qa_model(input_text, max_length=200, do_sample=True, temperature=0.3)[0]['generated_text']
        return answer
    except:
        return "I couldn't generate an answer. Please try a different question."


# Extract key sections from whitepapers
def extract_whitepaper_sections(text):
    sections = {
        "abstract": "",
        "introduction": "",
        "methodology": "",
        "results": "",
        "conclusion": "",
        "references": []
    }

    # Simple pattern matching for section headers
    lines = text.split('\n')
    current_section = None

    for line in lines:
        line_lower = line.lower().strip()

        if any(keyword in line_lower for keyword in ['abstract', 'summary']):
            current_section = 'abstract'
        elif 'introduction' in line_lower:
            current_section = 'introduction'
        elif any(keyword in line_lower for keyword in ['method', 'methodology', 'approach']):
            current_section = 'methodology'
        elif any(keyword in line_lower for keyword in ['result', 'finding', 'experiment']):
            current_section = 'results'
        elif any(keyword in line_lower for keyword in ['conclusion', 'discussion']):
            current_section = 'conclusion'
        elif any(keyword in line_lower for keyword in ['reference', 'bibliography']):
            current_section = 'references'
        elif current_section and line.strip():
            if current_section == 'references':
                if line.strip() not in sections['references']:
                    sections['references'].append(line.strip())
            else:
                sections[current_section] += line + " "

    return sections




