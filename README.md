# Document Intelligence AI: Classify & Extract Data with LLMs

A powerful Streamlit web application that leverages Large Language Models (LLMs) and Natural Language Processing (NLP) to automatically classify document types and extract structured information from them. This tool transforms unstructured documents (PDF, DOCX, TXT) into organized, queryable data.

## Features

- **Smart Document Classification:** Accurately identifies document types (Invoices, Resumes, Whitepapers, Contracts) using zero-shot learning with Hugging Face models.
- **Structured Data Extraction:** Pulls key entities (names, dates, emails, phone numbers, amounts) into a clean, consumable JSON format.
- **Document Q&A Chat:** Ask questions in natural language and get answers sourced directly from the uploaded document using a Retrieval-Augmented Generation (RAG) system.
- **Multi-Format Support:** Processes **PDF**, **DOCX**, and **TXT** files seamlessly.
- **Confidence Scoring:** Provides transparency by showing confidence levels for classification predictions.

## Tech Stack

- **Frontend & App Framework:** Streamlit
- **Core Language & ML:** Python
- **Language Models & NLP:** Hugging Face Transformers, spaCy, Sentence-Transformers
- **File Processing:** PyPDF2, python-docx

## Project Structure
document-ai-classifier/

│

├── app.py # Main Streamlit application file

├── main.py # Core logic for classification & output

├── utils.py # Helper functions (file reading, NLP, Q&A)

├── requirements.txt # List of Python dependencies

├── LICENSE # The MIT License

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Download the project files**
   - Click the green "Code" button on this GitHub page
   - Select "Download ZIP"
   - Extract the ZIP file to a folder on your computer

2. **Open a terminal/command prompt** and navigate to the project folder:
   ```bash
   cd path/to/document-ai-classifier
3. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
4.  Download the spaCy language model:
    ```bash
    python -m spacy download en_core_web_sm
   
### Usage
1.Run the application:
  streamlit run app.py
    
2.Open your browser to http://localhost:8501

3.Upload a document (PDF, DOCX, or TXT) and view the:

  - **Automatic classification results**

  - **Extracted structured data in JSON format**

  - **Ask questions about the document content**

### How It Works
-**Document Processing:** The app reads uploaded files using specialized libraries (PyPDF2 for PDFs, python-docx for Word files).

-**Classification:** A zero-shot learning model analyzes the text to determine the document type.

-**Information Extraction:** NLP techniques identify and extract key entities like names, dates, and contact information.

-**Question Answering:** A RAG (Retrieval Augmented Generation) system finds relevant context in the document to answer user questions.

### File Descriptions
-**app.py:** Main application file containing the Streamlit web interface

-**main.py:** Handles document classification and structured output generation

-**utils.py:** Contains helper functions for file reading, entity extraction, and Q&A

-**requirements.txt:** Lists all Python packages needed to run the project

### License
Distributed under the MIT License. See LICENSE file for details.

### Acknowledgments
-**Hugging Face for providing pre-trained models**

-**The Streamlit team for making web app development accessible**

-**spaCy for robust natural language processing capabilities**

