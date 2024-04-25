import os
import crewai_tools
from crewai import Agent, Task, Crew, Process
from crewai.memory.contextual import contextual_memory
from crewai_tools import SerperDevTool
from langchain_community.llms import Ollama


os.environ["SERPER_API_KEY"] = "10a9d81b97926379900a5519b05a919802ef770e"
model = Ollama(model="llama3:8b")

query = "what is the meaning of life"

researcher = Agent(
    role = "Researcher",
    goal = "Research internet to find the optimum answer for the question",
    backstory = "You are a researcher at a big company. Your only job is to find the best possible answers from the internet",
    memory = contextual_memory,
    verbose = True,
    allow_delegations = False,
    tools = [SerperDevTool()]
)

formatter = Agent(
    role = 'Summarizer',
    goal = 'Summarize the research results in short meaningful sentences',
    backslash = 'You are a professional summarizer at a big company. Your only job is to summarize the research results in short meaningful sentences',
    memory = contextual_memory,
    llm = model,
    verbose = 2,
    allow_delegations = False
)

researcher_task = Task(
    description = f"Research internet to find the optimum answer for the question: {query}",
    expected_output = "material related to the question from internet",
    agent = researcher
)

summarizer_task = Task(
    description = f"summarize the 'research' results",
    expected_output = "summarized answer for the question",
    agent = formatter
)

crew = Crew(
    agents = [researcher, formatter],
    tasks = [researcher_task, summarizer_task],
    verbose=2,
    process = Process.sequential
)

output = crew.kickoff()
print(output) 