import sys
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl, Qt, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QMainWindow, QSlider, QLabel, QGridLayout, QWidget, QPushButton


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
        self.durationSlider = QSlider()
        self.durationSlider.setOrientation(Qt.Orientation.Horizontal)
        self.durationLabel = QLabel("Totale duur: 0 seconden")
        self.durationLabel.setAlignment(Qt.AlignCenter)

        # 2.2.2 Volume slider
        self.volumeSlider = QSlider()
        self.volumeSlider.setOrientation(Qt.Orientation.Vertical)

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

        # 2.4 Volume controls
        # 2.4.1 Control methods
        @Slot()
        def raiseVolume():
            self.volumeLevel += 0.1
            print(f"Raising volume: {self.volumeLevel}")

        @Slot()
        def lowerVolume():
            self.volumeLevel -= 0.1
            print(f"Lowering volume: {self.volumeLevel}")

        # 2.4.2 Buttons themselves
        volumeUpButton = QPushButton()
        volumeUpButton.setIcon(QIcon("images/controls/volume-up.svg"))
        volumeUpButton.clicked.connect(raiseVolume)

        volumeDownButton = QPushButton()
        volumeDownButton.setIcon(QIcon("images/controls/volume-down.svg"))
        volumeDownButton.clicked.connect(lowerVolume)

        # 3. Adding widgets
        # 3.1 Control buttons
        layout.addWidget(playButton, 1, 2)
        layout.addWidget(pauseButton, 1, 1)
        layout.addWidget(nextSongButton, 1, 3)
        layout.addWidget(previousSongButton, 1, 0)

        # 3.2
        layout.addWidget(volumeDownButton, 1, 4)
        layout.addWidget(volumeUpButton, 1, 5)

        # 3.3 Slider
        layout.addWidget(self.durationSlider)
        layout.addWidget(self.durationLabel)

        layout.addWidget(self.volumeSlider)

        # (Optioneel) Signalen verbinden (Signals & Slots)
        # Wanneer de duur van het bestand bekend is, voer de functie uit
        self.player.durationChanged.connect(self.update_duration)

        # 4. Update the slider position
        self.player.positionChanged.connect(self.durationSlider.setValue)

        # 5. Media laden (vervang met een echt bestand op jouw pc)
        self.player.setSource(QUrl.fromLocalFile("./songs/wiley.mp3"))
        self.player.play()

    def update_duration(self, duration_ms):
        """Deze functie wordt aangeroepen zodra durationChanged afvuurt."""
        # Zet de maximale waarde van de slider naar de totale duur in ms
        self.durationSlider.setMaximum(duration_ms)

        # Bereken seconden voor de tekst
        totale_seconden = duration_ms // 1000
        self.durationLabel.setText(f"Totale duur: {totale_seconden} seconden")

    def update_volume(self):
        self.volumeSlider.setMaximum(1.0)
        self.volumeSlider.setMinimum(0.0)


# app = QApplication(sys.argv)
# venster = MediaWindow()
# venster.show()
# sys.exit(app.exec())
