from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema.document import Document
import io
import os

class RagService:
    def __init__(self):
        # Use OpenAI for embeddings and the chat model
        self.embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.vector_store = None

    def ingest_document(self, file_bytes: bytes, filename: str):
        # Create a file-like object in memory from the uploaded bytes
        pdf_file = io.BytesIO(file_bytes)
        # Use a temporary file for PyPDFLoader
        documents = PyPDFLoader(pdf_file).load()
        
        # Split the document into chunks
        chunks = self.text_splitter.split_documents(documents)
        
        # Create the vector store from the chunks
        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory="./chroma_db"  # Saves the vectors locally
        )
        self.vector_store.persist()

    def ask_question(self, question: str):
        if not self.vector_store:
            raise ValueError("No document has been processed yet.")
        
        # Create a Retriever -> Chain pipeline
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 3}) # Get top 3 relevant chunks
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff", # "Stuff" is simplest: stuffs all chunks into the prompt
            retriever=retriever,
            return_source_documents=False
        )
        
        result = qa_chain.invoke({"query": question})
        return result["result"]