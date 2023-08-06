import sys
import os.path
import logging as log
import argparse

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap

from .ui import QCrop
from . import __version__


def main():
    parser = argparse.ArgumentParser(prog='qcrop')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('image', help="Path to the image file to crop.")
    args = parser.parse_args()

    stream_handler = log.StreamHandler()
    log.basicConfig(handlers=(stream_handler,),
                    level='DEBUG',
                    format='%(asctime)s.%(msecs)03d:%(levelname)-8s:%(module)-12s# %(message)s',
                    datefmt='%Y%m%d-%H%M%S'
                    )

    if os.path.isfile(args.image):
        APP = QApplication(sys.argv)
        path = sys.argv[1]
        img = QPixmap(path)
        WIN = QCrop(img)

        rc = WIN.exec()
        if rc == QDialog.Accepted:
            WIN.image.save('{}.cropped{}'.format(*os.path.splitext(path)))

        APP.exit()
    else:
        print('File not found.')
        sys.exit(1)


if __name__ == '__main__':
    main()
