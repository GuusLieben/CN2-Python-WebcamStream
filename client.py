from __future__ import division
import subprocess as sp
import cv2
import numpy

path = r'C:\Users\Guus Lieben\Pictures\dab_stream.png'
paused_image = cv2.imread(path)
font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)
fontScale = 0.75
color = (0, 0, 255)
thickness = 2
pause_img = cv2.putText(paused_image, 'Stream paused', org, font,
                        fontScale, color, thickness, cv2.LINE_AA)

webcam_name = 'Logitech HD Webcam C525'

# FFMPEG command
ffmpeg = 'ffmpeg'
source = 'video={}'.format(webcam_name)
stream_id = str(hash(sp))[0:5]

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
        "rtmp://localhost/live/{}".format(stream_id),
        "-y",
        "-r", "24",
        "-pix_fmt", "bgr24",
        "-vcodec", "rawvideo",
        "-an",
        "-f", "image2pipe",
        "-"
    ]
    return sp.Popen(command, stdout=sp.PIPE, bufsize=10)


def run():
    pipe = run_ffmpeg()
    paused = False
    while True:
        if not paused:
            raw_frame = pipe.stdout.read(640 * 360 * 3)
            frame = numpy.frombuffer(raw_frame, dtype='uint8')
            frame = frame.reshape((360, 640, 3))
            cv2.putText(frame, 'ID {}'.format(stream_id), org, font,
                        fontScale, color, thickness, cv2.LINE_AA)
            if frame is not None:
                cv2.imshow('Preview', frame)
        elif paused:
            cv2.imshow('Preview', pause_img)

        key = cv2.waitKey(1)
        if key == 27:  # Esc
            break
        elif key == 32:  # Space
            paused = not paused

        if paused and pipe is not None:
            pipe.kill()
            pipe = None
        elif not paused and pipe is None:
            pipe = run_ffmpeg()

    cv2.destroyAllWindows()
    if pipe is not None:
        pipe.kill()


if __name__ == "__main__":
    run()
