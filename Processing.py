import cv2
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import QImage
from mtcnn import  MTCNN



class Thread(QThread):
    changePixmap = pyqtSignal(QImage,QImage)

    def load(self,set_filename):
        self.set_filename = set_filename
        self.reference = None



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
                self.image = rgbImage
                h, w, ch =   self.image.shape
                bytesPerLine = ch * w
                self.img1 = QImage(  self.image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.img2 = QImage(self.image.data, w, h, bytesPerLine, QImage.Format_RGB888)
                self.changePixmap.emit(self.img1,self.img2)

    def face_recognition1(self):
        detector = MTCNN()
        detector.detect_faces(self.image)




