import time
import ollama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from groq import Groq
import io
import google.generativeai as genai
from PIL import Image

load_dotenv()
groq_api_key = os.environ["GROQ_API_KEY"]
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def chat_with_groq_llama(text):
    """
    Initiates a conversation with a language model.
    """
    
    client = Groq(api_key=groq_api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant, who replies in 2 short sentences. If you dont understand anything, just reply 'i do not understand'.",
            },
            {   
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content



def chat_with_phi(text):

    response = ollama.chat(model='phi3',
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
        'content': f"Give a very short answer to the following query: {text}",
        'images': [image] 
    }
    
    print('Reading Image...')
    response = ollama.chat(
        model="llava:latest",  
        messages=[message]
    )
    
    return response['message']['content']


def chat_with_image_gemini(text, image_path):
    image_path = image_path.replace('\\','/')
    image = Image.open(image_path)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)
    
    image_parts = [
      {
        "mime_type": 'image/png',
        "data": image_bytes.read()  
      }
    ]
    
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(
        [text, image_parts[0]]
    )
    
    return response.text

# # Usage:
# image_path = r'C:\Users\Shahjahan.DESKTOP-MBDJTPL\Desktop\shaju.png'
# print(chat_with_image("What is this image about?", image_path))


# print(chat_with_image_gemini("what is the gender of the person in the image?",r'C:\Users\Shahjahan.DESKTOP-MBDJTPL\Desktop\shaju.png'))