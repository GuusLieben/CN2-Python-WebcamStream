import socket
import numpy as np
import cv2 as opencv

addr = ("127.0.0.1", 65534)
buf = 512
width = 640
height = 480
code = 'start'
code = ('start' + (buf - len(code)) * 'a').encode('utf-8')
run = True
frame = 0
camera = opencv.VideoCapture(0, opencv.CAP_DSHOW)
camera.set(3, width)
camera.set(4, height)

path = r'C:\Users\Guus Lieben\Pictures\dab_stream.png'
image = opencv.imread(path)
font = opencv.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 1
color = (255, 0, 0)
thickness = 2
image = opencv.putText(image, 'Stream paused', org, font,
                       fontScale, color, thickness, opencv.LINE_AA)


def mouse_event(event, x, y, flags, param):
    global run
    if event == opencv.EVENT_LBUTTONDOWN:
        run = not run


if __name__ == '__main__':
    window_name = 'Streamer'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    opencv.namedWindow(window_name)
    opencv.setMouseCallback(window_name, mouse_event)
    lastvisual = []
    while camera.isOpened():
        visual = None
        if run:
            ret, frame = camera.read()
            if ret:
                opencv.imshow(window_name, frame)
                visual = frame
                lastvisual = visual
                if opencv.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        else:
            opencv.waitKey(1)
            opencv.imshow(window_name, image)
            visual = image
            lastvisual = visual

        match = lastvisual == visual
        if match.all():
            s.sendto(code, addr)
            data = visual.tostring()
            for i in range(0, len(data), buf):
                s.sendto(data[i:i + buf], addr)

    s.close()
    camera.release()
    opencv.destroyAllWindows()
