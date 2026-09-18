from PySide6.QtCore import Slot


@Slot()
def play_music():
    print("Music started playing")


@Slot()
def stop_music():
    print("Music stopped playing")


@Slot()
def next_song():
    print("Next song started playing")


@Slot()
def previous_song():
    print("Previous song started playing")
