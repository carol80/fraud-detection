from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from fetch_email import fetch_messages,cloud,config
import time
import json
import datetime
from fetch_email import config


SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def check_new_mail(service, old_id):

    messages = []

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()

    if 'messages' in results:
      messages.extend(results['messages'])

    new_id = messages[0]['id']
    
    if new_id != old_id:
        #fetch new messages
        message_list, new_id = get_messages_list(service)
        get_messages(service, message_list, new_id)

    else:
        print('Waiting for 30s')
        time.sleep(30)
        check_new_mail(service, old_id)
    
def authenticate():

    store = file.Storage('token.json')
    creds = store.get()
    
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    return service
    
def get_messages_list(service):  #Fetch 'counter' number of messages

    messages = []
    count = 0

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
  
    if 'messages' in results:
      messages.extend(results['messages'])

    while 'nextPageToken' in results:
      page_token = results['nextPageToken']
      results = service.users().messages().list(userId='me', labelIds = ['INBOX'], pageToken=page_token).execute()
      messages.extend(results['messages'])
      count += 1
      if count == 1:
        break
    
    print(messages[0]['id'])   # messages[0] denotes first email, messages[0][0] denotes id of first email
    return messages, messages[0]['id']

def get_messages(service, messages, old_id):

    counter = 0

    if not messages:
        print ("No messages found.")
    else:
        
        print ("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            
            date_time = datetime.datetime.fromtimestamp(int(msg['internalDate'])/1000.0).strftime('%Y-%m-%d %H:%M:%S')
            
            header = msg['payload']['headers']
            
            for obj in header:
                if obj['name'] == 'From':
                    from_addr = obj['value']
                elif obj['name'] == 'To':
                    to_adr = obj['value']
                elif obj['name'] == 'Subject':
                    subj = obj['value']

            json_format = {
                "time":date_time,
                "from":from_addr,
                "to":to_adr,
                "subject":subj,
                "body": msg['snippet']
                }

            print(json_format)
            config.emails.document().set(json_format)

            if counter == 1:
                break
            counter += 1

            cloud.cloud(from_addr)
            print(from_addr)
    check_new_mail(service, old_id)

def exec_code():
    service = authenticate()