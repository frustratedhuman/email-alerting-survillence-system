import smtplib
import imghdr
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage

PASSWORD = "nfzylrjojvcwzjnb"
SENDER = "sawantritesh007@gmail.com"
RECEIVER = "sawantritesh007@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Look out, Here something we caught!"
    email_message.set_content("Hey, we just saw some activity!")

    # Initializing video object
    video_file = MIMEBase('application', "octet-stream")

    # Importing video file
    video_file.set_payload(open('recordings/video.mp4', "rb").read())

    # Encoding video for attaching to the email
    encoders.encode_base64(video_file)

    with open(image_path, "rb") as file:
        content = file.read()
        email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))
    #email_message.add_attachment(video_file, filename='video.mp4')

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/19.png")


