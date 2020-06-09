import sys
from PyQt5 import QtWidgets, QtGui,QtCore
from ImageProcessingTool.Mainwindow import Ui_Form
import cv2
from PyQt5.QtGui import QImage ,QPixmap


class Mainwindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Mainwindow, self).__init__()
        self.load_flag = False
        self.image=None
        self.gray=None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.Load.clicked.connect(self.slot_load)
        self.ui.Gray_scale.clicked.connect(self.slot_gray)
        self.ui.Mean.clicked.connect(self.slot_mean)
        self.ui.Median.clicked.connect(self.slot_median)
        self.ui.Gauss.clicked.connect(self.slot_gauss)

    def slot_load(self):
        print("load")
        self.image =cv2.imread('lena2.jpg',1)
        img = self.conv2Qimage()
        self.load_flag = True
        #img = QtGui.QImage(QtGui.QImageReader("lena2.jpg").read())
        pixmap = QPixmap.fromImage(img)
        h = self.ui.Screen_1.height()
        w = self.ui.Screen_1.width()
        self.ui.Screen_1.setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio))
        self.ui.Screen_2.setPixmap(pixmap.scaled(w,h,QtCore.Qt.KeepAspectRatio))


    def slot_gray(self):
        print("gray")
        if self.load_flag == True:
            self.ui.Gray_scale.setEnabled(True)
            image = self.image
            height, width, depth = image.shape
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            img = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(img)
            h = self.ui.Screen_1.height()
            w = self.ui.Screen_1.width()
            self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.gray = image

    def slot_mean(self):
        print("mean")
        num = self.getkernel()
        blur = cv2.blur(self.gray, (num,num))
        height, width, depth = self.image.shape
        img = QImage(blur.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(img)
        h = self.ui.Screen_1.height()
        w = self.ui.Screen_1.width()
        self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

    def slot_median(self):
        print("median")
        num = self.getkernel()
        blur = cv2.medianBlur(self.gray,num)
        height, width, depth = self.image.shape
        img = QImage(blur.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(img)
        h = self.ui.Screen_1.height()
        w = self.ui.Screen_1.width()
        self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

    def slot_gauss(self):
        print("gauss")
        num = self.getkernel()
        blur = cv2.GaussianBlur(self.gray, (num,num),0)
        height, width, depth = self.image.shape
        img = QImage(blur.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(img)
        h = self.ui.Screen_1.height()
        w = self.ui.Screen_1.width()
        self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

    def conv2Qimage(self):
        height, width, depth = self.image.shape
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = QImage(image.data, width, height, width * depth, QImage.Format_RGB888)
        return img
    def getkernel(self):
        default = 5
        num, ok = QtWidgets.QInputDialog.getInt(self, "Filter Input", "Enter a kernel",default,0,1000,1)
        if ok:
            return num



app = QtWidgets.QApplication(sys.argv)
w = Mainwindow()
w.show()
app.exec()



