import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import docx

load_dotenv()

# --- Helper: Extract text with page info ---
def extract_text_with_pages(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"text": text, "page": i + 1})  # ✅ keep page number
        return pages
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return [{"text": text, "page": None}]
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return [{"text": text, "page": None}]
    return []

# --- Helper: Split text into chunks ---
def split_text(content, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(content)

# --- Build a new FAISS index ---
def build_vector_store(folders, index_name="default_index"):
    if isinstance(folders, str):
        folders = [folders]

    texts = []
    metadatas = []
    for folder in folders:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            pages = extract_text_with_pages(file_path)
            for page in pages:
                chunks = split_text(page["text"])
                for i, chunk in enumerate(chunks):
                    texts.append(chunk)
                    metadatas.append({
                        "source": file,
                        "page": page["page"],
                        "chunk_id": i
                    })

    if not texts:
        raise ValueError(
            f"⚠️ No valid content found in {folders}. "
            "Please upload .txt, .pdf, or .docx files with readable text."
        )

    print(f"✅ Building FAISS index with {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    vector_store.save_local(index_name)   # ✅ saves to folder
    return vector_store

# --- Update an existing FAISS index ---
def update_vector_store(new_files, index_name="default_index"):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    vector_store = FAISS.load_local(index_name, embeddings, allow_dangerous_deserialization=True)

    new_texts = []
    new_metadatas = []
    for file_path in new_files:
        pages = extract_text_with_pages(file_path)
        for page in pages:
            chunks = split_text(page["text"])
            for i, chunk in enumerate(chunks):
                new_texts.append(chunk)
                new_metadatas.append({
                    "source": os.path.basename(file_path),
                    "page": page["page"],
                    "chunk_id": i
                })

    if not new_texts:
        raise ValueError("⚠️ No valid new files provided for update.")

    vector_store.add_texts(new_texts, metadatas=new_metadatas)
    vector_store.save_local(index_name)
    return vector_store

# --- Load an existing FAISS index ---
def load_vector_store(index_name="default_index"):
    embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
    index_folder = index_name  # ✅ FAISS saves to a folder

    if not os.path.exists(index_folder):
        print(f"⚠️ Index folder {index_folder} not found. Please build it first.")
        return None

    try:
        vector_store = FAISS.load_local(
            index_folder,
            embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"✅ Loaded FAISS index from {index_folder}")
        return vector_store
    except Exception as e:
        print(f"❌ Error loading index {index_folder}: {e}")
        return None
