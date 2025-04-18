import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QLineEdit,
    QGridLayout, QMessageBox, QGraphicsDropShadowEffect,
    QSizePolicy, QStackedWidget
)
from PyQt5.QtGui    import QPalette, QBrush, QPixmap
from PyQt5.QtCore   import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

from sqlConnector import connect

# page modules
from employee import Ui_Dialog        as EmployeePage
from owner    import Ui_OwnerDialog   as OwnerPage
from manager  import Ui_ManagerDialog as ManagerPage  # Updated class name
from lebron   import Ui_LebronDialog  as LebronPage   # special page


class LoginForm(QWidget):
    def __init__(self, stacked_widget: QStackedWidget):
        super().__init__()
        self.stacked_widget = stacked_widget          # reference to the global QStackedWidget
        self.media_player = QMediaPlayer()            # for error‑sound playback

        # ---------- basic window ----------
        self.setWindowTitle('Login Form')
        self.resize(500, 120)
        self.setMinimumSize(400, 120)

        # ---------- background image ----------
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("clwbeach.jpg")))
        self.setPalette(palette)

        # ---------- white rounded box ----------
        container = QWidget(self)
        container.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 20px;
        """)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 0)
        container.setGraphicsEffect(shadow)

        # ---------- form layout ----------
        container_layout = QGridLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)

        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Enter username')
        self.lineEdit_username.setStyleSheet(
            "border: 1px solid #ccc; border-radius: 10px; padding: 8px; font-size: 14px;"
        )

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Enter password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        self.lineEdit_password.setStyleSheet(
            "border: 1px solid #ccc; border-radius: 10px; padding: 8px; font-size: 14px;"
        )

        button_login = QPushButton('Login')
        button_login.setStyleSheet(
            "background-color: #007BFF; color: white; border: none; "
            "border-radius: 10px; padding: 10px 20px; font-size: 14px;"
        )
        button_login.clicked.connect(self.check_password)

        # add to layout
        container_layout.addWidget(label_name,        0, 0)
        container_layout.addWidget(self.lineEdit_username, 0, 1)
        container_layout.addWidget(label_password,    1, 0)
        container_layout.addWidget(self.lineEdit_password, 1, 1)
        container_layout.addWidget(button_login,      2, 0, 1, 2, alignment=Qt.AlignCenter)
        container_layout.setRowMinimumHeight(2, 75)

        # ---------- main layout (centering) ----------
        main_layout = QGridLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.addWidget(container, 0, 0, alignment=Qt.AlignCenter)
        main_layout.setRowStretch(0, 1)
        main_layout.setColumnStretch(0, 1)
        self.setLayout(main_layout)

        # place to store employee_id after DB lookup
        self.employee_id = None

    # ------------------------------------------------------------------
    # utilities
    # ------------------------------------------------------------------
    def play_error_audio(self):
        """Plays wrong.mp4 when login fails."""
        audio_path = os.path.abspath("wrong.mp4")
        if os.path.exists(audio_path):
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
            self.media_player.play()

    # ------------------------------------------------------------------
    # login logic
    # ------------------------------------------------------------------
    def check_password(self):
        """Validates credentials and routes to the proper page."""
        # ----- 1) hard‑coded “lebron” backdoor -------------------------
        if (self.lineEdit_username.text() == "lebron" and
                self.lineEdit_password.text() == "123084"):
            self.redirect_to_lebron()
            return

        # ----- 2) normal DB lookup ------------------------------------
        query = "SELECT * FROM employee WHERE userName = %s AND password = %s"
        data  = (self.lineEdit_username.text(), self.lineEdit_password.text())
        results = connect(query, data)

        if results:
            # assuming columns: employee_id, firstName, lastName, userName, password, role, ...
            self.employee_id = results[0][0]
            role             = results[0][5]          # change index if schema differs

            QMessageBox.information(self, "Login", "Login Successful")

            if role == 'owner':
                self.redirect_to_owner()
            elif role == 'manager':
                self.redirect_to_manager()
            elif role == 'employee':
                self.redirect_to_employee()
            else:
                QMessageBox.warning(self, "Login Error", f"Unknown role: {role}")
        else:
            self.play_error_audio()
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    # ------------------------------------------------------------------
    # routing helpers
    # ------------------------------------------------------------------
    def redirect_to_employee(self):
        page = QWidget()
        ui   = EmployeePage()
        ui.setupUi(page, self.stacked_widget, self.employee_id)  # pass employee_id
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def redirect_to_owner(self):
        page = QWidget()
        ui   = OwnerPage()
        ui.setupUi(page, self.stacked_widget, self.employee_id)  # pass employee_id
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def redirect_to_manager(self):
        page = QWidget()
        ui   = ManagerPage()
        ui.setupUi(page)                            # manager page needed no extras
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)

    def redirect_to_lebron(self):
        """Opens the special Lebron video page."""
        page = QWidget()
        ui   = LebronPage()
        ui.setupUi(page, self.stacked_widget)       # Lebron page only needs the stack
        self.stacked_widget.addWidget(page)
        self.stacked_widget.setCurrentWidget(page)


# ----------------------------------------------------------------------
# main entry‑point
# ----------------------------------------------------------------------
if __name__ == '__main__':
    app = QApplication(sys.argv)

    stacked_widget = QStackedWidget()
    login_form = LoginForm(stacked_widget)

    stacked_widget.addWidget(login_form)  # index 0 = login page
    stacked_widget.show()

    sys.exit(app.exec_())
