from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.rag_service import RagService
import os

app = FastAPI(title="DocuChat API")

# Configure CORS to allow requests from your Next.js frontend
# This is crucial for the frontend to talk to the backend!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The address of your Next.js app
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Global variable for the RAG service
rag_service = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to upload a PDF and process it into the vector store."""
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid file type. Please upload a PDF.")
    
    contents = await file.read()
    global rag_service
    rag_service = RagService() # Initialize with the PDF bytes
    rag_service.ingest_document(contents, filename=file.filename)
    
    return {"message": f"File '{file.filename}' processed successfully! You can now ask questions."}

@app.post("/chat")
async def chat(question: str):
    """Endpoint to ask a question about the uploaded document."""
    global rag_service
    if rag_service is None:
        raise HTTPException(400, detail="Please upload a document first.")
    
    try:
        # This is where the LangChain magic happens
        answer = rag_service.ask_question(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "DocuChat API is running!"}