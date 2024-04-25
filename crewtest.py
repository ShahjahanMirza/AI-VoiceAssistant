from langchain_community.llms import Ollama
from crewai import Agent, Task, Crew, Process
from groq import Groq
import os
from langchain_groq import ChatGroq

prompt_model = Ollama(model='llama3:8b')
# prompt_model = Ollama(model='tinyllama')
code_model = Ollama(model='codegemma:2b')

# groq_api_key = os.environ["GROQ_API_KEY"]
llm = ChatGroq(api_key='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',
    model="llama3-70b-8192",)


user_query = "program to find out fibonacci series for any given number"

prompt_engineer = Agent(
            role = 'Prompt engineer',
            goal = "accurately convert the user query to a professional step by step prompt",
            backstory = "You are a professional prompt engineer at a big company. Your only job is to write instruction steps from the user query",
            verbose = True,
            allow_delegations = False,
            llm = llm,
            max_iter = 3
)

write_prompt = Task(
    description = f"Write prompt based on this user query: {user_query}",
    agent = prompt_engineer,
    expected_output = "Steps to write code based on the prompt"
)



coder = Agent(
    role = "Programmer",
    goal = "Based on the steps, only write python code",
    backstory = "You are a professional python programmer at a big company. Your only job is to write python code for users to run directly without any errors",
    verbose = True,
    allow_delegations = False,
    llm = llm,
    max_iter = 3
)

prompt_to_code = Task(
    description = f"write correct python code based on this prompt: {write_prompt.output}",
    agent = coder,
    expected_output = "Only python code"
)


crew = Crew(
    agents = [prompt_engineer, coder],
    tasks = [write_prompt, prompt_to_code],
    verbose=2,
    process = Process.sequential
)

output = crew.kickoff()
print(output) 