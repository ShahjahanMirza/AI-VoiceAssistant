import time
import ollama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from groq import Groq
import io

load_dotenv()
groq_api_key = os.environ["GROQ_API_KEY"]

def chat_with_groq_llama(text):
    """
    Initiates a conversation with a language model.
    """
    
    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {   
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content



def chat_with_qwen(text):

    response = ollama.chat(model='qwen:1.8b',
                messages=[
                    {
                      "role": "system",
                      "content": "You are a helpful assistant who replies in 2 short sentences"
                    },
                    {
                        'role': 'user', 
                        'content': f'Give a short and to the point answer to the following query. Output should : {text}'
                        }
                ], 
                stream=False)

    return (response['message']['content'])

def chat_with_llama(text, prompt = "Give a short and to the point answer to the following query"):

    response = ollama.chat(model='llama3:8b',
                messages=[
                    {
                        'role': 'user', 
                        'content': f'{prompt}: {text}'
                        }
                ], 
                stream=False)

    return (response['message']['content'])

def chat_with_gemma(text):

    response = ollama.chat(model='gemma:2b',
                messages=[
                    {
                        'role': 'user', 
                        'content': f'Give a short and to the point answer to the following query: {text}'
                        }
                ], 
                stream=False)

    return (response['message']['content'])


# Other functions...

def chat_with_image(text, image_path):
    image_path = image_path.replace('\\','/')
    with open(image_path, 'rb') as image_file:
        image = io.BytesIO(image_file.read())

    message = {
        'role': 'user',
        'content': text,
        'images': [image] 
    }
    
    print('Reading Image...')
    response = ollama.chat(
        model="llava:latest",  
        messages=[message]
    )
    
    return response['message']['content']

# # Usage:
# image_path = r'G:\Personal Assistant Project\project\shaju.jpg'
# print(chat_with_image("What is this image about?", image_path))


def generate_code(text):
    """_summary_
        Use CrewAI to build a code generator.
    Args:
        text (_type_): code file
    """
    pass

def search(text):
    """_summary_
        Use AI to search internet.
    Args:
        text (_type_): search result
    """
    pass