import sys
from PySide6.QtWidgets import QApplication
from mediaWindow import MediaWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaWindow()
    window.show()
    app.exec()
