import sys
import os
import requests

from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtWidgets import QInputDialog

class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('API.ui', self)
        ll, ok_pressed = QInputDialog.getText(self,
                                                "Введите координаты через пробел", 
                                                "ширина, долгота =")
        if ok_pressed:
            self.lon, self.lat = ll.split()
        self.api_server = "http://static-maps.yandex.ru/1.x/"
        self.delta = "0.2"
        self.setImage()

    def setImage(self):
        self.params = {
            "ll": ",".join([self.lon, self.lat]),
            "spn": ",".join([str(self.delta), str(self.delta)]),
            "l": "map"
        }
        self.response = requests.get(self.api_server, params=self.params)
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            self.delta2 = self.delta
            self.delta = str(float(self.delta) * 2)
            if float(self.delta) >= 52:
                self.delta = self.delta2
            self.params["spn"] = ",".join([self.delta, self.delta])
            self.response = requests.get(self.api_server, params=self.params)
            self.getImage()
            self.newImage()

        elif event.key() == Qt.Key_PageUp:
            self.delta2 = self.delta
            self.delta = str(float(self.delta) / 2)
            if float(self.delta) < 0.0001:
                self.delta = self.delta2
            self.params["spn"] = ",".join([self.delta, self.delta])
            self.response = requests.get(self.api_server, params=self.params)
            self.getImage()
            self.newImage()

    def newImage(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap) 


    def getImage(self):
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(self.response.content)

    def closeEvent(self, event):
        os.remove(self.map_file)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# для теста использовала координаты 37.530887 55.703118
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
