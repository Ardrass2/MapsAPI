import os
import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self, map_request):
        super().__init__()
        self.getImage(map_request)
        self.initUI()

    def getImage(self, map_request):
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.img = ImageQt.ImageQt(Image.open(BytesIO(response.content)))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap.fromImage(self.img))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    coords = list(map(float, input().split()))
    ex = Example(f"http://static-maps.yandex.ru/1.x/?ll={coords[1]},{coords[0]}&spn=0.01,0.01&l=sat")
    ex.show()
    sys.exit(app.exec())