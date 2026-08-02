import urllib.request
import json
import os
from django.core.mail.backends.base import BaseEmailBackend

class ResendEmailBackend(BaseEmailBackend):
    """
    HTTP-based transactional email backend for Resend API.
    Bypasses cloud provider outbound SMTP socket port blocks (25/465/587) entirely.
    """
    def send_messages(self, email_messages):
        api_key = os.environ.get('RESEND_API_KEY', '').strip()
        if not api_key:
            print("ResendEmailBackend: RESEND_API_KEY missing from environment.")
            return 0
        
        num_sent = 0
        for message in email_messages:
            try:
                url = "https://api.resend.com/emails"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                
                html_body = None
                for content, mime_type in getattr(message, 'alternatives', []):
                    if mime_type == 'text/html':
                        html_body = content
                        break
                
                from_email = os.environ.get('DEFAULT_FROM_EMAIL', '').strip() or 'Rentora Concierge <onboarding@resend.dev>'
                
                payload = {
                    "from": from_email,
                    "to": list(message.to),
                    "subject": message.subject,
                    "html": html_body or message.body,
                    "text": message.body
                }
                
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status in (200, 201):
                        num_sent += 1
                        print(f"Resend HTTP API sent email to {message.to} successfully.")
            except Exception as e:
                print(f"Resend HTTP API dispatch error: {type(e).__name__} - {e}")
        return num_sent
