import os
from dotenv import load_dotenv

# Load environment variables before using OpenAI
load_dotenv()

import hashlib
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")   # ✅ explicitly pass the key
)
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

from langchain_core.documents import Document
from PyPDF2 import PdfReader
import docx

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

def chunk_document(content, source, file_path):
    """
    Split document into chunks and attach metadata for citations.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = [
        Document(
            page_content=content,
            metadata={
                "source": source,                # filename
                "filepath": file_path            # full path
            }
        )
    ]
    return splitter.split_documents(docs)

def _hash_content(content: str) -> str:
    """Generate a SHA256 hash of the document content for duplicate detection."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def build_vector_store(folders, index_name="combined_ops_index"):
    """
    Build a new FAISS index from scratch across multiple folders.
    Logs skipped duplicates and successful indexing.
    """
    all_chunks = []
    seen_hashes = set()

    for folder in folders:
        if not os.path.exists(folder):
            continue
        for f in os.listdir(folder):
            file_path = os.path.join(folder, f)
            content = extract_text(file_path)
            if content.strip():
                content_hash = _hash_content(content)
                if content_hash in seen_hashes:
                    st.warning(f"⚠️ Skipped duplicate file: {f}")
                    continue
                seen_hashes.add(content_hash)
                # ✅ include metadata for citations
                all_chunks.extend(chunk_document(content, f, file_path))
                st.success(f"✅ Indexed new file: {f}")

    if not all_chunks:
        return None

    vector_store = FAISS.from_documents(all_chunks, embeddings)
    save_path = os.path.join("data", index_name)
    vector_store.save_local(save_path)
    return vector_store

def load_vector_store(index_name="combined_ops_index"):
    """
    Load an existing FAISS index from disk.
    """
    save_path = os.path.join("data", index_name)
    if os.path.exists(save_path):
        return FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
    return None

def update_vector_store(file_path, index_name="combined_ops_index"):
    """
    Incrementally add a new file to an existing FAISS index, skipping duplicates.
    Logs skipped duplicates and successful indexing.
    """
    content = extract_text(file_path)
    if not content.strip():
        return None

    chunks = chunk_document(content, os.path.basename(file_path), file_path)

    save_path = os.path.join("data", index_name)

    if os.path.exists(save_path):
        vector_store = FAISS.load_local(save_path, embeddings, allow_dangerous_deserialization=True)
        existing_sources = [doc.metadata.get("source") for doc in vector_store.docstore._dict.values()]
        if os.path.basename(file_path) in existing_sources:
            st.warning(f"⚠️ File already indexed, skipping: {os.path.basename(file_path)}")
            return vector_store
        vector_store.add_documents(chunks)
        st.success(f"✅ Indexed new file: {os.path.basename(file_path)}")
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)
        st.success(f"✅ Indexed new file: {os.path.basename(file_path)}")

    vector_store.save_local(save_path)
    return vector_store
