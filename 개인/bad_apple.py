import cv2
import os
import time

# ASCII 문자 (밝기 순서)
ASCII_CHARS = " .:-=+*#%@"

def frame_to_ascii(frame, width=80):
    # 비율 유지하면서 리사이즈
    height, original_width = frame.shape
    aspect_ratio = height / original_width
    new_height = int(aspect_ratio * width * 0.55)

    resized = cv2.resize(frame, (width, new_height))

    ascii_frame = ""
    for row in resized:
        for pixel in row:
            ascii_frame += ASCII_CHARS[int(pixel) * len(ASCII_CHARS) // 256]
        ascii_frame += "\n"

    return ascii_frame


# 영상 파일 경로 (여기에 Bad Apple 영상 넣기)
video_path = "/home/sdh080200/bad_apple.mp4"

cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)


frame_delay = 1 / fps


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ascii_frame = frame_to_ascii(gray, width=60)

    print("\033[H\033[J", end="")  # 핵심!
    print(ascii_frame)

    time.sleep(0.03)

cap.release()

# import cv2
#
# video_path = "/home/sdh080200/bad_apple.mp4"
#
# cap = cv2.VideoCapture(video_path)
#
# print("열림 여부:", cap.isOpened())
#
# ret, frame = cap.read()
# print("프레임 읽힘:", ret)
#
# if ret:
#     print("프레임 shape:", frame.shape)