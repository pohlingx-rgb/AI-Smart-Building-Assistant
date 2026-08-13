# 📊 Use Case Comparison

| Feature             | 💬 Chat with Information                                                                 | 📑 Intelligent SOR Search                                                                 |
|---------------------|------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Purpose**         | General FM knowledge retrieval (SOPs, O&M manuals, contracts)                            | Contract compliance validation against Schedule of Rates (SOR)                            |
| **User Input**      | Plain‑language query (e.g., “What are the daily AHU/FCU operating procedures?”)           | Item/repair/procurement query (e.g., “Is a deck‑mounted self‑closing tap available in SOR?”) |
| **Retrieval Method**| Semantic search via FAISS vector store                                                   | Structured clause matching against indexed SOR database                                   |
| **AI Processing**   | LLM Summarizer reformulates SOP/O&M excerpts into clear procedural guidance              | Compliance Validator checks SOR clauses, then LLM reformulates into cost guidance         |
| **Output Style**    | Human‑like explanation with step‑by‑step procedures and inline citations                 | Clear compliance verdict (✅/❌) with contract‑backed cost and source reference             |
| **Example Response**| “Daily AHU/FCU checks include BAS/BMS status, alarms, airflow, condensate management, and documentation. Source: *SOP_AC_001_AHU_FCU_Operation_and_Maintenance.docx*.” | “✅ Compliant. Deck‑mounted self‑closing tap is available in SOR at $94.24. Source: *SOR_IFM Contract.docx*.” |
| **Key Benefit**     | Improves accessibility of technical SOPs and supports operational knowledge transfer     | Ensures procurement decisions align with contractual obligations and governance           |
