import time

import zmq
from paddleocr import PaddleOCR
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

if __name__ == '__main__':
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:12344")
    print("start success")
    while True:
        message = socket.recv()
        print(message.decode('utf-8', 'ignore'))
        img_path = message.decode('utf-8', 'ignore')
        start = time.time()
        result = ocr.ocr(img_path, det=False)
        print(result)
        res = result[0][0]
        end = time.time()
        print(res, end - start)
        socket.send(res.encode('utf-8'))
