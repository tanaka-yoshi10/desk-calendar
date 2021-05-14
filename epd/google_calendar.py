from __future__ import print_function
import datetime
import pickle
import os.path
import dateutil.parser
import pytz
import yaml
from datetime import timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from itertools import groupby

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events(token_file, calendar_list):
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
    # calendar_list_result = service.calendarList().list().execute()
    # calendar_list = calendar_list_result.get('items', [])
    # for calendar in calendar_list:
    #     print(calendar['id'], calendar['summary'])
    events = []
    for calendar_id in calendar_list:
        events_result = service.events().list(calendarId=calendar_id, timeMin=now, #timeMax=tomorrow,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        local_events = events_result.get('items', [])
        events.extend(local_events)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        parsedDate = dateutil.parser.parse(start)
        time = parsedDate.strftime('%m-%d %H:%M')
    return events

def map_event(event):
    start = event['start'].get('dateTime', event['start'].get('date'))
    jp = pytz.timezone('Asia/Tokyo')
    parsedDate = dateutil.parser.parse(start).replace(tzinfo=jp)
    return { 'date': parsedDate.date(), 'datetime': parsedDate, 'start': start, 'summary': event['summary'], 'event': event }

def google_calendar():
    events = []

    with open('setting.yaml') as file:
        obj = yaml.safe_load(file)
        print(obj)

        for item in obj:
            events_local = get_events(item['file'], item['calendar_list'])
            events.extend(events_local)

    mapped_list = map(map_event, events)
    sorted_list = sorted(mapped_list, key=lambda e:e['datetime'])[:10]
    return groupby(sorted_list, key=lambda m: m['date'])

if __name__ == '__main__':
    list = google_calendar()
    for item in list:
        print(item['start'], item['summary'])
