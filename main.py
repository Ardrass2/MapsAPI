import os
import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [1000, 1000]


class Example(QWidget):
    def __init__(self, map_request):
        super().__init__()
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.params = {
            "ll": ",".join(map_request[0]),
            "spn": ",".join(map_request[1]),
            "l": map_request[2],
            "z": "8"
        }
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
