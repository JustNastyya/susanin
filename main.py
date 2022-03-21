import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtWidgets import QInputDialog, QColorDialog
from PyQt5.QtCore import QTimer, QTime, Qt

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

        # clock display
        self.show_time()
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000 * 60)

        # weather display
        weather, temp = weather_api.get_weather_and_temp()
        self.weather_display.setText(weather)
        self.temperature_display.setText(temp)
        # set picture
        weather_timer = QTimer(self)
        weather_timer.timeout.connect(self.update_weather)
        timer.start(1000 * 60 * 60)

    def sos(self):
        pass

    # method called by timer
    def show_time(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm')
        self.clock.display(label_time)
    
    def update_weather(self):
        weather, temp = weather_api.get_weather_and_temp()
        self.weather_display.setText(weather)
        self.temperature_display.setText(temp)
        # set picture


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
