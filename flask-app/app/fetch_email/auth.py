from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import time
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def authenticate():

    store = file.Storage('token.json')
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service

authenticate()