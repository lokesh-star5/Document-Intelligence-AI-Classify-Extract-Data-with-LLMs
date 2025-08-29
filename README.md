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
- **Version Control:** Git & GitHub

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:
- You have installed **Python 3.8** or higher.
- You have installed **Git**.

### Installation & Setup

Follow these steps to get a local copy up and running:

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/document-ai-classifier.git
    cd document-ai-classifier
    ```

2.  **Create and activate a virtual environment** (Recommended)
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download the spaCy language model**
    ```bash
    python -m spacy download en_core_web_sm
    ```

### How to Run the Application

1.  **Ensure your virtual environment is activated** (you should see `(venv)` in your terminal prompt).
2.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```
3.  **Your browser will automatically open** to `http://localhost:8501`.
4.  **Upload a document** (PDF, DOCX, or TXT) and watch the AI process it!

## How to Use

1.  **Upload:** Drag and drop a file into the uploader box.
2.  **Automatic Processing:** The app will automatically:
    - **Classify** the document (e.g., "This is a Whitepaper").
    - Show a **confidence score**.
    - Display the **structured data** extracted in a JSON format.
3.  **Ask Questions:** Use the text input at the bottom to ask any question about the document's content (e.g., "What is the main topic?", "List the key technologies mentioned.").

## Project Structure
document-ai-classifier/

│

├── app.py # Main Streamlit application file

├── main.py # Core logic for classification & output

├── utils.py # Helper functions (file reading, NLP, Q&A)

├── requirements.txt # List of Python dependencies

├── LICENSE # The MIT License

└── README.md # This file

## Future Improvements

- Fine-tune a custom model for higher classification accuracy.
- Add support for images of documents using OCR.
- Implement a database to store processed documents.
- Deploy the application as a public web service.

## How to Contribute

Contributions are welcome! If you have ideas for improvements, please feel free to fork this repository and submit a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` file for more information.

## Acknowledgments

- Hugging Face for providing pre-trained models.
- The Streamlit team for making it easy to build data apps.

