from __future__ import print_function
import datetime
import pickle
import os.path
import dateutil.parser
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events(token_file):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        # Save the credentials for the next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    tomorrow = (datetime.datetime.utcnow().replace(hour=0, minute=0, second=0) + timedelta(days=2)).isoformat() + 'Z' # 'Z' indicates UTC time
    #print(tomorrow)
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        parsedDate = dateutil.parser.parse(start)
        time = parsedDate.strftime('%m-%d %H:%M')
        print(time, event['summary'])
    return events

def map_event(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    parsedDate = dateutil.parser.parse(start)
    print({ 'start': start, 'summary': event['summary'] })
    return { 'start': start, 'summary': event['summary'] }

if __name__ == '__main__':
    events_1 = get_events('token_1.pickle')
    events_2 = get_events('token_2.pickle')

    mapped_list = map(map_event, events_2)
    print(len(list(mapped_list)))
    print(list(mapped_list))
    print(mapped_list)
    for item in mapped_list:
        print("=========")
        print(item)

