from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

def build_vector_store(chunks):
    embeddings = OpenAIEmbeddings(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    vector_store = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )
    return vector_store
