#!/usr/bin/env python

from __future__ import division
import cv2
import numpy as np
import socket
import struct
import math

MAX_DGRAM = 2 ** 16


class FrameSegment(object):
    """
    Object to break down image frame segment
    if the size of image exceed maximum datagram size
    """
    MAX_DGRAM = 2 ** 16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64  # extract 64 bytes in case UDP frame overflown

    def __init__(self, sock, port, addr="127.0.0.1"):
        self.s = sock
        self.port = port
        self.addr = addr

    def udp_frame(self, img):
        """
        Compress image and Break down
        into data segments
        """
        compress_img = cv2.imencode('.jpg', img)[1]
        dat = compress_img.tostring()
        size = len(dat)
        count = math.ceil(size / self.MAX_IMAGE_DGRAM)
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack("B", count) +
                          dat[array_pos_start:array_pos_end],
                          (self.addr, self.port)
                          )
            array_pos_start = array_pos_end
            count -= 1


def dump_buffer(s):
    """ Emptying buffer frame """
    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        print(seg[0])
        if struct.unpack("B", seg[0:1])[0] == 1:
            print("finish emptying buffer")
            break


def main():
    """ Getting image udp frame &
    concat before decode and output image """

    # Set up receiving socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 12345))
    dat = b''
    dump_buffer(s)

    # Set up restream socket
    rs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 22345

    fs = FrameSegment(rs, port)

    while True:
        seg, addr = s.recvfrom(MAX_DGRAM)
        if struct.unpack("B", seg[0:1])[0] > 1:
            dat += seg[1:]
        else:
            dat += seg[1:]
            img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
            cv2.imshow('server', img)
            fs.udp_frame(img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            dat = b''

    cv2.destroyAllWindows()
    s.close()


if __name__ == "__main__":
    main()
