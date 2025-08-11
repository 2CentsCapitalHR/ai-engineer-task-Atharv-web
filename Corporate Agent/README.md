# Corporte Agent

This project is an application that automates legal document analysis and review using AI powered Assistant called Corporate Agent. This agent will assist in reviewing, validating, and helping users prepare documentation for business incorporation and compliance within the Abu Dhabi Global Markets (ADGM).

## Features

- **Upload Legal Documents:** Upload your `.docx` files for analysis.
- **Automated Process Identification:** The system identifies the type of legal process represented in the documents.
- **Checklist Validation:** Each document is checked against a pre-defined checklist for required items and compliance.
- **Legal Issue Detection:** Utilizes a FAISS vector database built from your knowledge base (PDF, CSV, DOCX) to flag potential legal issues.
- **Document Annotation and Reporting:** Documents are annotated with findings, and a comprehensive report is generated.
- **Progress Monitoring:** Real-time progress updates during processing.

## How It Works

1. **Knowledge Base Preparation:** Place relevant reference documents in the `KB` folder. Run `KnowledgeBase.py` to build the FAISS vector database (`faiss_db`).
2. **Start the Application:** Run `app.py` (or `legal_work.py`) to launch the Flask web server.
3. **Upload Documents:** Use the web interface to upload `.docx` files for review.
4. **Automated Workflow:** The app processes your files step-by-step:
   - Identifies the legal process.
   - Checks documents against the checklist.
   - Finds legal issues using semantic search.
   - Annotates and generates a report.
5. **View and Download Results:** After processing, download the annotated files and the report from the results page.

## Project Structure

- `app.py`: Main web application.
- `legal_work.py`: (Duplicate of `app.py`; intended for modularization or alternate entry-point.)
- `KnowledgeBase.py`: Prepares the FAISS vector database from the `KB` folder.
- `input/`: Uploaded documents.
- `output/`: Annotated documents and reports.
- `backend/checklist.json`: Checklist used for validation.
- `backend/faiss_db/`: Generated vector database.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare your knowledge base in the `KB` folder.
3. Run the knowledge base script to build the vector store:
   ```bash
   python KnowledgeBase.py
   ```
4. Start the web application:
   ```bash
   python app.py
   ```
5. Open your browser at [http://localhost:5000](http://localhost:5000), upload legal `.docx` files, and review the results. The `.docx` (annotated) file will be present in the `output` folder

