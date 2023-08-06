import datetime as dt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendar:
    def __init__(self, credentials, secrets_file):
        self.secrets_file = secrets_file
        self.creds = credentials

    def get_credentials(self):
        # This method retrieves the credentials if they could not be provided
        # at instanciation time.

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file, SCOPES)
                self.creds = flow.run_local_server(port=0)

        return self.creds

    def get_events(self, cal_id, time_min, time_max, full_days_splitted=False):
        # This method retrieves the events in the calendar identified by
        # cal_id, that were scheduled between "time_min" and "time_max"

        self.get_credentials()
        service = build('calendar', 'v3', credentials=self.creds)

        page_token = None
        result = []
        
        while True:
            events_result = service.events().list(calendarId=cal_id, timeMin=time_min,
                                                  timeMax=time_max, singleEvents=True, pageToken=page_token).execute()
            events = events_result.get('items', [])
            result.extend(events)

            page_token = events_result.get('nextPageToken')
            if not page_token:
                return result

    def get_full_days_splitted_events(self, cal_id, time_min, time_max)
        max_date = dt.datetime.strptime(time_max[:-6], '%Y-%m-%dT%H:%M:%S')
        events = self.get_events(cal_id, time_min, time_max)
        result = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            if len(start) > 10:
                stdt = dt.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
                endt = dt.datetime.strptime(end[:-6], '%Y-%m-%dT%H:%M:%S')
            else:
                stdt = dt.datetime.strptime(start, '%Y-%m-%d')
                endt = dt.datetime.strptime(end, '%Y-%m-%d')

            delta = (endt - stdt)
            for i in range(delta.days):
                day_date = stdt + dt.timedelta(days=i)

                if day_date <= max_date:
                    result.append((day_date, event['summary']))
                else:
                    break

        return result