import sys
from PySide6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QMainWindow
from controlButtons import play_music, stop_music, next_song, previous_song


# class Window(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setStyleSheet("background-color: yellow;")

#         self.show()


app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

play_button = QPushButton("Play")
play_button.clicked.connect(play_music)

stop_button = QPushButton("Stop")
stop_button.clicked.connect(stop_music)

next_song_button = QPushButton("Next")
next_song_button.clicked.connect(next_song)

previous_song_button = QPushButton("Previous")
previous_song_button.clicked.connect(previous_song)

layout.addWidget(play_button)
layout.addWidget(stop_button)
layout.addWidget(next_song_button)
layout.addWidget(previous_song_button)

window.show()
app.exec()
