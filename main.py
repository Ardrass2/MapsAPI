import os
import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton

SCREEN_SIZE = [600, 800]


class Example(QWidget):
    def __init__(self, map_request):
        super().__init__()
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.btn = QRadioButton(self)
        self.btn_2 = QRadioButton(self)
        self.btn_3 = QRadioButton(self)
        self.btn.move(5, 10)
        self.btn_2.move(5, 30)
        self.btn_3.move(5, 50)
        self.btn.setText('Схема')
        self.btn_2.setText('Спутник')
        self.btn_3.setText('Гибрид')
        self.image.resize(*SCREEN_SIZE)
        self.params = {
            "ll": ",".join(map_request[0]),
            "spn": ",".join(map_request[1]),
            "l": map_request[2],
            "z": "8"
        }
        self.btn.clicked.connect(self.scheme)
        self.btn_2.clicked.connect(self.satellite)
        self.btn_3.clicked.connect(self.hybrid)
        self.getImage()

    def scheme(self):
        print(self.params['l'])
        if self.params['l'] == 'sat':
            self.params['l'] = 'map'
        elif self.params['l'] == 'sat,skl':
            self.params['l'] = 'map'
        self.getImage()

    def satellite(self):
        print(self.params['l'])
        if self.params['l'] == 'map':
            self.params['l'] = 'sat'
        elif self.params['l'] == 'sat,skl':
            self.params['l'] = 'sat'
        self.getImage()

    def hybrid(self):
        print(self.params['l'])
        if self.params['l'] == 'sat':
            self.params['l'] = 'sat,skl'
        elif self.params['l'] == 'map':
            self.params['l'] = 'sat,skl'
        self.getImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.upscale_map()
        if event.key() == Qt.Key.Key_PageUp:
            self.downscale_map()
        if event.key() == Qt.Key.Key_Left:
            self.move_left()
        if event.key() == Qt.Key.Key_Right:
            self.move_right()
        if event.key() == Qt.Key.Key_Up:
            self.move_up()
        if event.key() == Qt.Key.Key_Down:
            self.move_down()

    def move_left(self):
        ll = list(map(float, self.params["ll"].split(",")))
        ll[0] -= float(self.params["spn"].split(",")[0]) * 2 \
            if ll[0] - float(self.params["spn"].split(",")[0]) * 2 >= 0 else 0
        self.params["ll"] = ",".join(map(str, ll))
        self.update_map()

    def move_right(self):
        ll = list(map(float, self.params["ll"].split(",")))
        ll[0] += float(self.params["spn"].split(",")[0]) * 2 \
            if ll[0] + float(self.params["spn"].split(",")[0]) * 2 < 180 else 0
        self.params["ll"] = ",".join(map(str, ll))
        self.update_map()

    def move_up(self):
        ll = list(map(float, self.params["ll"].split(",")))
        ll[1] += float(self.params["spn"].split(",")[1]) * 2 \
            if ll[1] + float(self.params["spn"].split(",")[0]) * 2 <= 180 else 0
        self.params["ll"] = ",".join(map(str, ll))
        self.update_map()

    def move_down(self):
        ll = list(map(float, self.params["ll"].split(",")))
        ll[1] -= float(self.params["spn"].split(",")[1]) * 2 \
            if ll[1] - float(self.params["spn"].split(",")[0]) * 2 >= 0 else 0
        self.params["ll"] = ",".join(map(str, ll))
        self.update_map()

    def upscale_map(self):
        new_spn = round(float(self.params["spn"].split(",")[0]) * 2, 3)\
            if round(float(self.params["spn"].split(",")[0]) * 2, 3) < 80 else 90.000
        self.params["spn"] = ",".join([str(new_spn), str(new_spn)])
        print(self.params["spn"])
        self.update_map()

    def downscale_map(self):
        new_spn = round(float(self.params["spn"].split(",")[0]) / 2, 3)
        self.params["spn"] = ",".join([str(new_spn), str(new_spn)])
        print(self.params["spn"])
        self.update_map()

    def update_map(self):
        self.image.clear()
        self.getImage()

    def getImage(self):
        response = requests.get("http://static-maps.yandex.ru/1.x/", params=self.params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))
        self.image.setPixmap(QPixmap.fromImage(self.img))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    coords = list(map(float, input().split()))
    ex = Example(list(([str(coords[1]), str(coords[0])], [str(0.01), str(0.01)], "sat")))
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
