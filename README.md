# Voice Assistant

This is a voice assistant application that can perform various tasks through voice commands.

> For example: Write code, talk to documents, talk to images, general chat, and many more...

It is built completely locally.
Used:
Llama3
Gemma
Qwen
Faster Whisper
Pyaudio
CrewAI - Later to be used
Groq

\*Frame-work used : LangChain

## Features

- _Speech Recognition_ - Uses PyAudio to record voice input and Whisper for transcription
- _Text to Speech_ - Uses gTTS to read back text
- _General Conversations_ - Uses Llama3 for general conversation
- _Information Storage_ - Can add spoken information to a knowledge document and have conversations based on it
- _Document Understanding_ - Analyzes uploaded documents to extract key information
- _Image Captioning_ - Describes images uploaded by the user
- _Code Generation_ - Creates simple Python code based on voice commands
- _Fixed Code Files_ - Fixes uploaded python files
- _Internet Search_ - Searches the web for queries and reads back results
- _Calendar Integration_ - Adds events to Google Calendar and retrieves upcoming events via API

## Overview

The main capabilities of the assistant include:

- Taking voice input from the user and transcribing it to text
- Adding information to a knowledge document that the assistant can then reference in future conversations
- Having a conversation with the user based on the knowledge document
- Allowing users to upload documents for the assistant to read and extract information from
- Generating code based on voice commands
- Adding events to a calendar

## Setup

To run this assistant yourself:

## Pre-requisites:

> - Should have `Ollama` installed with the models used.
> - Set up Google API here: `https://developers.google.com/calendar/api/quickstart/python` and download c`redentials.json`
> - Save `Groq` API key in `.env` from here: `https://console.groq.com/playground`

1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Run `python main.py`
4. Speak to give commands to the assistant
5. Press `Space` to end speech command

## Commands

Here are some example voice commands the assistant can handle:

- "Bye" "Exit" - Exits the Voice Assistant
- "Add information" - Adds spoken information to the knowledge document
- "Give information" - Triggers the assistant to converse based on the knowledge document
- "Upload document" - Uploads a document for the assistant to read and converse based on the uploaded document
- "Upload image" - Uploads an image for the assistant to read and converse based on the uploaded image
- "Generate code" - Generates working code based on voice commands and outputs it in a .py file
- "Modify program" - Fixes an uploaded .py file and rewrites with fixed working code
- "Add event" - Adds an event to the Google Calendar via API
- "Get my events" - Retrieves the upcoming events from Google Calendar via API

The assistant can also have general conversations based on the user's input.

## Customization

To customize the assistant's capabilities:

- Modify the `main()` function to add/remove handler logic
- Add/remove modules in `models.py`, `audios.py` etc to enable different features
- Expand the knowledge document and conversation model for more intelligent dialog
- so on...

## Improvements

There is a lot of room for building on top of this basic framework to create a more versatile voice assistant.

- General Memory can be introduced to store information that can be referenced in future conversations with every model
- A lot of repetition is there, that can be fixed
- Many models are being used, Local and API both, that can be improved
- Prompt Engineering for better responses
- Functionize things the main file
- Improve the UI
- Add function calling
- Prompt ( user text )
- Better Embeddings ( OpenAI )
- Gemini Vision
- Image capture for talking to image
- Multiple Document Chat
- Multiple Document type chat
- so on...
