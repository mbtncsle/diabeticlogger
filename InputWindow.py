from PyQt5.QtWidgets import QMdiSubWindow, QApplication, QPushButton, QCalendarWidget, QVBoxLayout, QHBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from datetime import datetime
import sys

class InputWindow(QMdiSubWindow):
	
	def __init__(self):
		super(InputWindow, self).__init__(parent = None)
		
		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

	# Log the given input
	def log_input(self):
		pass