from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QWidget, QTextBrowser, QSpinBox
from PyQt5 import QtCore, uic
from PyQt5.QtGui import QPixmap, QImage
import sys
from PIL import Image
import numpy as np
from matplotlib import colors

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi('kuva.ui', self)

        self.valitse = self.findChild(QPushButton, "valitseKuvaNappi")
        self.valitse.clicked.connect(self.valitseKuva)

        self.tiedostoKentta = self.findChild(QTextBrowser, "tiedostoKentta")
        self.kuvaPolku = ""

        self.lataa = self.findChild(QPushButton, "lataaKuvaNappi")
        self.lataa.clicked.connect(self.lataaKuva)
        self.alkuKuva = self.findChild(QLabel, "alkuKuva")

        self.prosessoi = self.findChild(QPushButton, "prosessoiNappi")
        self.prosessoi.clicked.connect(self.prosessoiKuva)
        self.loppuKuva = self.findChild(QLabel, "loppuKuva")

        self.hLower = self.findChild(QSpinBox, "hueLower")
        self.hUpper = self.findChild(QSpinBox, "hueUpper")

        self.sLower = self.findChild(QSpinBox, "sLower")
        self.sUpper = self.findChild(QSpinBox, "sUpper")

        self.vLower = self.findChild(QSpinBox, "vLower")
        self.vUpper = self.findChild(QSpinBox, "vUpper")

        #self.hLower.valueChanged.connect(self.prosessoiKuva)
        #self.hUpper.valueChanged.connect(self.prosessoiKuva)
        #self.sLower.valueChanged.connect(self.prosessoiKuva)
        #self.sUpper.valueChanged.connect(self.prosessoiKuva)
        #self.vLower.valueChanged.connect(self.prosessoiKuva)
        #self.vUpper.valueChanged.connect(self.prosessoiKuva)

        self.show()

    def valitseKuva(self):
        kuva = QFileDialog.getOpenFileName(self, "Valitse kuva", "", "(*.jpg)")
        self.kuvaPolku = kuva[0]
        print(str(self.kuvaPolku))
        self.tiedostoKentta.setText(str(kuva[0]))

    def lataaKuva(self):
        self.pixmap1 = QPixmap(self.kuvaPolku)
        
        self.alkuKuva.setPixmap(self.pixmap1)

    def prosessoiKuva(self):
        self.adjustValues()
        img = np.array(Image.open(str(self.kuvaPolku)).rotate(90))
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)

        self.loppuKuva.setPixmap(QPixmap(qImg))

    def adjustValues(self):
        if self.hLower.value() > self.hUpper.value():
            self.hUpper.setValue(self.hLower.value()+1)
        if self.sLower.value() > self.sUpper.value():
            self.sUpper.setValue(self.sLower.value()+1)
        if self.vLower.value() > self.vUpper.value():
            self.vUpper.setValue(self.vLower.value()+1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()