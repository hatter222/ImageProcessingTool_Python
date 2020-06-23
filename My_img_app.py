import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot

from Mainwindow import Ui_Form
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import numpy as np
from Processing import Thread

class Mainwindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(Mainwindow, self).__init__()
        self.load_flag = False
        self.gray_flag = False
        self.image = None
        self.gray = None
        self.msg = None
        self.filters = None
        self.text = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
    #function to initialise the buttons
        self.ui.Load.clicked.connect(self.slot_load)
        self.ui.Gray_scale.clicked.connect(self.slot_gray)
        self.ui.Mean.clicked.connect(self.set_mean)
        self.ui.Median.clicked.connect(self.set_median)
        self.ui.Gauss.clicked.connect(self.set_gaussian)
        self.ui.Bilateral.clicked.connect(self.set_bilateral)
        self.ui.Clear.clicked.connect(self.clear_all)
        self.ui.Erosion.clicked.connect(self.set_erosion)
        self.ui.Dilation.clicked.connect(self.set_dilation)
        self.ui.Closing.clicked.connect(self.set_closing)
        self.ui.Opening.clicked.connect(self.set_opening)
        self.ui.Open_camera.clicked.connect(self.open_camera)
        self.ui.Load_Video.clicked.connect(self.load_video)


    def slot_load(self):
        print("load")
        file = str(QFileDialog.getOpenFileName(self,"Open Image"," "," "))
        #print(file[-9:-6])

        if file == None:
            self.msg = "Load input"
            self.display()
        elif file[-9:-6]=='jpg' or file[-9:-6]=='png':

            self.image = cv2.imread(file[2:-6], 1)
            img = self.conv2Qimage()
            self.load_flag = True
            # img = QtGui.QImage(QtGui.QImageReader("lena2.jpg").read())
            pixmap = QPixmap.fromImage(img)
            h = self.ui.Screen_1.height()
            w = self.ui.Screen_1.width()
            self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.ui.Screen_2.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            self.text = "Load"
            self.ui.usedcommand.setText(self.text)
        else :
            self.msg = "Load correct input"
            self.display()

    def slot_gray(self):
        print("gray")
        if self.load_flag:
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
            self.text = self.text + "--> gray"
            self.ui.usedcommand.setText(self.text)
            self.gray_flag = True
        else:
            self.msg = "Image is not loaded"
            self.display()

    def set_mean(self):
        self.filters = "mean"
        self.slot_filter()
    def set_median(self):
        self.filters = "median"
        self.slot_filter()
    def set_gaussian(self):
        self.filters = "gaussian"
        self.slot_filter()
    def set_bilateral(self):
        self.filters = "bilateral"
        self.slot_filter()
    def set_erosion(self):
        self.filters = "erosion"
        self.slot_filter()
    def set_dilation(self):
        self.filters = "Dilation"
        self.slot_filter()
    def set_closing(self):
        self.filters = "closing"
        self.slot_filter()
    def set_opening(self):
        self.filters = "opening"
        self.slot_filter()

    def clear_all(self):
        self.ui.Screen_1.clear()
        self.ui.Screen_2.clear()
        self.image = None
        self.gray = None
        self.load_flag = False
        self.gray_flag = False



    def slot_filter(self):
        if self.load_flag:
            if self.gray_flag:
                num = self.getkernel()
                kernel = np.ones((num, num), np.uint8)
                blur = None
                if self.filters == "mean":
                    blur = cv2.blur(self.gray, (num, num))
                elif self.filters == "median":
                    blur = cv2.medianBlur(self.gray, num)
                elif self.filters == "gaussian":
                    blur = cv2.GaussianBlur(self.gray, (num, num), 0)
                elif self.filters == "bilateral":
                    num2 = self.getkernel()
                    blur = cv2.bilateralFilter(self.gray, num, num2, num2)
                elif self.filters == "erosion":
                    blur = cv2.erode(self.gray, kernel)
                elif self.filters == "Dilation":
                    blur = cv2.dilate(self.gray, kernel)
                elif self.filters == "opening":
                    blur = cv2.morphologyEx(self.gray, cv2.MORPH_OPEN, kernel)
                elif self.filters == "closing":
                    blur = cv2.morphologyEx(self.gray, cv2.MORPH_CLOSE, kernel)

                else:
                    print("not working")
                height, width, depth = self.image.shape
                img = QImage(blur.data, width, height, width, QImage.Format_Grayscale8)
                pixmap = QPixmap.fromImage(img)
                h = self.ui.Screen_1.height()
                w = self.ui.Screen_1.width()
                self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
                self.text = "gray" + "-->" + self.filters + " with kernel-" + str(num)
                self.ui.usedcommand.setText(self.text)
            else :
                self.msg = "Gray Image is not Loaded"
                self.display()
        else:
            self.msg ="Input Image is not Loaded"
            self.display()

    def conv2Qimage(self):
        height, width, depth = self.image.shape
        image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = QImage(image.data, width, height, width * depth, QImage.Format_RGB888)
        return img

    def getkernel(self):
        default = 5
        num, ok = QtWidgets.QInputDialog.getInt(self, "Filter Input", "Enter a kernel", default, 0, 1000, 1)
        if ok:
            return num

    def update_command(attach, self=None):
        self.text = self.text + str(attach)
        self.ui.usedcommand.setText(self.text)

    def display(self):
        error_dialog = QtWidgets.QErrorMessage()
        error_dialog.showMessage(self.msg)
        error_dialog.exec()


    @pyqtSlot(QImage)
    def setImage(self, image):
        pixmap = QPixmap.fromImage(image)
        h = self.ui.Screen_1.height()
        w = self.ui.Screen_1.width()
        self.ui.Screen_1.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
        self.ui.Screen_2.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))

    def open_camera(self):
         th = Thread(self)
         th.changePixmap.connect(self.setImage)
         th.start()

    def load_video(self):
        print("load")
        file = str(QFileDialog.getOpenFileName(self, "Open Image", " ", " "))
        filename = file[2:-6]
        th = Thread(self)
        th.load(filename)
        th.changePixmap.connect(self.setImage)
        th.start()





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Mainwindow()
    w.show()
    app.exec()