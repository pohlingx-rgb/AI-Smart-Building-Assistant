import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Debug print AFTER loading
print("DEBUG: OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_answer(question, docs):
    # Build context and collect sources
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    prompt = f"""
You are a Facilities Management AI Assistant.

Answer ONLY using the context provided.

Context:
{context}

Question:
{question}

At the end of your answer, list the sources used:
Sources: {", ".join(sources)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_sor_answer(question, docs):
    # Build context and collect sources
    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "Unknown") for doc in docs]

    prompt = f"""
You are a Facilities Management Schedule of Rates (SOR) Validator.

Using ONLY the provided context:

Determine:
1. Coverage Status (Covered / Not Covered / Unclear)
2. Relevant Clause
3. Supporting Evidence
4. Source Reference

If information is unavailable, state:
'Information not found in uploaded SOR documents.'

Context:
{context}

Question:
{question}

Sources: {", ".join(sources)}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
