from fastapi import APIRouter, UploadFile, Body
from pydantic import BaseModel
import shutil
import os
import tempfile
import uuid
from service.pdf_loader import load_pdf
from service.vector_store import store_resume_in_vector_db
from service.agent import run_agent

router = APIRouter()

# Global memory cache for Vector Stores keyed by session_id
# If the server restarts, sessions are lost
SESSION_STORES = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post('/analyze-resume')
async def analyze_resume(file: UploadFile):
    # Save to OS temp directory so Uvicorn/LiveServer doesn't trigger a hot-reload and blank the screen
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        file_path = tmp.name

    try:
        # Generate a unique session ID for this conversation
        session_id = str(uuid.uuid4())

        # 1. Load the text from PDF
        text = load_pdf(file_path)
        
        # 2. Chunk and Store the text into FAISS Vector DB
        vector_store = store_resume_in_vector_db(text)
        
        # 3. Store the vector_store in global session cache
        SESSION_STORES[session_id] = vector_store

        # 4. Run the LangGraph agent initially
        result = run_agent(vector_store, session_id=session_id, is_initial=True)

        return {"result": result, "session_id": session_id}
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post('/chat')
async def chat(request: ChatRequest):
    session_id = request.session_id
    message = request.message

    if session_id not in SESSION_STORES:
        return {"result": "Error: Session expired or not found. Please upload your resume again."}

    vector_store = SESSION_STORES[session_id]

    # Run the LangGraph agent for conversational follow-up
    result = run_agent(vector_store, session_id=session_id, message=message, is_initial=False)

    return {"result": result}

