from __future__ import print_function
import pickle
import os
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def get_credentials(scopes, credentials_file="credentials.json", pickle_file="token.pickle"):
    """Get credentials for access"""
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
                'credentials.json', scopes)
            #creds = flow.run_local_server(port=0)
            creds = flow.run_local_server(port=3000)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def overwrite_sheet(creds, values=[], **kwargs):
    """
    WIP: script to overwrite sheet range into.
    """
    #  pylint: disable=no-member

    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': values,
    }
    service.spreadsheets().values().update(
        body=body,
        **kwargs,
    ).execute()


def append_sheet(creds, spreadsheet_id, range_name, appending_values):
    """
    WIP: script to overwrite sheet range into.
    """
    #  pylint: disable=no-member

    #################### read current values

    service = build('sheets', 'v4', credentials=creds)
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name,
    ).execute()

    if not result:
        print('No data found.')
    else:
        for row in result['values']:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)

    #################### write new values

    values = result['values']
    values.append(*appending_values)
    body = {
        'values': values,
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
