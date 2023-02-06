import os
import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, map_request):
        super().__init__()
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.params = {
            "ll": ",".join(map_request[0]),
            "spn": ",".join(map_request[1]),
            "l": map_request[2]
        }

        self.getImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageDown:
            self.change_scale(1.5)
        if event.key() == Qt.Key.Key_PageUp:
            self.change_scale(0.6)

    def change_scale(self, change):
        new_spn = round(float(self.params["spn"].split(",")[0]) * change, 3)\
            if round(float(self.params["spn"].split(",")[0]) * change, 3) < 80 else 80.000
        self.params["spn"] = ",".join([str(new_spn), str(new_spn)])
        print(self.params["spn"])
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
    # Отлов ошибок
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    coords = list(map(float, input().split()))
    ex = Example(list(([str(coords[1]), str(coords[0])], [str(0.01), str(0.01)], "sat")))
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
