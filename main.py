from models import *
from audios import *
from doc_models import *


audio_save_path = './audios/audio.wav'


def user():
    listen(audio_save_path=audio_save_path) # User audio to file
    audio_text = transcribe(audio_file_path=audio_save_path) # User audio file to text
    return (audio_text)

def main():

    print("Setting up the Assistant...")
    
    
    print('Ready...')
    
    
        
    while True:
        user_input = user()
        print('User: ', user_input)
        # If user doesnt want to talk more, just add bye or exit 
        if any(keyword.strip() in user_input.lower() for keyword in ['bye', 'exit']):
            speak(transcribed_text='Okay, bye.')
            print('Exiting...')
            break
        
        
        # If user want to add information to the document
        elif any(keyword.strip() in user_input.lower() for keyword in ['add information']): # Add information
            print('adding information...')
            user_input = user()
            most_common_chunks, paragraphs = (update_document(user_input))
        
        
        # If uer wants to talk to document
        elif any(keyword.strip() in user_input.lower() for keyword in ['give information']): # Talk to Document
            most_common_chunks, paragraphs = (update_document(''))
            print('talking to information document...')
            user_input = user()
            response = chat_with_doc(user_input, most_similar_chunks = most_common_chunks, paragraphs=paragraphs )
            speak(response)
        
        
        #If user wants to talk to document
        elif any(keyword.strip() in user_input.lower() for keyword in ['upload document']): # Upload Document
            print('uploading document...')
            filename = upload_document()
            most_common_chunks, paragraphs = (update_document(filename=filename))
            while True:
                user_input = user()
                print(user_input)
                if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all"]):
                    print('Exiting Document...')
                    break
                response = chat_with_doc(user_input, most_similar_chunks = most_common_chunks, paragraphs=paragraphs )
                speak(response)
        
        # If user want to talk to Image
        elif any(keyword.strip() in user_input.lower() for keyword in ['upload image']): # Talk to Image
            pass
        
        
        # If user wants to generate code
        elif any(keyword.strip() in user_input.lower() for keyword in ['write code']): # Generate Code
            pass
        
        
        # If user want to add an event to google calendar
        elif any(keyword.strip() in user_input.lower() for keyword in ['add event']): # Add Event
            pass
        
        
        # If user just want to chat normally
        else:
            response = chat_with_qwen(user_input)
            print('Model Speaking...')
            speak(response)
        user_input = None






















if __name__ == '__main__':
    main()