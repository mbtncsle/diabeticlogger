from PyQt5.QtWidgets import QMdiSubWindow, QApplication, QPushButton, QCalendarWidget, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from datetime import datetime
import sys

class InputWindow(QMdiSubWindow):
	
	def __init__(self):
		super(InputWindow, self).__init__(parent = None)

		# Setup the submit button
		self.submit_button = QPushButton()
		self.submit_button.setText("Submit")
		self.submit_button.adjustSize()
		self.submit_button.clicked.connect(self.log_input)

		# Setup the calendar
		self.calendar = QCalendarWidget()

		# Main space for widgets
		self.inner_space = QGridLayout()

		self.add_widget(self.calendar, 20, 0)
		self.add_widget(self.submit_button, 20, 20)
		for i in range(0, 22):
			self.inner_space.setColumnStretch(i, 2)
			self.inner_space.setRowStretch(i, 1)

	# Allow adding of widgets
	def add_widget(self, widget, x, y, spanx = 1, spany = 1):
		self.inner_space.addWidget(widget, y, x, spany, spanx)

	# Prepare and show the window
	def make_window(self):

		# Prepare the layout
		wid = QWidget()

		wid.setLayout(self.inner_space)

		self.setWidget(wid)

		# Prepare and show window
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.show()

	# Log the given input
	def log_input(self):
		pass