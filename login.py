import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QGraphicsDropShadowEffect, QSizePolicy, QStackedWidget)
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import os
from sqlConnector import connect
from employee import Ui_Dialog as EmployeePage  # Import Employee page
from owner import Ui_OwnerDialog as OwnerPage  # Import Owner page
from manager import Ui_Dialog as ManagerPage    # Import Manager page

class LoginForm(QWidget):
	def __init__(self, stacked_widget):
		super().__init__()
		self.stacked_widget = stacked_widget  # Reference to the QStackedWidget
		self.media_player = QMediaPlayer()  # Initialize the media player
		self.setWindowTitle('Login Form')
		self.resize(500, 120)
		self.setMinimumSize(400, 120)  # Set minimum window size

		# Set background image
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setBrush(QPalette.Window, QBrush(QPixmap("clwbeach.jpg")))
		self.setPalette(palette)

		# Create a container for the white box with modern styling
		container = QWidget(self)
		container.setStyleSheet("""
			background-color: white;
			border-radius: 15px;
			padding: 20px;
		""")
		# Set size policy to make container expand
		container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

		# Add shadow effect to the container
		shadow = QGraphicsDropShadowEffect()
		shadow.setBlurRadius(15)
		shadow.setOffset(0, 0)
		container.setGraphicsEffect(shadow)

		container_layout = QGridLayout(container)
		container_layout.setContentsMargins(20, 20, 20, 20)  # Add margins for better spacing

		label_name = QLabel('<font size="4"> Username </font>')
		self.lineEdit_username = QLineEdit()
		self.lineEdit_username.setPlaceholderText('Enter username')
		self.lineEdit_username.setStyleSheet("""
			border: 1px solid #ccc;
			border-radius: 10px;
			padding: 8px;
			font-size: 14px;
		""")
		container_layout.addWidget(label_name, 0, 0)
		container_layout.addWidget(self.lineEdit_username, 0, 1)

		label_password = QLabel('<font size="4"> Password </font>')
		self.lineEdit_password = QLineEdit()
		self.lineEdit_password.setPlaceholderText('Enter password')
		self.lineEdit_password.setEchoMode(QLineEdit.Password)
		self.lineEdit_password.setStyleSheet("""
			border: 1px solid #ccc;
			border-radius: 10px;
			padding: 8px;
			font-size: 14px;
		""")
		container_layout.addWidget(label_password, 1, 0)
		container_layout.addWidget(self.lineEdit_password, 1, 1)

		button_login = QPushButton('Login')
		button_login.setStyleSheet("""
			background-color: #007BFF;
			color: white;
			border: none;
			border-radius: 10px;
			padding: 10px 20px;
			font-size: 14px;
		""")
		button_login.clicked.connect(self.check_password)
		container_layout.addWidget(button_login, 2, 0, 1, 2, alignment=Qt.AlignCenter)
		container_layout.setRowMinimumHeight(2, 75)

		# Center the white box on the main layout
		main_layout = QGridLayout(self)
		main_layout.setContentsMargins(50, 50, 50, 50)  # Add margins for better spacing
		main_layout.addWidget(container, 0, 0, 1, 1, alignment=Qt.AlignCenter)
		main_layout.setRowStretch(0, 1)  # Make the row stretchable
		main_layout.setColumnStretch(0, 1)  # Make the column stretchable
		self.setLayout(main_layout)

	def play_error_audio(self):
		"""Play the error audio."""
		try:
			audio_path = os.path.abspath("wrong.mp4")  # Get absolute path
			if not os.path.exists(audio_path):
				print(f"Audio file not found: {audio_path}")
				return
			audio_url = QUrl.fromLocalFile(audio_path)
			self.media_player.setMedia(QMediaContent(audio_url))
			self.media_player.play()
			print(f"Playing error audio: {audio_path}")
		except Exception as e:
			print(f"Error playing audio: {e}")

	def check_password(self):
		msg = QMessageBox()

		# Query to check username and password
		query = "SELECT * FROM employee WHERE userName = %s AND password = %s"
		data = (self.lineEdit_username.text(), self.lineEdit_password.text())

		# Execute the query using the connect function
		results = connect(query, data)

		if results and len(results) > 0:
			# Debug: Print the query result to verify its structure
			print(f"Query Result: {results}")

			# Extract the employee_id and role
			self.employee_id = results[0][0]  # Assuming employee_id is the first column
			role = results[0][5]  # Assuming 'role' is the 6th column (0-based index)
			print(f"Login successful. Employee ID: {self.employee_id}, Role: {role}")  # Debug print
			msg.setText('Login Successful')
			msg.exec_()

			# Redirect based on role
			if role == 'owner':
				self.redirect_to_owner()
			elif role == 'manager':
				self.redirect_to_manager()
			elif role == 'employee':
				self.redirect_to_employee(self.employee_id)
		else:
			self.play_error_audio()  # Play error audio before showing the error message
			print("Invalid username or password.")  # Debug print
			msg.setText('Invalid Username or Password')
			msg.exec_()

	def redirect_to_employee(self, employee_id):
		print("Redirecting to Employee Page...")  # Debug print
		employee_page = QWidget()
		employee_ui = EmployeePage()
		employee_ui.setupUi(employee_page, self.stacked_widget, employee_id)  # Pass employee_id
		self.stacked_widget.addWidget(employee_page)
		self.stacked_widget.setCurrentWidget(employee_page)

	def redirect_to_owner(self):
		print("Redirecting to Owner Page...")  # Debug print
		owner_page = QWidget()
		owner_ui = OwnerPage()
		owner_ui.setupUi(owner_page, self.stacked_widget, self.employee_id)  # Pass both stacked_widget and employee_id
		self.stacked_widget.addWidget(owner_page)
		self.stacked_widget.setCurrentWidget(owner_page)

	def redirect_to_manager(self):
		print("Redirecting to Manager Page...")  # Debug print
		manager_page = QWidget()
		manager_ui = ManagerPage()
		manager_ui.setupUi(manager_page)
		self.stacked_widget.addWidget(manager_page)
		self.stacked_widget.setCurrentWidget(manager_page)

if __name__ == '__main__':
	app = QApplication(sys.argv)

	stacked_widget = QStackedWidget()
	form = LoginForm(stacked_widget)
	stacked_widget.addWidget(form)
	stacked_widget.show()

	sys.exit(app.exec_())