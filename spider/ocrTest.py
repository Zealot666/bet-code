import time

from paddleocr import PaddleOCR
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

if __name__ == '__main__':
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    img_path = r"D:\code\spider\test.png"
    start = time.time()
    result = ocr.ocr(img_path, det=False)
    for i in result:
        print(i, "S")
    res = result[0][0]
    end = time.time()
    print("S")
    print(res, end - start)
