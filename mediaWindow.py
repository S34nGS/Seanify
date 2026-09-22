from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtCore import QUrl, Qt, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from PySide6.QtWidgets import QMainWindow, QLabel, QSlider, QGridLayout, QWidget, QPushButton, QListWidget, QListWidgetItem


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
        # 2.0 Library
        self.songList = QListWidget()
        layout.addWidget(self.songList, 0, 5, 4, 2)
        songs_path = Path("/Users/seansteenhuis/Documents/Music/Songs")

        for song_path in songs_path.iterdir():
            if song_path.is_file() and song_path.suffix.lower() in {".mp3", ".wav", ".m4a", ".flac"}:
                item = QListWidgetItem(song_path.stem)
                item.setData(Qt.ItemDataRole.UserRole, str(song_path))
                self.songList.addItem(item)

        self.songList.itemDoubleClicked.connect(self.play_selected_song)

        # 2.1 Player
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.volumeLevel = 0.5
        self.audioOutput.setVolume(self.volumeLevel)

        # 2.2 Sliders
        # 2.2.1 Duration slider
        self.durationSlider = QSlider(Qt.Orientation.Horizontal)
        self.durationSlider.setRange(0, 0)

        self.player.positionChanged.connect(self.update_slider_position)
        self.player.durationChanged.connect(self.update_duration_range)

        self.durationSlider.sliderMoved.connect(self.change_duration)

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
        self.playButton = QPushButton()
        self.playButton.setIcon(QIcon("images/controls/play.png"))
        self.playButton.clicked.connect(playMusic)

        self.pauseButton = QPushButton()
        self.pauseButton.setIcon(QIcon("images/controls/pause.png"))
        self.pauseButton.clicked.connect(pauseMusic)

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

        self.playButton.setFixedSize(*button_size)
        self.pauseButton.setFixedSize(*button_size)
        nextSongButton.setFixedSize(*button_size)
        previousSongButton.setFixedSize(*button_size)

        # 2.4 Metadata
        # 2.4.1 Title
        self.titleLabel = QLabel("Loading title...")
        self.player.metaDataChanged.connect(self.update_title)

        # 2.4.2 Artist
        self.artistLabel = QLabel("Loading artist...")
        self.player.metaDataChanged.connect(self.update_artist)

        # 3. Adding widgets
        # 3.1 Control buttons
        self.player.playbackStateChanged.connect(self.update_play_button)
        layout.addWidget(self.playButton, 1, 1)
        layout.addWidget(self.pauseButton, 1, 1)

        layout.addWidget(nextSongButton, 1, 2)
        layout.addWidget(previousSongButton, 1, 0)

        # 3.2 Slider
        layout.addWidget(self.durationSlider, 2, 0, 1, 3)

        layout.addWidget(self.volumeSlider, 1, 4, 2, 1)

        # 3.3 Metadata
        # 3.3.1 Title
        layout.addWidget(self.titleLabel)

        # 3.3.2 Artist
        layout.addWidget(self.artistLabel)

        # 3.4 Duration in numbers
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

    def play_selected_song(self, item):
        song_path = item.data(Qt.ItemDataRole.UserRole)

        self.player.setSource(QUrl.fromLocalFile(song_path))
        self.player.play()

    def update_play_button(self, state):
        is_playing = state == QMediaPlayer.PlaybackState.PlayingState

        self.playButton.setVisible(not is_playing)
        self.pauseButton.setVisible(is_playing)

    def update_title(self):
        title = self.player.metaData().value(QMediaMetaData.Title)
        if title:
            self.titleLabel.setText(str(title))
        else:
            self.titleLabel.setText("Unknown title")

    def update_artist(self):
        artistName = self.player.metaData().value(QMediaMetaData.ContributingArtist)
        if artistName:
            self.artistLabel.setText(str(artistName).strip("[]'"))
        else:
            self.artistLabel.setText("Unknown artist")

    def update_duration_range(self, duration_ms):
        self.durationSlider.setRange(0, duration_ms)

    def update_slider_position(self, position_ms):
        if not self.durationSlider.isSliderDown():
            self.durationSlider.setValue(position_ms)

    def change_duration(self, value):
        self.player.setPosition(value)

    def change_volume(self, volumeValue):
        self.volumeLevel = volumeValue / 100
        self.audioOutput.setVolume(self.volumeLevel)
        print(f"Current volume: {self.volumeLevel}")
