import streamlit as st

from modules.disclaimer import show_disclaimer

st.title("Methodology")

st.markdown("""
## RAG Workflow

User Uploads Documents
↓
Document Loader
↓
Text Chunking
↓
Embeddings
↓
FAISS Vector Store
↓
Retriever
↓
LLM
↓
Answer + Source References

### Steps

1. Document Upload
2. Text Extraction
3. Chunking
4. Embedding Generation
5. FAISS Storage
6. Retrieval
7. LLM Response Generation
8. Source Citation
""")

show_disclaimer()