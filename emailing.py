import smtplib
import imghdr
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
import os

PASSWORD = "nfzylrjojvcwzjnb"
SENDER = "sawantritesh007@gmail.com"
RECEIVER = "sawantritesh007@gmail.com"

def send_email(image_path, video_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Look out, Here something we caught!"
    email_message.set_content("Hey, we just saw some activity!")

    # Attaching image
    with open(image_path, "rb") as file:
        content = file.read()
        email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))


    # Attaching video
    with open(video_path, "rb") as file:
        video_data = file.read()
        video_file = MIMEBase('application', "octet-stream")
        video_file.set_payload(video_data)
        encoders.encode_base64(video_file)
        video_file.add_header("Content-Disposition", f"attachment; filename={os.path.basename(video_path)}")
        email_message.add_attachment(video_file)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email(image_path="images/19.png", video_path="recordings/video.mp4")


