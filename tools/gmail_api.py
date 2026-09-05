import os
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from schemas.email import EmailInput

# Quyen truy cap: Doc, Gui, Xoa va Quan ly thu
SCOPES = ['https://mail.google.com/']

def get_gmail_service():
    """Lay credentials va khoi tao Gmail API service."""
    creds = None
    token_path = os.getenv("GMAIL_TOKEN_PATH", "token.json")
    creds_path = os.getenv("GMAIL_CREDENTIALS_PATH", "credentials.json")
    
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(f"Khong tim thay file {creds_path}. Vui long lam theo huong dan de lay file nay.")
                
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f"Loi khi khoi tao Gmail Service: {error}")
        return None

def fetch_unread_emails(max_results=5) -> list[EmailInput]:
    """Lay danh sach cac email chua doc tu hop thu den."""
    service = get_gmail_service()
    if not service:
        return []

    emails = []
    try:
        results = service.users().messages().list(
            userId='me', 
            labelIds=['INBOX', 'UNREAD'], 
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        for msg in messages:
            msg_id = msg['id']
            msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            
            headers = msg_data.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "No Subject")
            sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Unknown Sender")
            date = next((h['value'] for h in headers if h['name'].lower() == 'date'), "")
            
            body = "Noi dung khong the doc"
            payload = msg_data.get('payload', {})
            
            def get_body_recursive(payload_part):
                if payload_part.get('mimeType') == 'text/plain':
                    data = payload_part.get('body', {}).get('data')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
                elif 'parts' in payload_part:
                    for part in payload_part['parts']:
                        result = get_body_recursive(part)
                        if result: return result
                return None
                
            parsed_body = get_body_recursive(payload)
            if parsed_body:
                body = parsed_body

            emails.append(EmailInput(
                id=msg_id,
                sender=sender,
                subject=subject,
                body=body[:1000],
                date=date
            ))
            
    except HttpError as error:
        print(f"Loi khi doc email: {error}")
        
    return emails

def create_draft_reply(email_id: str, sender: str, subject: str, draft_body: str):
    """Tao mot ban nhap tra loi (Draft) trong Gmail."""
    service = get_gmail_service()
    if not service:
        return
        
    try:
        message = EmailMessage()
        message.set_content(draft_body)
        
        import re
        match = re.search(r'<(.+?)>', sender)
        to_email = match.group(1) if match else sender
        
        message['To'] = to_email
        message['Subject'] = subject if subject.startswith("Re:") else f"Re: {subject}"
        
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        create_draft_request_body = {
            'message': {
                'raw': encoded_message,
                'threadId': email_id
            }
        }
        
        draft = service.users().drafts().create(userId='me', body=create_draft_request_body).execute()
        print(f"Da tao thanh cong thu nhap tren Gmail (Draft ID: {draft['id']})")
        return draft
        
    except HttpError as error:
        print(f"Loi khi tao draft: {error}")
