from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def store_resume_in_vector_db(text: str):
    """
    Chunks the given text and stores it in an in-memory FAISS vector database.
    Returns the vector store object.
    """
    # 1. Chunk the text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # If the text is empty or too short, ensure there's at least one chunk
    if not chunks:
        chunks = [text] if text else ["No resume content found."]

    # 2. Setup Embeddings
    # Using all-MiniLM-L6-v2 which is fast and lightweight for local embedding
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # 3. Create FAISS vector store
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    return vector_store
