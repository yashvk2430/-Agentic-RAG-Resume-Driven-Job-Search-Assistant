from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_skills(text):
    prompt=f""" 
    Extract all the technical skills from the following text and return them as a comma-separated list.
    
    Text: {text}
    
    Skills: 
    """
    response=llm.invoke(prompt)
    return response.content

if __name__ == "__main__":
    print(extract_skills("I have 2 years of experience in Python and Java also NLP and Machine Learning"))