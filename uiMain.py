from PyQt5.QtWidgets import (QMainWindow, 
                             QApplication, 
                             QWidget, 
                             QPushButton, 
                             QLineEdit, 
                             QTextBrowser, 
                             QFileDialog, 
                             QProgressBar,
                             QCheckBox)
from PyQt5 import uic, QtCore
from pathlib import Path
from greenPixelsCalculator import Laskuri
import sys, time
from threading import *
import numpy

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


class UI(QMainWindow):
    progressChanged = QtCore.pyqtSignal(int)
    def __init__(self):
        
        super().__init__()

        uic.loadUi("uiTesti.ui", self)

        self.setWindowTitle("Vihreät Hama-helmet laskuri")

        self.yhteysOK = False
        self.client = None

        self.data = None

        self.path = None

        self.projekti = self.findChild(QLineEdit, "projektiKentta")

        self.tunnus = self.findChild(QLineEdit, "TunnusKentta")
        self.salasana = self.findChild(QLineEdit, "SalasanaKentta")

        self.viesti = self.findChild(QTextBrowser, "yhteysViestiKentta")

        self.DBNappi = self.findChild(QPushButton, "DBNappi")
        self.DBNappi.clicked.connect(self.DBPainettU)

        self.kansioNappi = self.findChild(QPushButton, "kansioNappi")
        self.kansioNappi.clicked.connect(self.kansioPainettu)
        self.kansioKentta = self.findChild(QTextBrowser,"kansioKentta")

        self.analysoiNappi = self.findChild(QPushButton, "analysoiNappi")
        self.analysoiNappi.clicked.connect(self.analysoiPainettu)

        self.lataaNappi = self.findChild(QPushButton, "lataaNappi")
        self.lataaNappi.clicked.connect(self.tallenna)

        self.pilviCheck = self.findChild(QCheckBox, "pilviCheck")
        self.pilviCheck.setCheckable(False)

        self.csvCheck = self.findChild(QCheckBox, "csvCheck")
        self.csvCheck.setCheckable(False)

        self.pBar = self.findChild(QProgressBar, "progressBar")
        self.progressChanged.connect(self.pBar.setValue)

        self.show()

    def kansioPainettu(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Valitse kansio")
        if dir_name:
            newpath = Path(dir_name)
            self.kansioKentta.setText(str(newpath))
            self.path = str(newpath)

    def DBPainettU(self):
        tunnus = self.tunnus.text()
        salasana = self.salasana.text()

        try:    
            cluster = f"mongodb+srv://{tunnus}:{salasana}@cluster0.q0twyxy.mongodb.net/?retryWrites=true&w=majority"
            self.client = MongoClient(cluster, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            self.viesti.setText("Ok")
            self.yhteysOK = True
            self.pilviCheck.setCheckable(True)
        
        except Exception as e:
            self.viesti.setText(str(e))
            self.pilviCheck.setChecked(False)
            self.pilviCheck.setCheckable(False)
            self.yhteysOK = False

    def tallenna(self):
        if self.pilviCheck.isChecked() and self.yhteysOK == True and type(self.data)== numpy.ndarray:
            db = self.client.GrowthRateCamera
            green = db.GreenData
            if self.projekti == None:
                self.projekti = ""
            for i in range(len(self.data)):
                green.insert_one({
                    "project":str(self.projekti.text()),
                    "picID":i,
                    "greenPixels":int(self.data[i])
                    })

    #need to check this later. may have one too many strings...

    def edista(self):
        laskuri = Laskuri(fr"{self.kansioKentta.toPlainText()}")
        laskuri.start()
        
        while True:
            time.sleep(0.1)
            if laskuri.is_alive():
                self.progressChanged.emit(laskuri.getProgress())
            else:
                self.progressChanged.emit(laskuri.getProgress())
                self.data = laskuri.pisteet
                break

    def analysoiPainettu(self):
        t1 = Thread(target=self.edista)
        t1.start()


        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    sys.exit(app.exec_())