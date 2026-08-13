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

    %% Make all connectors white
    linkStyle default stroke:#ffffff,stroke-width:2px;

    %% Color styling per layer
    style Roles fill:#b3d9ff,stroke:#333,stroke-width:1px
    style Governance fill:#ffe6b3,stroke:#333,stroke-width:1px
    style DataLayer fill:#e6e6e6,stroke:#333,stroke-width:1px
    style AIProcessing fill:#d9b3ff,stroke:#333,stroke-width:1px
    style UseCases fill:#b3ffb3,stroke:#333,stroke-width:1px
