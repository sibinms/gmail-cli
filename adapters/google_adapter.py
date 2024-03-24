import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from schema.utils import get_or_create_email

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify'
]


def authenticate():
    """
    Function to authenticate with google using Oauth2
    and returns the credentials after writing it into pickle file

    Args:
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_service(service_type, version, credentials):
    if service_type == 'gmail':
        service = build('gmail', version, credentials=credentials)
        return service

    raise AssertionError(f"Service type {service_type} not implemented")


def fetch_emails(service):
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])
    return messages


def get_user_email(service):
    profile = service.users().getProfile(userId='me').execute()
    return profile['emailAddress']


def import_emails(messages, service):
    user_id = get_user_email(service)

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        message_id = msg['id']
        sender = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'From')
        subject = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject')
        date = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date')
        body = msg['snippet']
        email, created = get_or_create_email(
            user_id=user_id,
            message_id=message_id,
            sender=sender,
            subject=subject,
            body=body,
            date=date
        )
        if created:
            print(f"Created - {message_id} - {subject} - {sender} for user - {user_id}")
        else:
            print(f" Message -{message_id} - {subject} - {sender} already exists for user - {user_id}")


def mark_as_read(service, message_id):
    """
    Marks the specified email message as read.

    Args:
        service: The authenticated Gmail service object.
        message_id (str): The ID of the email message to mark as read.
    """
    body = {"removeLabelIds": ["UNREAD"]}
    try:
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        print(f"Email message with ID '{message_id}' marked as read.")
    except Exception as e:
        print(f"Failed to mark email message with ID '{message_id}' as read: {e}")


def mark_as_unread(service, message_id):
    """
    Marks the specified email message as unread.

    Args:
        service: The authenticated Gmail service object.
        message_id (str): The ID of the email message to mark as unread.
    """
    body = {"addLabelIds": ["UNREAD"]}
    try:
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        print(f"Email message with ID '{message_id}' marked as unread.")
    except Exception as e:
        print(f"Failed to mark email message with ID '{message_id}' as unread: {e}")


def move_to_inbox(service, message_id):
    """
    Moves the specified email message to the Inbox.

    Args:
        service: The authenticated Gmail service object.
        message_id (str): The ID of the email message to move to the Inbox.
    """
    body = {"addLabelIds": ["INBOX"], "removeLabelIds": []}
    try:
        service.users().messages().modify(userId='me', id=message_id, body=body).execute()
        print(f"Email message with ID '{message_id}' moved to Inbox.")
    except Exception as e:
        print(f"Failed to move email message with ID '{message_id}' to Inbox: {e}")
