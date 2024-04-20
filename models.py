import time
import ollama


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

import io

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


