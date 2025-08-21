# DocuChat - RAG PDF Assistant

A full-stack application that demonstrates Retrieval-Augmented Generation (RAG). Users can upload a PDF and ask questions whose answers are derived directly from the document's content.

## 🚀 Tech Stack

*   **Frontend:** Next.js, React
*   **Backend:** FastAPI (Python)
*   **AI Orchestration:** LangChain
*   **LLM:** OpenAI GPT-3.5-Turbo
*   **Vector Database:** ChromaDB
*   **Infrastructure:** Docker, Docker Compose

## 🏗️ Architecture

1.  **Upload:** PDF is uploaded to the FastAPI backend.
2.  **Processing:** LangChain splits the text into chunks, generates embeddings (using OpenAI), and stores them in ChromaDB.
3.  **Query:** A user question is converted to an embedding. ChromaDB performs a similarity search to find the most relevant text chunks.
4.  **Generation:** LangChain stuffs the relevant chunks into a prompt for the OpenAI LLM, which generates a contextual answer.

## 🛠️ Installation & Setup

1.  Clone the repo: `git clone <your-repo-url>`
2.  Add your OpenAI API key to `backend/.env`: `OPENAI_API_KEY=sk-your-key-here`
3.  Run with Docker: `docker-compose up --build`
4.  Open [http://localhost:3000](http://localhost:3000)

## 📸 Demo

[I will add a link to a short screen recording (e.g., on Google Drive or Loom) showing me using the app!]