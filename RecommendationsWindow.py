from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt
import sys

class RecommendationsWindow(QMdiSubWindow):

	def __init__(self):
		super(RecommendationsWindow, self).__init__(parent = None)

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		self.show()

	# Get recommendation and show it
	def update(self):
		pass