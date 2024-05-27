import base64
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Set up the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
creds = None
token_path = 'token.json'
if os.path.exists(token_path):
creds = Credentials.from_authorized_user_file(token_path)
if not creds or not creds.valid:
if creds and creds.expired and creds.refresh_token:
creds.refresh(Request())
else:
flow = InstalledAppFlow.from_client_secrets_file(
'credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
with open(token_path, 'w') as token:
token.write(creds.to_json())
service = build('gmail', 'v1', credentials=creds)
def create_message(sender, to, subject, message_text):
message = MIMEMultipart()
message['to'] = to
message['from'] = sender
message['subject'] = subject
msg = MIMEText(message_text)
message.attach(msg)
raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
return {'raw': raw_message}
def send_message(service, sender, to, subject, body):
try:
message = create_message(sender, to, subject, body)
sent_message = service.users().messages().send(userId=sender, body=message).execute()
print('Message Id: {}'.format(sent_message['id']))
return sent_message
except HttpError as error:
print('An error occurred: {}'.format(error))
# Replace with your information
sender_email = ‘faheem@gmail.com’
recipient_email = ‘abc@gmail.com’
email_subject = 'Test Email'
email_body = 'This is a test email sent using the Gmail API with OAuth.'
# Send the email
send_message(service, sender_email, recipient_email, email_subject, email_body)