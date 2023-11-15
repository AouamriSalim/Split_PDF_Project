import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd


def send_email(smtp_server, smtp_port, username, password, sender, recipient, attachments):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Bulletin'

    msg.attach(MIMEText('', 'plain'))

    for attachment, original_name in attachments:
        with open(attachment, 'rb') as file:
            part = MIMEApplication(file.read(), Name=original_name)
        part['Content-Disposition'] = f'attachment; filename="{original_name}.pdf"'
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)  # Use TLS (Transport Layer Security) if available
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        print(f"Email sent to {recipient} successfully. Included {original_name}")
    except Exception as e:
        print(f"Email could not be sent. Error: {str(e)} {original_name}")

def send_emails_from_excel(excel_file, smtp_server, smtp_port, username, password, sender):
    df = pd.read_excel(excel_file)

    for index, row in df.iterrows():
        pdf_path = row['PDF Name']
        recipient_email = row['Email Address']
        #pdf_attachment = f'{pdf_path}.pdf'
        attachment_path = f'E:/output/{pdf_path}.pdf'  # Replace 'path_to_your_pdfs/' with your PDFs directory

        # Attach the PDF document to the email and pass the original file name as well
        attachments = [(attachment_path, pdf_path)]

        # Call the send_email function for each recipient
        send_email(smtp_server, smtp_port, username, password, sender, recipient_email, attachments)

# Example usage:
smtp_server = 'yourSMTP_server'
smtp_port = 465  # Modify the port as needed
username = 'yourmail_username'
password = 'yourmailpassword'
sender = 'yourmail'
excel_file = r'E:\output\split_emails.xlsx'  # Replace with your Excel file
# Call the send_emails_from_excel function to send emails to recipients from the Excel list
send_emails_from_excel(excel_file, smtp_server, smtp_port, username, password, sender)
