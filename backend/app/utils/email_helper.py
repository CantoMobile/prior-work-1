# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from google.auth import exceptions
# from google.auth.transport.requests import Request
# from google.oauth2 import service_account

# def send_otp_email(email, otp):
#     # Configura la información del correo electrónico
#     sender_email = 'yesidtrash15@gmail.com'  # Tu dirección de correo electrónico
#     subject = 'Código de verificación de cambio de propietario'
#     message = f'Tu código de verificación es: {otp}'

#     # Crea el objeto MIMEText para el contenido del correo electrónico
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(message, 'plain'))

#     try:
#         # Carga las credenciales del archivo JSON descargado desde la Consola de Desarrolladores de Google
#         credentials = service_account.Credentials.from_service_account_file(
#             'D:\\MISCOSAS\\PROYECTOS\\prior-work-1\\backend\\key.json',
#             scopes=['https://mail.google.com/']
#         )

#         # Refresca las credenciales si es necesario
#         if credentials.expired and credentials.refresh_token:
#             credentials.refresh(Request())

#         # Establece la conexión SMTP con el servidor de Gmail utilizando OAuth
#         with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             server.ehlo()
#             server.starttls()
#             server.login('', credentials)

#             # Envía el correo electrónico
#             server.sendmail(sender_email, email, msg.as_string())

#         return True
#     except exceptions.GoogleAuthError as e:
#         print(str(e))
#         return False

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from random import randint

def send_otp_email(email, otp):
    sender_email = 'correos@coally.com'  
    subject = 'Código de verificación de cambio de propietario'
    message = f'Tu código de verificación es: {otp}'

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
            print(f"Error al enviar el correo electrónico. Código de estado: {response.status_code}")
            return False
    except Exception as e:
        print(str(e))
        return False

