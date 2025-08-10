import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, CSVLoader
from docx import Document as d
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
import faiss


VECTORDB_NAME = "faiss_db"
folder_path = "KB"

embedding_model = OllamaEmbeddings(model = 'all-minilm:22m')

# Function to load and extract text from multiple formats
def load_documents_from_folder(folder_path):
    docs = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            docs.extend(loader.load())
        elif filename.lower().endswith(".csv"):
            loader = CSVLoader(file_path)
            docs.extend(loader.load())
        elif filename.lower().endswith(".docx"):
            file_path = os.path.join(folder_path,filename)
            doc = d(file_path)
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if full_text.strip():
                doc_data = Document(page_content=full_text,metadata={"source": filename})
                docs.append(doc_data)
    return docs

folder_path = "KB"

def VectorStore():
    index = faiss.IndexFlatL2(384)
    documents = load_documents_from_folder(folder_path)

    # Split text into chunks for embeddings
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(documents)

    vs = FAISS(
        embedding_function = embedding_model,
        index = index,
        docstore = InMemoryDocstore(),
        index_to_docstore_id = {}
    )

    vs.add_documents(split_docs)
    # Save FAISS index locally
    vs.save_local(VECTORDB_NAME)

    print(f"Indexed {len(split_docs)} document chunks into FAISS.")

VectorStore()