from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt
import sys

class GraphWindow(QMdiSubWindow):

	def __init__(self):
		super(GraphWindow, self).__init__(parent = None)

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4
		self.data = self.blood_glucose

		self.update()

		self.show()

	# Change which data is graphed
	def change_data(data):
		self.data = data

	# Get data and graph it
	def update(self):
		pass