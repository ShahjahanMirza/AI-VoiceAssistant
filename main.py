from models import *
from audios import *
from doc_models import *
from coder import *
from internet_surfer import *
from event_adder import GoogleCalendar
from images_test import capture_image
import os.path
import datetime as dt

audio_save_path = './audios/audio.wav'
# calendar = GoogleCalendar()


lang_extensions = {
    "javascript": ".js",
    "python": ".py",
    "c++": ".cpp",
}


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
            speak('adding information')
            user_input = user()
            most_common_chunks, paragraphs = (update_document(user_input))
        
        
        
        # If uer wants to talk to document
        elif any(keyword.strip() in user_input.lower() for keyword in ['give information']): # Talk to Document
            most_common_chunks, paragraphs = (update_document(''))
            speak('talking to information document')
            user_input = user()
            response = chat_with_doc(user_input, most_similar_chunks = most_common_chunks, paragraphs=paragraphs )
            speak(response)
        
        
        
        #If user wants to talk to document
        elif any(keyword.strip() in user_input.lower() for keyword in ['upload document']): # Upload Document
            speak('Please upload document')
            filename = upload_document()
            most_common_chunks, paragraphs = (update_document(filename=filename))
            while True:
                user_input = user()
                print(user_input)
                if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all"]):
                    speak('Closing Document')
                    break
                response = chat_with_doc(user_input, most_similar_chunks = most_common_chunks, paragraphs=paragraphs )
                speak(response)
        
        
        
        # If user want to talk to Image
        elif any(keyword.strip() in user_input.lower() for keyword in ['upload image']): # Talk to Image
            speak('Please Upload image')
            root = Tk()
            root.filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Image files", "*.jpg"), ("all files", "*.*")))
            root.destroy()
            print("Selected file: ", root.filename)
            image_path = (root.filename)
            while True:
                user_input = user()
                print(user_input)
                if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all",]):
                    speak('Closing Image')
                    break
                else:
                    response = chat_with_image_gemini(user_input, image_path)
                    speak(response)



        # If user want to talk to click an image and then talk to it
        elif any(keyword.strip() in user_input.lower() for keyword in ['take a snapshot', 'take a photo', 'take snapshot', 'take snap shot','take screen shot', 'take a screenshot' ]): # Talk to Image
            img_save_path = './images/snapshot.png'
            speak('Please capture image')
            capture_image()
            while True:
                user_input = user()
                print(user_input)
                if any(keyword.strip() in user_input.lower() for keyword in ["okay, that's all","Okay that's all", "Okay, that's all",]):
                    speak('Closing Image')
                    break
                else:
                    response = chat_with_image_gemini(user_input, img_save_path)
                    speak(response)
            os.remove(img_save_path)
        
        
        
        # If user wants to generate code
        elif any(keyword.strip() in user_input.lower() for keyword in ['generate code']): # Generate Code
            speak("Please tell me what you want me to code")
            user_input = user()
            filename = None
            for extension in lang_extensions:
                if any(keyword.strip() in user_input.lower() for keyword in [extension]):
                    filename = f"generated_{extension}_code" + lang_extensions[extension]
                    
            result = write_code(user_input)
            with open(filename, 'w') as f:
                f.write(result)
                
            speak(f"Code Generated in {filename}")
        
        
        
        # If the user want to fix code
        elif any(keyword.strip() in user_input.lower() for keyword in ['modify program']): # Fix Code
            speak("Please upload the file you want me to fix")
            if code_fix():
                speak(f"Code Fixed and uploaded ")
            else:
                speak(f"Code Could not be Fixed and uploaded ")
        
        
        
        # If the user wants to search the internet
        elif any(keyword.strip() in user_input.lower() for keyword in ['search the internet']): # Search the internet
            speak("Speak your search query: ")
            user_input = user()
            result = search_internet(user_input)
            print("Search Result: ")
            print(result) 
            speak(result)
            print("Done...")
        
        
        
        # If user want to add an event to google calendar
        elif any(keyword.strip() in user_input.lower() for keyword in ['add event']): # Add Event
            print("What do you want to add: ")
            user_input = user()
            response = chat_with_groq_llama("Generate ONLY a JSON object to this user query:" + user_input + """ The JSON output should look like this: 
            {
            "summary": "",
            "location": "",
            "description": "",
            "colorId": "6",
            "start": {
                "dateTime": "2024-04-27T00:00:00+00:00",
                "timeZone": "Asia/Karachi"
            },
            "end": {
                "dateTime": "2024-05-01T00:00:00+00:00",
                "timeZone": "Asia/Karachi"
            },
            "recurrence": [
                
            ],
            "attendees": [
                {"email": "03318325446sm@gmail.com"}
            ] }
            DONT MISS ANY BRACKETS. Write summary, location, description, and dateTimes from user query. timeZone is Asia/Karachi fixed. Dont change attendees, recurrence, colorId. Dont even write 'Here is the JSON object','Here is the JSON object based on the user query:' or anything else. ONLY JSON RESPONSE IS REQUIRED. 
                        """)
            print(response)
            json_response = json.loads(response)
            GoogleCalendar().add_event(json_response)
            speak("Event added to google calendar")
        
        
        
        # If user want to get events from google calendar
        elif any(keyword.strip() in user_input.lower() for keyword in ['get my events']): # Add Event
            events = GoogleCalendar().get_events()
            response = chat_with_groq_llama("In a report form, tell me which events do i have and when.  Dont output special characters. use the following events data: " + str(events))
            speak(response)
        
        
        
        # If user just want to chat normally
        else:
            response = chat_with_groq_llama(user_input)
            print('Model Speaking...')
            speak(response)
        user_input = None


if __name__ == '__main__':
    main()