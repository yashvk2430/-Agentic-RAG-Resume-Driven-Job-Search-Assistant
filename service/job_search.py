from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def search_jobs(skills: str) -> str:
    """
    Searches the web for relevant job openings WITH LINKS, aiming for 10-15 results.
    """
    # Truncate skills to max 3 so the search engine query doesn't become too restrictive or fail
    skill_list = [s.strip() for s in skills.split(',')]
    core_skills = " ".join(skill_list[:3])
    
    # Configure wrapper to return up to 5 results per search type (total up to 15)
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
    search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    
    combined_results = []
    
    # Perform 3 separate searches to guarantee a mix of job types
    for mode in ["remote", "hybrid", "onsite"]:
        query = f"{mode} {core_skills} developer hiring board"
        try:
            results = search.run(query)
            if results:
                combined_results.append(f"--- {mode.upper()} JOBS ---\n{results}")
        except Exception as e:
            continue
            
    if not combined_results:
        return "No jobs found. The search engine didn't return any results for those top skills."
        
    return "\n\n".join(combined_results)

if __name__ == "__main__":
    print(search_jobs("Python, React, AWS"))
