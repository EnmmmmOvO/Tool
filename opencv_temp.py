import cv2
import os
import requests
import time
import shutil


def compress_img_CV(name):
    image = cv2.imread(name + '.png')
    cv2.imwrite(name + '.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])


def screen_cap():
    payload = {'isOverlayRequired': 'True',
               'apikey': 'K84290104588957',
               'language': 'chs',
               }

    while True:
        try:
            name = 'example/' + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
            os.system('adb exec-out screencap -p > ' + name + '.png')
            compress_img_CV(name)
            with open(name + '.jpg', 'rb') as f:
                r = requests.post('https://api.ocr.space/parse/image',
                                  files={name: f},
                                  data=payload,
                                  )
            with open(name + '.txt', 'wb') as p:
                p.write(r.content)
            time.sleep(0 * 3600 + 0 * 60 + 20)
            break
        except KeyboardInterrupt:
            shutil.rmtree('example')
            os.mkdir('example')
            break
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    screen_cap()