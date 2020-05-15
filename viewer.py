import os
import tempfile
import atexit
import subprocess
import cv2


def run_cv_window():
    vcap = cv2.VideoCapture("rtmp://localhost/live/darwin")

    while True:
        ret, frame = vcap.read()
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    run_cv_window()
