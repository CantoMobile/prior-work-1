import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_otp_email(email, otp):
    sender_email = 'correos@coally.com'  
    subject = 'Cantonica verification code'
    message = f'Your verification code is:{otp}'

    mail = Mail(
        from_email=sender_email,
        to_emails=email,
        subject=subject,
        plain_text_content=message
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(mail)
        if response.status_code == 202:
            print("Email sent successfully")
            return True
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(str(e))
        return False

