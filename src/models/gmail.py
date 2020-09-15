import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from src.models import loader 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
class Gmail:
    @staticmethod
    def get_gmail_creds():
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('src/secrets/token.pickle'):
            with open('src/secrets/token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.abspath(os.environ.get('GMAIL_CREDENTIALS')), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('src/secrets/token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds