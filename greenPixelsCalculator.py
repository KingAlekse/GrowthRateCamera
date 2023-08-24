from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import colors
from threading import Thread


class Laskuri(Thread):
   def __init__(self, folder):
      super().__init__()
      self.folder = folder
      self.mones = 1
      self.monta = 0
      self.progress = 0
      self.pisteet = np.array([])

   def getProgress(self):
      return self.progress

   
   #this will iterate jpg images in folder, transform them in numpy array, turn rgb to hsv and then mask all 'green' pixels and count amount
   # need to upgrade this, since rgb to hsvtransformation may be unnecessary
   def run(self):
      files = os.listdir(fr"{self.folder}")
      files = [f for f in files if f.endswith("jpg")] #Filtering only the files.
      self.monta = len(files)
      if self.monta != 0:
         for i in files:
            img = np.array(Image.open(fr"{self.folder}\{i}"))
            uusi = img.reshape(len(img)*len(img[0]),3)
            apuUusi = uusi/[255, 255, 255]
            apuUusi = colors.rgb_to_hsv(apuUusi)
            apuUusi = (apuUusi*[360, 100, 100]).astype(int)
            c = (np.logical_and(apuUusi[:, 0] >= 150, apuUusi[:, 0] <= 170)) & (np.logical_and(
            apuUusi[:, 1] > 45, apuUusi[:, 1] < 85)) & (np.logical_and(apuUusi[:, 2] < 50, apuUusi[:, 2] > 15))
            self.pisteet = np.append(self.pisteet, np.sum(c))

            self.progress = int(100*(self.mones/self.monta))
            self.mones += 1
               
      self.pisteet = (self.pisteet / 6000).astype(int)


   