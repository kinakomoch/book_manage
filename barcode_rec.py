import subprocess
import time

import cv2
import numpy as np
from pyzbar.pyzbar import decode


def barcode_rec():
    '''
    barcode_rec recodes isbns through the video

    Return:
        isbns: a list of string
    '''

    capture = cv2.VideoCapture(0)
    count = 0
    start = time.time()
    isbns = set()
    cmd = 'next'

    while True:
        # Capture frame-by-frame
        try:
            ret, frame = capture.read()
            if ret == False:
                break

            # gray_image is gray scale frame
            # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_image = frame
            # Display the resulting frame
            cv2.imshow('frame', gray_image)

            if decode(gray_image) == []:
                count += 1
            else:
                # isbn is str, decode(gray_image) must be a tuple
                isbn = decode(gray_image)[0][0].decode('utf-8', 'ignore')

                # isbn 13 is only needed, and records just only one time
                if isbn[:3] == '978' and isbn not in isbns:
                    print(isbn)
                    subprocess.call('say "%s"' % cmd, shell=True)
                    isbns.add(isbn)
                    count = 0

            # time count is also OK, but this is easier than it
            if count > 300:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # if you want to quit, you can use Ctrl-C safely
        except KeyboardInterrupt:
            break

    # processing time of taking a video
    elapsed_time = time.time() - start
    print('\n', elapsed_time, '[sec]')

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()

    return isbns

if __name__ == '__main__':
    isbns = barcode_rec()
    print(isbns)
