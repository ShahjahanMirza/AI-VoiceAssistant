import os.path
import datetime as dt
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleCalendar:
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self):
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json')
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_events(self):
        try:
            now = dt.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
            event_result = self.service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute() 
            events = event_result.get('items', [])
            out = ''
            if not events:
                print('No upcoming events found.')
                return
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                out += (start + ' - Summary:' + event['summary'] + '\n')
            return out
        except HttpError as error:
            print(f'An error occurred: {error}')
        os.remove('token.json')

    def add_event(self, event):
        print("add_event function called")
        try:
            print("in try block of add_event function")
            # Ensure end time is provided
            if 'end' not in event:
                raise ValueError("End time is missing in the event parameters.")
            print("End time is present")
            # Insert the event
            print("Inserting the event", event)
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print("Event Created: %s" % (event.get('htmlLink')))
        
        except ValueError as error:
            print(f'Error adding event: {error}')
        os.remove('token.json')

# Example usage:
calendar = GoogleCalendar()
# events = calendar.get_events()
# print(events)
response = {
"summary": "Business Meeting",
"location": "England",
"description": "Business Meeting",
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
]} 

# calendar.add_event(response)
# print(calendar.get_events())
