from __future__ import division

import subprocess as sp

import cv2

# Paused stream image
path = r'C:\Users\Guus Lieben\Pictures\dab_stream.png'
image = cv2.imread(path)  # Use the predefined image as paused image
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 0.75
color = (0, 0, 255)
thickness = 2
pause_img = cv2.putText(image, 'Stream paused', org, font,
                        fontScale, color, thickness, cv2.LINE_AA)

webcam_name = 'Logitech HD Webcam C525'

# FFMPEG command
ffmpeg = 'ffmpeg'
source = 'video={}'.format(webcam_name)
temp_folder = 'D:\CN2PyStream\\temp'


def run_ffmpeg():
    command = [
        ffmpeg,
        "-f", "dshow",
        "-video_size", "640_360",
        "-i", source,
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "zerolatency",
        "-f", "flv",  # output format
        "rtmp://localhost/live/stream_id",
        "-y",
        "-r", "1",
        "-pix_fmt", "bgr24",
        "-vcodec", "rawvideo",
        "-an",
        "-f", "yuv4mpegpipe",
        temp_folder
    ]
    return sp.Popen(command, stdout=sp.PIPE, bufsize=10)


def run_cv(ffmpeg_process):
    cap = cv2.VideoCapture(temp_folder)

    while True:
        if cap.isOpened():
            _, frame = cap.read()
            cv2.imshow('Preview', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


def run():
    ffmpeg_process = run_ffmpeg()
    run_cv(ffmpeg_process)


if __name__ == "__main__":
    run()
