"""
Testing to see if the LLM can classify the intent of the user query, 
and based on that we can use If else statements to respond accordingly
"""


from groq import Groq
import os

client = Groq(api_key=os.environ["GROQ_API_KEY"],)


SYSTEM_PROMPT = """ You are a helpful assistant. You either reply in 2 short sentences to the users query or classify the intent of the user query.
These are your options:
'exit': if the user wants to end the conversation,
'store information': if the user wants to save ay kind of information,
'retrieve information': if the user wants to retrieve any information from the stored information,
'upload document': if the user wants to upload a document and talk about it
'upload image': if the user is talking about uploading an image,
'click image': if the user is talking about taking an image,
'generate code': if the user wants to generate code for any language,
'fix code': if the user wants to fix any code file,
'search internet': if the user wants to get results from the internet or the information he needs can only be found in the internet,
'add event': if the user wants to add an event to the calendar 
'get events': if the user wants to get the upcoming events from the calendar,

Only reply with the option after clearly classifying the intent of the user query, or reply with simple answer to the user query. If you dont understand,
reply with 'i dont understand'.
"""

def chat_with_groq_llama_3(user_input):
    chat_completion = client.chat.completions.create(
        messages = 
        [
            {
            'role': 'system',
            'content':SYSTEM_PROMPT
            },
            {'role': 'user',
            'content': user_input
            }
        ],
        model = "llama3-70b-8192",
    )
    return chat_completion.choices[0].message.content


