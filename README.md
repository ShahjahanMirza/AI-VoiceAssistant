# Voice Assistant

This is a voice assistant application that can perform various tasks through voice commands.
It is built completely locally. 
Used:
Llama3
Gemma
Qwen
Faster Whisper
Pyaudio
CrewAI - Later to be used

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
> Should have Ollama installed with the models used.
1. Clone this repository
2. Install dependencies with `pip install -r requirements.txt`
3. Run `python main.py`
4. Speak to give commands to the assistant

## Commands

Here are some example voice commands the assistant can handle:

- "Add information" - Adds spoken information to the knowledge document 
- "Give information" - Triggers the assistant to converse based on the knowledge document
- "Upload document" - Uploads a document for the assistant to read
- "Write code" - Generates code based on voice commands
- "Add event" - Adds an event to the calendar

The assistant can also have general conversations based on the user's input.

## Customization

To customize the assistant's capabilities:

- Modify the `main()` function to add/remove handler logic
- Add/remove modules in `models.py`, `audios.py` etc to enable different features
- Expand the knowledge document and conversation model for more intelligent dialog

There is a lot of room for building on top of this basic framework to create a more versatile voice assistant.
