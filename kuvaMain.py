# note to myself: translate methods to english and add comments and etc

from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, 
                             QLabel, QFileDialog, QWidget, QTextBrowser, QSpinBox, QRadioButton)
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

        self.blackRadio = self.findChild(QRadioButton, "blackRadio")
        self.blackRadio.setChecked(True)
        
        self.whiteRadio = self.findChild(QRadioButton, "whiteRadio")
        
        self.redRadio = self.findChild(QRadioButton, "redRadio")
        

        self.show()

    def valitseKuva(self):
        kuva = QFileDialog.getOpenFileName(self, "Valitse kuva", "", "(*.jpg)")
        self.kuvaPolku = kuva[0]
        self.tiedostoKentta.setText(str(kuva[0]))
        self.pixmap1 = QPixmap(self.kuvaPolku)
        self.alkuKuva.setPixmap(self.pixmap1)


    #this turns image to numpy array, turns rgb values to hsv and then counts pixels in given range
    #rgb to hsv transformation may actually be unnecessary...
    def prosessoiKuva(self):
        self.adjustValues()
        try:
            img = np.array(Image.open(str(self.kuvaPolku)))
            height, width, _ = img.shape
            bytesPerLine = 3 * width

            uusi = img.reshape(len(img)*len(img[0]), 3)
            apuUusi = uusi/[255, 255, 255]
            apuUusi = colors.rgb_to_hsv(apuUusi)
            apuUusi = (apuUusi*[360, 100, 100]).astype(int)
            c = (np.logical_and(apuUusi[:, 0] >= int(self.hLower.value()), apuUusi[:, 0] <= int(self.hUpper.value()))) & (np.logical_and(
            apuUusi[:, 1] >= int(self.sLower.value()), apuUusi[:, 1] <= int(self.sUpper.value()))) & (np.logical_and(
                apuUusi[:, 2] >= int(self.vLower.value()), apuUusi[:, 2] <= int(self.vUpper.value())))
            
            if self.redRadio.isChecked() == True:
                uusi[c, :] = [255, 0, 0]
            elif self.whiteRadio.isChecked() == True:
                uusi[c, :] = [255, 255, 255]
            else:
                uusi[c, :] = [0, 0, 0]

            qImg = QImage(uusi.data, width, height, bytesPerLine, QImage.Format_RGB888)
            self.loppuKuva.setPixmap(QPixmap(qImg))
        
        except Exception as e:
            self.loppuKuva.setText(str(e))

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
