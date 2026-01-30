# Event-Driven RAG Agent

A robust, event-driven Retrieval-Augmented Generation (RAG) agent built to ingest PDFs, generate embeddings asynchronously, and answer user queries with context.

This project leverages **Inngest** for durable workflow orchestration, **Qdrant** for vector storage, **LlamaIndex** for document processing, and **Streamlit** for the user interface.

## 🚀 Features

* **Async PDF Ingestion**: Uploads are processed in the background using Inngest events (`rag/ingest_pdf`), ensuring the UI remains responsive.
* **Durable Workflows**: Uses Inngest steps to handle failures, retries, and state management during ingestion and retrieval.
* **Vector Search**: Efficient similarity search using **Qdrant**.
* **Advanced RAG**: Uses **LlamaIndex** for chunking and **OpenAI** (`text-embedding-3-large`) for high-quality embeddings.
* **Interactive UI**: Clean interface built with **Streamlit** to upload documents and chat with your data.

## 🛠️ Tech Stack

* **Workflow Orchestration**: [Inngest](https://www.inngest.com/)
* **Backend API**: FastAPI
* **Frontend**: Streamlit
* **Vector Database**: Qdrant
* **Package Manager**: uv
* **LLM & Embeddings**: OpenAI (GPT-4o-mini & text-embedding-3-large)

## 📂 Project Structure

```bash
├── main.py             # FastAPI app & Inngest function definitions
├── streamlit_app.py    # Frontend UI for uploading PDFs and chat
├── data_loader.py      # Logic for loading PDFs and generating embeddings
├── vector_db.py        # Qdrant client wrapper
├── custom_types.py     # Pydantic models for data validation
├── pyproject.toml      # Project dependencies (uv)
└── .env                # Environment variables (API Keys)
```
## ⚙️ Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.13+**
- [**uv**](https://github.com/astral-sh/uv) (Python package manager)
- **Docker Desktop** (for running Qdrant)
- **Node.js & npm** (for running the Inngest CLI)

## 📦 Installation & Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/amanparganiha/Event-Driven-RAG-Agent.git && cd Event-Driven-RAG-Agent
    ```
    
2. **Install dependencies using uv:**
    ```bash
    uv sync
    ```
    
3. **Set up Environment Variables:**
Create a `.env` file in the root directory and add your keys:
    ```bash
    OPENAI_API_KEY=sk-your-openai-key-here
    ```

## 🏃‍♂️ Running the Application

This system requires 4 components running simultaneously. Open 4 separate terminal windows.

### Step 1: Start Vector Database (Qdrant)

Make sure **Docker Desktop** is running, then run:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### Step 2: Start the Backend API

In a new terminal, run the FastAPI server (Main App):

```bash
uv run uvicorn main:app
```

### Step 3: Start the Inngest Dev Server

In a new terminal, run the Inngest CLI to manage workflows:

```bash
npx inngest-cli@latest dev -u [http://127.0.0.1:8000/api/inngest](http://127.0.0.1:8000/api/inngest) --no-discovery
```

### Step 4: Start the Frontend (Streamlit)

In the final terminal, launch the user interface:

```bash
uv run streamlit run .\streamlit_app.py
```

## 💡 How to Use

1. Open the Streamlit app in your browser (usually `http://localhost:8501`).
2. **Upload a PDF**: The app will send an event to Inngest to parse and embed the document.
3. **Wait for Processing**: You can check the Inngest dashboard to see the `rag/ingest_pdf` function running.
4. **Ask a Question**: Type a query into the chat box. The agent will retrieve relevant context from Qdrant and generate an answer.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
