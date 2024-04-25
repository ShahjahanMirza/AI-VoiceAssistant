from models import *
from audios import *
from doc_models import *
from coder import *
from internet_surfer import *
from event_adder import *

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
            print('Upload image...')
            root = Tk()
            root.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Image files", "*.jpg"), ("all files", "*.*")))
            root.destroy()
            print("Selected file: ", root.filename)
            image_path = (root.filename)
            while True:
                user_input = user()
                print(user_input)
                if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all",]):
                    print('Exiting Image...')
                    break
                else:
                    response = chat_with_image(user_input, image_path)
                    speak(response)
            
        
        
        # If user wants to generate code
        elif any(keyword.strip() in user_input.lower() for keyword in ['write code']): # Generate Code
            speak("Please tell me what you want me to code")
            user_input = user()
            result = write_code(user_input)
            filename = "generated_code.py"
            with open(filename, 'w') as f:
                f.write(result)
            speak(f"Code Generated in {filename}")
        
        
        # If the user wants to search the internet
        elif any(keyword.strip() in user_input.lower() for keyword in ['search the internet']): # Search the internet
            print("Search Query: ")
            user_input = user()
            result = search_internet(user_input)
            print("Search Result: ")
            print(result)
            print("Done...")
        
        # If user want to add an event to google calendar
        elif any(keyword.strip() in user_input.lower() for keyword in ['add event']): # Add Event
            print("What do you want to add: ")
            user_input = user()
            response = chat_with_groq_llama("Generate a JSON object to this user query:"+user_input+""". The JSON output should look like this: 
            {"summary: "Google I/O 2015",
            "location": "800 Howard St., San Francisco, CA 94103",
            "description": "A chance to hear more about Google's developer products.",
            "colorId": "8",
            "start": {
                "dateTime": "2024-04-26T09:00:00-07:00",
                'timeZone': 'Asia/Karachi',
            },
            "end": {
                "dateTime": "2024-04-26T09:00:00-07:00",
                'timeZone': 'Asia/Karachi',
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=2"
            ],
            "attendees": [
                {"email": "03318325446sm@gmail.com"},
                {"email": "shahjahanmirza007@gmail.com"} ]}
            Dont change timezones, and attendees. Dont Output any extra words or explanations. A json response is all i require. 
            """)
            # event = json.loads(response)
            print(response)
            # add_event(event)
        
        
        
        # If user want to get events from google calendar
        elif any(keyword.strip() in user_input.lower() for keyword in ['get my events']): # Add Event
            events = get_events()
            response = chat_with_groq_llama("In a report form, tell me which event do i have and when.  Dont output special characters. use the following events: " + str(events))
            speak(response)
        
        
        # If user just want to chat normally
        else:
            response = chat_with_groq_llama(user_input)
            print('Model Speaking...')
            speak(response)
        user_input = None







if __name__ == '__main__':
    main()