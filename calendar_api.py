from __future__ import print_function
import datetime
import pickle
import os.path
import create_assignments as ca
import person_list as pl
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    one = ca.get_days(pl.person_list, '2020-08-28', '2020-11-21', 1000)
    ca.results(one)
    event_list = ca.convert_to_events(one)
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API - Create Calendar
    calendar = {
    'summary': ('RA Calendar (Created - ' + datetime.date.today().isoformat() + ')'),
    'timeZone': 'America/New_York'}

    created_calendar = service.calendars().insert(body=calendar).execute()

    cdid = created_calendar['id']

    # Create events iteratively
    for i in event_list:
        
        name = i[1]
        day = i[0]
        email = i[2]
        color = i[3]

        event = {
        'summary': name + ' - Duty',
        'location': 'South Campus',
        'description': 'Duty shift for' + name + 'on' + day,
        'start': {
        'dateTime': day + 'T23:00:00+00:00',
        'timeZone': 'America/New_York',},
        'end': {
        'dateTime': day + 'T23:30:00+00:00',
        'timeZone': 'America/New_York',},
        'attendees': [
        #{'email': email},
        ],
        'colorId': color,
        'reminders': {
        'useDefault': True,
        },}

        event = service.events().insert(calendarId=cdid, body=event).execute()
        time.sleep(2)



if __name__ == '__main__':
    main()