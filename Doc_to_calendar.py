from __future__ import print_function
import re
import person_list as pl
import datetime
import pickle
import os.path
import create_assignments as ca
import person_list as pl
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
### date_object
class event:
	def __init__(self, date_of, name):
		self.date_of = date_of
		self.name = name
		self.email = [i for i in [i.email if i.name == name else None for i in pl.person_list] if i is not None][0]
		self.color = pl.color_dict[name]


### Open File
file = open('OFFICIAL_RA_SCHEDULE.txt', 'r')
file_lines = file.readlines()

### Parse for events
file_lines_parsed = []
date = re.compile('....-..-..')
dash = re.compile('--------------')
for i in file_lines:
	if date.match(i[:10]) is not None and dash.match(i) is None:
		file_lines_parsed.append(i[:-1])
	else:
		pass

### Create event object
event_list = []
for i in file_lines_parsed:
	temp = [i[:10], i[11:]]
	temp[1] = temp[1].split(',')
	temp[1][1] = temp[1][1][1:]
	event_list.append(event(temp[0], temp[1][0]))
	event_list.append(event(temp[0], temp[1][1]))

### Clear calendar
def main(event_list):
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
        
        name = i.name
        day = i.date_of
        email = i.email
        color = i.color

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
        'colorId': color,
        'reminders': {
        'useDefault': True,
        },}

        event = service.events().insert(calendarId=cdid, body=event).execute()
        time.sleep(2)

#main(event_list)
### Load events into calendar
##         'attendees': [
 ##       {'email': email},
 ##       ],