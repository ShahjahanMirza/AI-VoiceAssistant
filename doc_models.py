
from models import chat_with_llama
from datetime import datetime
import os
import json
import ollama
from numpy.linalg import norm
import numpy as np
from audios import speak
import tkinter as tk
from tkinter import filedialog
from tkinter import *

filename = 'info_doc.txt'

def update_document(text='', prompt = "understand the provided text. Convert and Reply ONLY with the key-points. Dont come up with any material that is not in the provided text", filename=filename):
    if text != '':
        with open("docs/"+filename, "a") as f:
            f.write('\n\nEvent Added Date: ' + datetime.today().strftime('%B %d, %Y'))
            f.write(chat_with_llama(text, prompt))     
        
    paragraphs = parse_file(filename)
    embeddings = get_embeddings(filename, paragraphs)
    prompt_embedding = ollama.embeddings(model='nomic-embed-text', prompt=prompt)[
        'embedding'
        ]
    most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]
    
    print('Document Updated...')
    
    return most_similar_chunks, paragraphs


def parse_file(filename = filename):
    if 'info_doc.txt' in filename:
        file = 'docs/info_doc.txt'
    else: file = filename.replace('\\', '/')
    with open(file, encoding='utf-8-sig') as f:
        paragraps = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif len(buffer):
                paragraps.append(' '.join(buffer))
                buffer = []
        if len(buffer):
            paragraps.append(' '.join(buffer))
    return paragraps


def save_embeddings(filename, embeddings):
    """
    Save embeddings to a JSON file.
    """
    filename = filename.split('/')[-1]
    print(f"Saving embeddings to embeddings/{filename}.json")
    embeddings_dir = "embeddings/"
    if not os.path.exists(embeddings_dir):
        os.makedirs(embeddings_dir)
    file_path = os.path.join(embeddings_dir, f"{filename}.json")
    print(f"Creating embeddings to {file_path}")
    with open(file_path, "w") as f:
        json.dump(embeddings, f)


def get_embeddings(filename, chunks):
    filename = filename.split('/')[-1]
    if (embeddings := load_embeddings(filename)) is not False:
        return embeddings
    
    embeddings = [
        ollama.embeddings(model='nomic-embed-text', prompt=chunk)
        ['embedding'] for chunk in chunks
    ]   
    save_embeddings(filename, embeddings)
    return embeddings
    

def load_embeddings(filename):
    filename = filename.split('/')[-1]
    print(f"Loading embeddings from embeddings/{filename}.json")
    if not os.path.exists(f"embeddings/'{filename}.json'"):
        return False
    # load embeddings from json
    with open(f"embeddings/'{filename}.json'", "r") as f:
        return json.load(f)


def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item)/(needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)


def chat_with_doc(user_input, paragraphs, most_similar_chunks, SYSTEM_PROMPT="""Answer the following question based only on the provided context. 
                                        Dont answer other than based on the provided context. If you dont know the answer, reply "I dont know """, filename = 'info_doc.txt'):
    
    response = ollama.chat(
        model='llama3:8b',
        messages = [{
            'role': 'system',
            'content': SYSTEM_PROMPT+' '.join([paragraphs[item[1]] for item in most_similar_chunks])
        },
        {'role': 'user', 'content': user_input}
        ],
    )
    
    if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all"]):
            speak(transcribed_text='Okay, Closing Document.')
            print('Exiting...')
    else:
        return (response['message']['content'])


def upload_document():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    root.destroy()
    print("Selected file: ", root.filename)
    return (root.filename)