from datetime import datetime
from itertools import count
import traceback
from typing import List
import uuid
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64

from bs4 import BeautifulSoup

import datetime

# from mysqldb import SqlConection




listOfMails=[]
def createFilter(service, userId, o):
    """Creates the filter with the criteria specified"""
    try:
        r = service.users().settings().filters().create(
            userId=userId, body=o).execute()
        return r
    except:
        print("Filter was already created")
        pass


def getMatchingThreads(service, userId, labelIds, query):
    """Get all threads from gmail that match the query"""
    response = service.users().threads().list(userId=userId, labelIds=labelIds,
                                              q=query).execute()
    threads = []
    if 'threads' in response:
        threads.extend(response['threads'])
        # Do the response while there is a next page to receive.
    while 'nextPageToken' in response:
        pageToken = response['nextPageToken']
        response = service.users().threads().list(
            userId=userId,
            labelIds=labelIds,
            q=query,
            pageToken=pageToken).execute()
        threads.extend(response['threads'])
    return threads
def buildSearchQuery(criteria):
    """Input is the criteria in a filter object. Iterate over it and return a
    gmail query string that can be used for thread search"""
    queryList = []
    positiveStringKeys = ["from", "to", "subject"]
    for k in positiveStringKeys:
        v = criteria.get(k)
    if v is not None:
        queryList.append("("+k+":"+v+")")
    v = criteria.get("query")
    if v is not None:
        queryList.append("("+v+")")
    # TODO: This can be extended to include other queries. Negated queries,
    # non-string queries
    return " AND ".join(queryList)

def applyFilterToMatchingThreads(service, userId, filterObject):
    """After creating the filter we want to apply it to all matching threads
    This function searches all threads with the criteria and appends the same
    label of the filter"""

    query = buildSearchQuery(filterObject["criteria"])
    threads = getMatchingThreads(service, userId, [], query)
    addLabels = filterObject["action"]["addLabelIds"]
    print("Adding labels {} to {} threads".format(addLabels, len(threads)))

    for t in threads:
        body = {
            "addLabelIds": addLabels,
            "removeLabelIds": []
        }

        result = service.users().threads().modify(userId=userId, id=t["id"],
                                         body=body).execute()
        messages = result.get('messages')
        for msg in messages:
            # Get the message from its id
            txt = service.users().messages().get(
                userId='me', id=msg['id']).execute()
            try:
                # Get value of 'payload' from dictionary 'txt'
                payload = txt['payload']
                headers = payload['headers']

                # Look for Subject and Sender Email in the headers
                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'To':
                        sender = d['value']
                    if d['name'] == 'Date':
                        sendDate = d['value']


                
                if(sender!='failedmailsmeli@gmail.com'):
                    newMail = Mail(sendDate, sender, subject,msg['id'])
                    listOfMails.append(newMail)
            except Exception as e:
                print("Error detected: ", e)
                pass


# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.modify',
            'https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.readonly']







def fetchMails() -> List:
    creds = None
    # The file token.pickle contains the user access token.
    if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Gmail Api connection
    try:
        service = build('gmail', 'v1', credentials=creds)
        desiredFilters = [
            {
                "criteria": {
                    "subject": "[Failure]",
                },
                "action": {
                    "addLabelIds": [["INBOX"]],
                }
            },
            {
                "criteria": {
                    "subject": "[Undeliverable]",
                },
                "action": {
                    "addLabelIds": [["INBOX"]],
                }
            },
            {
                "criteria": {
                    "subject": "[Delivery Service Notification]",
                },
                "action": {
                    "addLabelIds": [["INBOX"]],
                }
            },
        ]
        for df in desiredFilters:
            createFilter(service, "me", df)
            applyFilterToMatchingThreads(service, "me", df)

        return listOfMails
    except Exception as error:
        print(F'An error occurred: {error}')



class Mail:
    id: str
    receptionDate: datetime
    to: str
    subject: str
    body: str
    gmailId:str

    def __init__(self,receptionDate,to,subject,gmailId):
        self.receptionDate = receptionDate
        self.to = to
        self.subject = subject
        self.id = str(uuid.uuid4())
        self.gmailId = gmailId
        self.body = ""



