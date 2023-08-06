import sys
import os.path
import logging as log

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap

from .qcrop import QCrop


def main():
    stream_handler = log.StreamHandler()
    log.basicConfig(handlers=(stream_handler,),
                    level='DEBUG',
                    format='%(asctime)s.%(msecs)03d:%(levelname)-8s:%(module)-12s# %(message)s',
                    datefmt='%Y%m%d-%H%M%S'
                    )

    APP = QApplication(sys.argv)

    if sys.argv[1] and os.path.isfile(sys.argv[1]):
        path = sys.argv[1]
        img = QPixmap(path)
        WIN = QCrop(img)

        rc = WIN.exec()
        if rc == QDialog.Accepted:
            WIN.image.save('{}.cropped{}'.format(*os.path.splitext(path)))

    APP.exit()


if __name__ == '__main__':
    main()
