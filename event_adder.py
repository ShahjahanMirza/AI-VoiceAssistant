import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_events():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
      
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        now = dt.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time

        event_result = service.events().list(calendarId='primary', timeMin=now, maxResults=3, singleEvents=True, orderBy='startTime').execute() 
        
        events = event_result.get('items', [])
        
        out = ''
        if not events:
            print('No upcoming events found.')
            return
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            out += (start + ' - Summary:' + event['summary'] + '\n')
        
    except HttpError as error:
        print(f'An error occurred: {error}')
    
    return out   

def add_event(event):
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
      
    try:
        service = build('calendar', 'v3', credentials=creds)

        event = {
            "summary": "Google I/O 2015",
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
                {"email": "shahjahanmirza007@gmail.com"}
            ]
        } # OR just pass the event parameter

        event = service.events().insert(calendarId='primary', body=event).execute()
        
        print("Event Created: %s" % (event.get('htmlLink')))
        
    except HttpError as error:
        print(f'An error occurred: {error}')
   
    
