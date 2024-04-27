import cv2
import time
import glob
import os
from datetime import datetime
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


# for video saving saving
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)
nowtime = datetime.now()
formatted_time = nowtime.strftime("%Y-%m-%d %H:%M:%S")
filename = f"{formatted_time}.mp4"
result = cv2.VideoWriter("recordings/video.mp4", cv2.VideoWriter_fourcc(*'MP4V'), 10, size)

def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            images_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]


    if status == 1:
        result.write(frame)

    if status_list[0] == 1 and status_list[1] == 0:
        result.release()
        email_thread = Thread(target=send_email, args=(images_with_object , "recordings/video.mp4" ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        email_thread.daemon = True

        email_thread.start()


    print(status_list)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()

if clean_thread is not None:
    clean_thread.start()


