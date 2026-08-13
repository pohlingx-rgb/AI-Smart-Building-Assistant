import logging
from datetime import datetime

import streamlit as st

from modules.disclaimer import show_disclaimer

logging.basicConfig(filename="audit.log", level=logging.INFO)


def log_event(event):
    logging.info(f"{datetime.now()} - {event}")


def show_methodology():
    st.title("⚙️ Methodology")

    st.write("""
    Our AI Smart Building Assistant is implemented as a **Streamlit‑based web application** powered by **Large Language Models (LLMs)** with **Retrieval‑Augmented Generation (RAG)**. 
    The methodology explains how data flows through the system, how modules interact, and how each use case is supported.
    """)

    st.subheader("🔄 Data Flow Overview")

    st.write("""
    1. **Document Upload** → Admins upload FM documents (SOR, SOPs, O&M manuals, contracts).
    2. **Vector Store Indexing** → Files embedded into FAISS for semantic search.
    3. **User Query Processing** → Queries passed to vector store for retrieval.
    4. **LLM Summarisation** → Retrieved excerpts processed with prompt engineering.
    5. **UX Integration** → Results displayed in chatbot UI with citations, history, and admin controls.
    """)

    st.subheader("🛠️ Implementation Details")

    st.write("""
    1. **Streamlit Pages** — Each module (SOR Validator, Operations Assistant, History) implemented as separate files with **show_*()** functions.
    2. **Session State** — Manages role separation (Admin vs User), history logging, and pagination.
    3. **FAISS Vector Store** — Provides efficient similarity search across uploaded documents.
    4. **LLM Integration** — GPT‑based models configured with prompt engineering for domain‑specific responses.
    5. **Safety Features** — Role‑based access, prompt injection safeguards, error handling, and audit logging.
    """)

    st.subheader("🧾 Audit Logging & Traceability")

    st.write("""
    The system includes an audit log to record all user and admin actions, ensuring transparency and traceability. Each event — such as document uploads, note additions, or validation checks — is timestamped and stored in a log file (audit.log).
    
    Key Benefits:
    1. **Operational Accountability** — Tracks who performed each action and when.
    2. **Data Integrity** — Provides a verifiable record of document interactions.
    3. **Security & Compliance** — Supports audit trails for FM governance and contract validation.
    4. **Debugging Support** — Helps developers monitor system behavior and troubleshoot issues efficiently.
    
    This feature strengthens the system’s reliability and aligns with best practices in smart building data management.
    """)

    st.subheader("🔐 Role‑Based Access Control")

    st.write("""
    The system enforces strict role separation between Admins and Users:
    1. **Admin Role** — Can upload, categorize, and delete documents (SOR, SOPs, O&M manuals, contracts). Upload features are visible only to Admins.
    2. **User Role** — Can query documents and view results but cannot upload or manage files. The upload button is hidden/disabled for Users to prevent unauthorized changes.
    
    Key Benefits:
    1. **Security** — Prevents unauthorized document uploads or deletions.
    2. **Governance** — Ensures only validated documents enter the knowledge base.
    3. **Clarity** — Users see only relevant features, reducing interface clutter.
    4. **Compliance** — Aligns with FM best practices where document control is restricted to authorized personnel.
    """)

    st.subheader("💬 Use Case A: Chat with Information")
    
    st.write("""
    Supports general FM knowledge retrieval across SOPs, O&M manuals, and contracts.
    
    Example Query: “*I’m new to the building, can you tell me what are the daily operating and monitoring procedures for checking of the AHU / FCU?*"
    
    System Response Flow:
    - User Input → Plain‑language query about daily procedures.
    - Semantic Search → Retrieves relevant SOP/O&M document sections.
    - LLM Summarisation → Reformulates technical steps into a structured checklist.
    - Output Display → Presents guidance with citations.
    
    Response Example:
    "*Welcome to the building! Here’s a quick overview of the daily operating and monitoring procedures for AHUs and FCUs:
    • Start‑of‑Day Checks — BAS/BMS status, alarms, air conditioning availability, physical inspection, documentation.
    • First‑Line Operator Checks — Power supply, thermostat settings, airflow, condensate management, scope of fault.
    • Alarm Response Procedure — Standardised monitoring, preventive maintenance, troubleshooting.*"
    
    Sources: "*SOP_AC_001_AHU_FCU_Operation_and_Maintenance.docx*”

    Outcome:
    1. ✅ Provides accessible operational guidance for new staff.
    2. ✅ Improves knowledge transfer from SOPs into daily practice.
    3. ✅ Supports thermal comfort, equipment reliability, and indoor air quality.
    """)

    st.subheader("📑 Use Case B: Intelligent SOR Search")

    st.write("""
    Supports contract compliance checks against the Schedule of Rates.
    
    Example Query: "*I have a leaking deck‑mounted self‑closing tap! Can check whether item is available in SOR and what is the cost for replacement?*"
    
    System Response Flow:
    1. User Input → The query specifies a repair/procurement item (deck‑mounted self‑closing tap).
    2. SOR Clause Matching → The system searches the indexed Schedule of Rates (SOR) database for relevant entries.
    3. Compliance Validation → The Compliance Validator confirms that the item is covered under contract.
    4. LLM Reformulation → The raw contract entry is reformulated into a clear, user‑friendly answer with actionable steps.
    5. Output Display → The chatbot presents the cost and source references.
    
    Response:

    “*If you’re dealing with a leaking deck‑mounted self‑closing tap, it’s available for replacement in the SOR inventory.
    Cost: $94.24
    Next steps: Confirm availability, purchase, and arrange installation if needed.
    Sources: "*SOR_IFM Contract.docx*"*"

    Outcome:
    1. ✅ Provides a contract‑backed cost for procurement decisions.
    2. ✅ Ensures compliance with SOR clauses.
    3. ✅ Strengthens governance by citing the official source document.
    4. ✅ Offers actionable guidance (e.g., availability, purchase, installation) beyond just cost lookup.
    
    """)

    st.subheader("📊 Use Case Comparison")

    st.markdown("""

    | Feature             | 💬 Chat with Information                                                                 | 📑 Intelligent SOR Search                                                                 |
    |---------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
    | **Purpose**         | General FM knowledge retrieval (SOPs, O&M manuals, contracts)                            | Contract compliance validation against Schedule of Rates (SOR)                            |
    | **User Input**      | Plain‑language query (e.g., “What are the daily AHU/FCU operating procedures?”)          | Item/repair/procurement query (e.g., “Is a deck‑mounted self‑closing tap available in SOR?”) |
    | **Retrieval Method**| Semantic search via FAISS vector store                                                   | Structured clause matching against indexed SOR database                                   |
    | **AI Processing**   | LLM Summarizer reformulates SOP/O&M excerpts into clear procedural guidance              | Compliance Validator checks SOR clauses, then LLM reformulates into cost guidance         |
    | **Output Style**    | Human‑like explanation with step‑by‑step procedures and inline citations                 | Clear compliance verdict with contract‑backed cost and source reference             |
    | **Example Response**| “Daily AHU/FCU checks include BAS/BMS status, alarms, airflow, condensate management, and documentation. Source: *SOP_AC_001_AHU_FCU_Operation_and_Maintenance.docx*.” | “Deck‑mounted self‑closing tap is available in SOR at $94.24. Source: *SOR_IFM Contract.docx*.” |
    | **Key Benefit**     | Improves accessibility of technical SOPs and supports operational knowledge transfer     | Ensures procurement decisions align with contractual obligations and governance           |
    """)

    st.subheader("🎛️ Enhancing User Experience")

    st.write("""
    1. Beyond backend architecture and compliance validation, the assistant is designed with user‑centric features that make interactions smoother, clearer, and more trustworthy:
    2. Source Display Options → Users can toggle between “Show Sources Only” (raw excerpts) and summarized answers, giving flexibility depending on whether they need detail or quick guidance.
    3. Summarization Toggle → Allows switching between concise answers and full contextual explanations, improving readability for both operators and evaluators.
    4. Pagination & History Controls → Users can navigate past queries, review previous answers, and download logs, supporting auditability and knowledge transfer.    
    
    ✨ Impact
    These enhancements ensure that the assistant is not only technically robust but also accessible, transparent, and evaluator‑friendly. 
    They demonstrate attention to human factors — empowering FM teams to trust the system, adapt outputs to their needs, and maintain governance without sacrificing usability.
    """)


    st.subheader("🧪 Evaluation & Testing")

    st.write("""
    1. Tested with sample SOP, SOR, and O&M documents to validate retrieval accuracy.
    2. Iterative UX improvements: summarization toggle, pagination fixes, admin clear history.
    3. Feedback loop from FM practitioners to refine clarity, compliance checks, and trustworthiness.
    """)

    st.subheader("📊 Diagram Caption")

    st.write("""
    System Workflow: Upload → Index → Search → Summarize → Display
    """)

    st.write("""
    ```mermaid
    flowchart TD
    subgraph Roles["🔐 Role Separation Layer"]
        Admin[👨‍💼 Admin: Upload Documents]
        User[👤 User: Query & View Results]
    end

    subgraph Governance["🧾 Governance Features"]
        RBAC[🔐 Role-Based Access Control]
        Audit[🧾 Audit Log]
    end

    subgraph DataLayer["📂 Data Layer"]
        Repo[📁 Document Repository]
        Vector[🧮 FAISS Vector Database]
    end

    subgraph AIProcessing["🧠 AI Processing Layer"]
        Engine[🔍 Query Engine]
        Summarizer[🧠 LLM Summarizer]
        Validator[🛠️ Compliance Validator]
    end

    subgraph UseCases["💬 Use Case Layer"]
        Chat[💬 Chat with Information]
        SOR[📑 Intelligent SOR Search]
    end

    Admin --> Repo
    User --> Vector
    Repo --> Vector
    Vector --> Engine
    Engine --> Summarizer
    Engine --> Validator
    Summarizer --> Chat
    Validator --> SOR
    RBAC -.-> Admin
    Audit -.-> Repo
    Audit -.-> Vector

    %% Make all connectors black
    linkStyle default stroke:#000000,stroke-width:2px;

    %% Color styling per layer
    style Roles fill:#b3d9ff,stroke:#333,stroke-width:1px
    style Governance fill:#ffe6b3,stroke:#333,stroke-width:1px
    style DataLayer fill:#e6e6e6,stroke:#333,stroke-width:1px
    style AIProcessing fill:#d9b3ff,stroke:#333,stroke-width:1px
    style UseCases fill:#b3ffb3,stroke:#333,stroke-width:1px
""")

    st.caption(
    "Figure 1: Layered architecture of the AI Smart Building Assistant. "
    "Admins upload SOPs, O&M manuals, and SOR documents into the repository, "
    "Users query via the vector database, "
    "Governance features (RBAC and Audit) enforce compliance, "
    "AI modules (Query Engine, Summarizer, Validator) transform data, "
    "and outputs branch into two workflows: "
    "💬 Chat with Information (e.g., AHU/FCU daily procedures) "
    "and 📑 Intelligent SOR Search (e.g., deck-mounted self-closing tap compliance and cost). "
    "Enhancing user experience features — such as summarization toggles, source display options, "
    "and question history navigation — ensure transparency, flexibility, and usability across all interactions."
    )

    log_event(f"{st.session_state.username} viewed Methodology page.")

    show_disclaimer()