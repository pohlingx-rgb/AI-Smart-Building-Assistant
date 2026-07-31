import hashlib
import os

import docx
import streamlit as st
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
)


def _hash_content(content: str) -> str:
    """Generate a SHA256 hash of the document content for duplicate detection."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def extract_text_with_pages(file_path):
    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"text": text, "page": i + 1})
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


def split_text(content, chunk_size=1000, chunk_overlap=200):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )
    return splitter.split_text(content)


def chunk_document(content, source, file_path, page=None):
    """Split document into chunks and attach metadata for citations."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = [
        Document(
            page_content=content,
            metadata={
                "source": source,
                "filepath": file_path,
                "page": page,
            },
        )
    ]
    return splitter.split_documents(docs)


def get_index_path(index_name):
    candidates = [os.path.join("data", index_name), index_name]
    for path in candidates:
        if os.path.exists(path):
            return path
    return os.path.join("data", index_name)


def build_vector_store(folders, index_name="combined_ops_index"):
    """Build a new FAISS index from scratch across multiple folders."""
    if isinstance(folders, str):
        folders = [folders]

    all_chunks = []
    seen_hashes = set()

    for folder in folders:
        if not os.path.exists(folder):
            continue
        for file_name in os.listdir(folder):
            file_path = os.path.join(folder, file_name)
            pages = extract_text_with_pages(file_path)
            if not pages:
                continue

            for page in pages:
                text = page["text"]
                if not text.strip():
                    continue
                content_hash = _hash_content(text)
                if content_hash in seen_hashes:
                    st.warning(f"⚠️ Skipped duplicate file content: {file_name}")
                    continue
                seen_hashes.add(content_hash)
                all_chunks.extend(
                    chunk_document(text, file_name, file_path, page=page.get("page"))
                )
                st.success(f"✅ Indexed new file: {file_name}")

    if not all_chunks:
        return None

    os.makedirs(os.path.dirname(os.path.join("data", index_name)), exist_ok=True)
    vector_store = FAISS.from_documents(all_chunks, embeddings)
    save_path = os.path.join("data", index_name)
    vector_store.save_local(save_path)
    return vector_store


def load_vector_store(index_name="combined_ops_index"):
    """Load an existing FAISS index from disk."""
    save_path = get_index_path(index_name)
    if os.path.exists(save_path):
        return FAISS.load_local(
            save_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
    return None


def update_vector_store(file_path, index_name="combined_ops_index"):
    """Incrementally add a new file to an existing FAISS index, skipping duplicates."""
    pages = extract_text_with_pages(file_path)
    if not pages:
        return None

    chunks = []
    for page in pages:
        text = page["text"]
        if text.strip():
            chunks.extend(
                chunk_document(
                    text,
                    os.path.basename(file_path),
                    file_path,
                    page=page.get("page"),
                )
            )

    if not chunks:
        return None

    save_path = os.path.join("data", index_name)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    if os.path.exists(save_path):
        vector_store = FAISS.load_local(
            save_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        existing_sources = [
            doc.metadata.get("source")
            for doc in vector_store.docstore._dict.values()
        ]
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
