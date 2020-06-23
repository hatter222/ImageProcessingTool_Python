import cv2
import sys
from PyQt5.QtCore import QThread, Qt,pyqtSignal,pyqtSlot
from PyQt5.QtGui import QImage , QPixmap


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    def load(self,set_filename):
        self.set_filename = set_filename


    def run(self):
        if self.set_filename == None :
            cap = cv2.VideoCapture(0)
        else:
            print(self.set_filename)
            cap = cv2.VideoCapture(self.set_filename)
        while True:
            ret , frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                img1 = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)

                self.changePixmap.emit(img1)
