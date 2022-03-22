import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QTimer, QTime, Qt, QUrl
from PyQt5.QtWebEngineWidgets import *

from features.weather import *

# useful classes and variables

weather_api = WeatherAPI()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_window()

    def main_window(self):
        # первое окно с оновными функциями программы

        uic.loadUi('main.ui', self)
        self.sos_button.clicked.connect(self.sos)

        self.title = "СУСАНИН"
        self.setWindowTitle(self.title)

        # clock display
        self.show_time()
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000 * 60)

        # weather display
        weather, temp = weather_api.get_weather_and_temp()
        self.weather_display.setText(weather.capitalize())
        self.temperature_display.setText(temp)

        # set picture
        label = QLabel(self)
        pixmap = QPixmap(f'img\\{weather}.png')
        label.setPixmap(pixmap)
        rect = self.weather_pic.frameGeometry()
        label.move(rect.x(), rect.y())
        label.resize(rect.width(), rect.height())

        # waether timer
        weather_timer = QTimer(self)
        weather_timer.timeout.connect(self.update_weather)
        weather_timer.start(1000 * 60 * 60)

        # map
        width, heights = self.map.width(), self.map.height()
        print(width, heights)
        with open("map.html", "r", encoding='utf-8') as f:
            page = f.read()
            page = page.replace('{{w}}', str(width - 20))
            page = page.replace('{{h}}', str(heights - 20))
            self.map.setHtml(page)
        self.map.show()

    def sos(self):
        pass

    # method called by timer
    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        print(label_time)
        self.clock.display(label_time)

    def update_weather(self):
        weather, temp = weather_api.get_weather_and_temp()
        self.weather_display.setText(weather)
        self.temperature_display.setText(temp)
        pixmap = QPixmap(f'\\img\\{weather}.png')
        self.weather_pic.setPixmap(pixmap)

        label = QLabel(self)
        pixmap = QPixmap(f'img\\{weather}.png')
        label.setPixmap(pixmap)
        rect = self.weather_pic.frameGeometry()
        label.move(rect.x(), rect.y())
        label.resize(rect.width(), rect.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
