import sys

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QTimer, QTime, Qt, QUrl
from PyQt5.QtWebEngineWidgets import *

import os

from features.weather import *
from features.voice_helper import *

# useful classes and variables

weather_api = WeatherAPI()
voice_recog = Interaction()

from os import listdir
print([f for f in listdir()])

a = open('some.txt', 'r').readlines()
print(a)


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
        with open("map.html", "r", encoding='utf-8') as f:
            page = f.read()
            page = page.replace('{{w}}', str(width - 20))
            page = page.replace('{{h}}', str(heights - 20))
            self.map.setHtml(page)
        self.map.show()

        # voice
        self.voice.clicked.connect(self.help)
    
    def help(self):
        words = 'Чем могу помочь'
        say(words)
        self.voice_recognize()
    
    def voice_recognize(self):
        said = voice_recog.question()
        if not(said):
            say('Не могу понять')
        elif 'сегодня' in said or 'погода' in said:
            say(f'Сегодня в Воронеже {weather_api.temp} градусов, {weather_api.weather}')
        elif 'время' in said or 'час' in said:
            current_time = QTime.currentTime()
            h, m = [i for i in current_time.toString('hh:mm').split(':')]
            say(f'Сечас {h} часов {m} минут')

    def sos(self):
        words = 'Не паникуйте. За помощью наберите 0 1 или 1 1 2'
        say(words)

    # method called by timer
    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm')
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
