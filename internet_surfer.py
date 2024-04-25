from groq import Groq
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()



groq_api_key = os.environ["GROQ_API_KEY"]
# llm = Groq(api_key=groq_api_key, model = 'llama3-70b-8192')
llm = ChatGroq(api_key=groq_api_key, model = 'llama3-70b-8192')


# Wikipedia 
from langchain_community.utilities import WikipediaAPIWrapper
wikipedia = WikipediaAPIWrapper()
# print(wikipedia.run('Langchain'))


# DuckDuckGo Search
from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()
# print(search.run('Bitcoin Price ?'))

from langchain.tools import tool

def search_internet(text):
    @tool
    def wikipedia_search(prompt: str) -> str:
        """Useful for when you need to look up a topic, country or person on wikipedia"""
        return wikipedia.run(prompt)

    @tool
    def duckduck_search(prompt: str) -> str:
        """Useful for when you need to do a search on the internet to find information that another tool can't find. be specific with your input."""
        return search.run(prompt)


    from langchain.agents import initialize_agent
    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description", 
        tools=[wikipedia_search, duckduck_search], 
        llm=llm,
        verbose=True,
        max_iterations=5,
    )

    return zero_shot_agent.run(f"Output a simple and to the point answer to the question: {text}")

# print(search_internet("What is the url of Facebook?"))