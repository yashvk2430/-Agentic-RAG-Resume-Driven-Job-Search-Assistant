from langchain_core.tools import tool
from service.job_search import search_jobs

def get_tools(vector_store):
    
    @tool
    def Retrieve_Resume_Info(query: str) -> str:
        """
        Searches the user's resume for skills, experience, or details. Use this first before searching for jobs.
        Pass a specific query string (e.g., "What are the core technical skills?" or "What is the experience?").
        """
        if not vector_store:
            return "Error: No resume currently loaded in the database."
        docs = vector_store.similarity_search(query, k=4)
        return "\n---\n".join([doc.page_content for doc in docs])

    @tool
    def Search_Jobs(skills: str) -> str:
        """
        Searches the internet for real job listings based on a comma-separated list of skills.
        """
        return search_jobs(skills)

    return [Retrieve_Resume_Info, Search_Jobs]