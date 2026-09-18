import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtGui import QIcon
from controlButtons import play_music, stop_music, next_song, previous_song


app = QApplication(sys.argv)

window = QWidget()
window.setStyleSheet("background-color: blue;")
layout = QVBoxLayout(window)

play_button = QPushButton()
play_button.setIcon(QIcon("images/controls/play.png"))
play_button.clicked.connect(play_music)

stop_button = QPushButton()
stop_button.setIcon(QIcon("images/controls/pause.png"))
stop_button.clicked.connect(stop_music)

next_song_button = QPushButton()
next_song_button.setIcon(QIcon("images/controls/next.png"))
next_song_button.clicked.connect(next_song)

previous_song_button = QPushButton()
previous_song_button.setIcon(QIcon("images/controls/previous.png"))
previous_song_button.clicked.connect(previous_song)

layout.addWidget(play_button)
layout.addWidget(stop_button)
layout.addWidget(next_song_button)
layout.addWidget(previous_song_button)

window.show()
app.exec()
