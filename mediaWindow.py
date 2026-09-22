from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl, Qt, Slot, QDirListing
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QMainWindow, QLabel, QSlider, QGridLayout, QWidget, QPushButton


class MediaWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seanify music player")
        self.resize(500, 200)

        # 1. Create main widget
        container = QWidget()
        self.setCentralWidget(container)
        layout = QGridLayout(container)

        # 2. Multimedia setup
        # 2.1 Player
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.volumeLevel = 0.5
        self.audioOutput.setVolume(self.volumeLevel)

        # 2.2 Sliders
        # 2.2.1 Duration slider
        self.durationSlider = QSlider(Qt.Orientation.Horizontal)
        self.durationSlider.sliderMoved.connect(self.change_duration)

        # self.player.positionChanged.connect(self.durationSlider.setValue)
        self.player.durationChanged.connect(self.update_duration_slider_position)

        # 2.2.2 Volume slider
        self.volumeSlider = QSlider(Qt.Orientation.Vertical)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(self.change_volume)

        # 2.3 Control buttons
        # 2.3.1 Control methods
        @Slot()
        def playMusic():
            print("Music started playing")
            self.player.play()

        @Slot()
        def pauseMusic():
            print("Music paused")
            self.player.pause()

        @Slot()
        def nextSong():
            print("Next song started playing")

        @Slot()
        def previousSong():
            print("Previous song started playing")

        # 2.3.2 Buttons themselves
        playButton = QPushButton()
        playButton.setIcon(QIcon("images/controls/play.png"))
        playButton.clicked.connect(playMusic)

        pauseButton = QPushButton()
        pauseButton.setIcon(QIcon("images/controls/pause.png"))
        pauseButton.clicked.connect(pauseMusic)

        nextSongButton = QPushButton()
        nextSongButton.setIcon(QIcon("images/controls/next-button.png"))
        nextSongButton.clicked.connect(nextSong)

        previousSongButton = QPushButton()
        previousSongButton.setIcon(QIcon("images/controls/previous.png"))
        previousSongButton.clicked.connect(previousSong)

        # 2.3.3 Button styling
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)

        button_size = (30, 30)

        playButton.setFixedSize(*button_size)
        pauseButton.setFixedSize(*button_size)
        nextSongButton.setFixedSize(*button_size)
        previousSongButton.setFixedSize(*button_size)

        # 3. Adding widgets
        # 3.1 Control buttons
        layout.addWidget(playButton, 1, 2)
        layout.addWidget(pauseButton, 1, 1)
        layout.addWidget(nextSongButton, 1, 3)
        layout.addWidget(previousSongButton, 1, 0)

        # 3.2 Slider
        layout.addWidget(self.durationSlider, 2, 0, 1, 4)

        layout.addWidget(self.volumeSlider, 1, 4, 2, 1)

        # 3.3 Duration in numbers
        rawSeconds = self.player.position() // 1000
        seconds = rawSeconds
        if rawSeconds % 60 == 0:
            seconds = 0
        minutes = self.player.position() // 60000
        playedDuration = f"{minutes}:{seconds}"

        totalDuration = self.player.duration()
        totalDurationSeconds = totalDuration % 60
        totalDurationMinutes = totalDuration // 60

        formattedDuration = QLabel(f"{playedDuration}/{totalDurationMinutes}:{totalDurationSeconds}")
        layout.addWidget(formattedDuration)

        # 4. Load media
        self.player.setSource(QUrl.fromLocalFile("./songs/wiley.mp3"))
        self.player.play()

        # 5. Get directory files
        self.songs = QDirListing("/Users/seansteenhuis/Documents/Music/Songs")
        # for song in self.songs:
        #     print(f"Filename {song.absoluteFilePath()}")

    def update_duration_slider_position(self, duration_ms):
        if not self.durationSlider.isSliderDown():
            self.durationSlider.setMaximum(duration_ms)

    def change_duration(self, durationValue):
        self.player.setPosition(durationValue)

    def change_volume(self, volumeValue):
        self.volumeLevel = volumeValue / 100
        self.audioOutput.setVolume(self.volumeLevel)
        print(f"Current volume: {self.volumeLevel}")
