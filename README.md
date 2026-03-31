# Agentic RAG: Resume-Driven Job Search Assistant

An advanced, agentic RAG (Retrieval-Augmented Generation) application that analyzes your resume, extracts key skills, and automatically searches the web for relevant job listings using a ReAct-style AI agent.

## 🚀 Features

- **PDF Resume Upload**: Automatically parses contents from uploaded PDF resumes.
- **Intelligent Vector Search**: Uses FAISS and HuggingFace embeddings (`all-MiniLM-L6-v2`) for efficient local context retrieval.
- **Agentic ReAct Workflow**: Built with **LangGraph**, the agent follows a multi-step reasoning process:
    1. Retrieves technical context from your resume.
    2. Searches the live web for real-time job listings (Remote, Hybrid, On-site).
    3. Provides a professional summary and a direct list of application links.
- **Multi-Turn Chat**: Maintain context across conversations to refine search results or ask follow-up questions about specific roles.
- **Groq Acceleration**: High-speed inference using the **Groq LPU** (Large Language Model processing unit).

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python 3.10+)
- **AI Orchestration**: LangGraph, LangChain
- **LLM**: Groq (Model: `openai/gpt-oss-120b`) / Google Gemini (Backup)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
- **Frontend**: Vanilla HTML/CSS/JS with `marked.js` for Markdown rendering.

## 📋 Prerequisites

- Python 3.10 or higher
- A Groq API Key (get one at [groq.com](https://groq.com))
- (Optional) A Google Gemini API Key

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Agentic_RAG
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv myenv
   myenv\Scripts\activate  # On Windows
   source myenv/bin/activate  # On Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add your keys:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   GOOGLE_API_KEY=your_gemini_api_key_here (optional)
   ```

## 🏃 Running the Application

1. **Start the FastAPI server**:
   ```bash
   myenv\Scripts\uvicorn app.main:app --reload --port 8000
   ```

2. **Access the Web UI**:
   Open your browser and navigate to: `http://127.0.0.1:8000`

## 📂 Project Structure

- `app/` - FastAPI application entry points and API routes.
- `service/` - Core logic, including the AI Agent, Vector Store, and Tools.
- `frontend/` - Static web assets (HTML, CSS, JS).
- `requirements.txt` - Python package dependencies.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
Built with ❤️ using LangGraph and FastAPI.
