# main.py
from transformers import pipeline
from utils import extract_entities, extract_whitepaper_sections

# Improved classification with more document types
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
candidate_labels = [
    "research paper", "whitepaper", "technical report",
    "invoice", "receipt", "purchase order",
    "resume", "CV", "curriculum vitae",
    "contract", "agreement", "legal document",
    "business report", "blog post", "article"
]


def classify_document(text):
    # Use a longer text sample for better classification
    sample_text = text[:1000] if len(text) > 1000 else text

    result = classifier(sample_text, candidate_labels)

    # Get top 3 labels with confidence scores
    top_labels = []
    for i in range(min(3, len(result['labels']))):
        label = result['labels'][i]
        confidence = float(result['scores'][i])
        top_labels.append((label, confidence))

    # Return the most confident label
    return {"label": top_labels[0][0], "confidence": top_labels[0][1], "all_predictions": top_labels}


# Enhanced Structured Output
def structured_output(text, doc_type):
    entities = extract_entities(text, doc_type)

    if doc_type in ["whitepaper", "research paper", "technical report"]:
        sections = extract_whitepaper_sections(text)
        output = {
            "document_type": doc_type,
            "extracted_fields": {
                "title": text[:100] if len(text) > 100 else text,
                "authors": entities.get("PERSON", []),
                "organizations": entities.get("ORG", []),
                "publication_date": entities.get("DATE", []),
                "technologies": entities.get("TECH", []),
                "key_sections": {
                    "abstract": sections["abstract"][:500] + "..." if len(sections["abstract"]) > 500 else sections[
                        "abstract"],
                    "methodology": sections["methodology"][:500] + "..." if len(sections["methodology"]) > 500 else
                    sections["methodology"],
                    "key_findings": sections["results"][:500] + "..." if len(sections["results"]) > 500 else sections[
                        "results"]
                },
                "reference_count": len(sections["references"])
            }
        }
    elif doc_type == "invoice":
        output = {
            "document_type": "invoice",
            "extracted_fields": {
                "vendor_name": entities.get("ORG", []),
                "invoice_date": entities.get("DATE", []),
                "total_amount": entities.get("MONEY", []),
                "line_items": []  # This would require more advanced table extraction
            }
        }
    elif doc_type in ["resume", "CV", "curriculum vitae"]:
        output = {
            "document_type": "resume",
            "extracted_fields": {
                "candidate_name": entities.get("PERSON", []),
                "contact_info": {
                    "email": entities.get("EMAIL", []),
                    "phone": entities.get("PHONE", [])
                },
                "skills": entities.get("TECH", []),
                "education": [],
                "work_experience": []
            }
        }
    elif doc_type in ["contract", "agreement", "legal document"]:
        output = {
            "document_type": "contract",
            "extracted_fields": {
                "parties": entities.get("ORG", []),
                "dates": entities.get("DATE", []),
                "key_clauses": []
            }
        }
    else:  # General document
        output = {
            "document_type": doc_type,
            "extracted_fields": {
                "key_entities": {k: v for k, v in entities.items() if v},
                "summary": text[:300] + "..." if len(text) > 300 else text
            }
        }

    return output







