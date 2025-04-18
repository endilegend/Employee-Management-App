# lebron.py  – sign‑out order fixed
import os
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtCore import QUrl


class Ui_LebronDialog(object):
    def setupUi(self, Dialog, stacked_widget):
        self.Dialog = Dialog
        self.stacked_widget = stacked_widget
        Dialog.setObjectName("LebronDialog")
        Dialog.resize(900, 600)

        # -------- layout --------
        layout = QtWidgets.QVBoxLayout(Dialog)
        self.videoWidget = QtMultimediaWidgets.QVideoWidget(Dialog)
        layout.addWidget(self.videoWidget)
        self.btnSignOut = QtWidgets.QPushButton("Sign Out")
        self.btnSignOut.setFixedHeight(40)
        layout.addWidget(self.btnSignOut, alignment=QtCore.Qt.AlignCenter)

        # -------- media player --------
        self.player = QtMultimedia.QMediaPlayer(Dialog)
        self.player.setVideoOutput(self.videoWidget)
        video_path = os.path.abspath("lebron.mp4")
        self.player.setMedia(QtMultimedia.QMediaContent(QUrl.fromLocalFile(video_path)))
        QtCore.QTimer.singleShot(0, self.player.play)
        self.player.setVolume(80)

        # connect
        self.btnSignOut.clicked.connect(self.sign_out)

    # ---------------- sign‑out (new) ----------------
    def sign_out(self):
        """Return to login screen and clean up the video page."""
        self.player.stop()

        # Ensure the login widget is correctly referenced
        login_widget = self.stacked_widget.widget(0)  # First widget is the login screen

        # Remove THIS page from the stack and delete it
        self.stacked_widget.removeWidget(self.Dialog)
        self.Dialog.deleteLater()  # Free resources

        # Redirect to the login screen
        self.stacked_widget.setCurrentWidget(login_widget)
        print("Redirected to login screen.")  # Debug print
