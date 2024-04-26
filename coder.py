from groq import Groq
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain.tools import tool
from langchain_community.utilities import PythonREPL
from langchain.agents import initialize_agent
from tkinter import filedialog
from tkinter import *
load_dotenv()


groq_api_key = os.environ["GROQ_API_KEY"]
# llm = Groq(api_key=groq_api_key, model = 'llama3-70b-8192')
llm = ChatGroq(api_key=groq_api_key, model = 'llama3-70b-8192')


def write_code(text):
    print('Writing code...')
    repl = PythonREPL()
    @tool
    def python_repl(prompt: str) -> str:
        """useful for when you need to use python to answer a question. You should input python code"""
        return repl.run(prompt)
    
    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description", 
        tools=[python_repl], 
        llm=llm,
        verbose=True,
        max_iterations=10,
    )
    
    return zero_shot_agent.run(f"Write python code for {text}. ONLY output code without any explanation or extra words. Use proper python syntax for output. With new lines and spaces")
# print(write_code("fibonacci series of any given number"))



def code_fix():
    print("Fixing code...")
    repl = PythonREPL()
    @tool
    def python_repl(prompt: str) -> str:
        """useful for when you need to use python to answer a question. You should input python code"""
        return repl.run(prompt)
    
    zero_shot_agent = initialize_agent(
        agent="zero-shot-react-description", 
        tools=[python_repl], 
        llm=llm,
        verbose=True,
        max_iterations=10,
    )
    
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.py"), ("all files", "*.*")))
    root.destroy()
    print("Selected file: ", root.filename)
    file_path = (root.filename)
    with open(file_path, 'rb') as f:
        content = f.read()
    
    fixed = zero_shot_agent.run(f"Fix this python code: {content}. ONLY output the correct working code without any explanation or extra words. Use proper python syntax for output With new lines and spaces")
    
    with open(file_path, 'w') as f:
        f.write(fixed) 
    
    return True
    

# print(code_fix("""def div(a, b):
#     b,a = a,b
#     return a * b"""))




# client = Groq(api_key=groq_api_key)

# def write_code(text):
#     groq = client.chat.completions.create(
#         model='llama3-70b-8192',
#         messages = [{
#             'role': 'system',
#             'content': 'Only output the code. Dont write any extra text. Use \\t or \\n for indentation  and new lines in the code'
#         },
#         {'role': 'user', 'content': 'Python code for {text}'}
#         ]
#     )