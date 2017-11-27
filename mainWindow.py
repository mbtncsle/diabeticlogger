from PyQt5.QtWidgets import QMdiArea, QApplication, QPushButton, QMainWindow, QAction
from PyQt5.QtCore import Qt
import sys
from InputWindow import InputWindow
from exercise import Exercise
from foodlist import Foodlist
from sleep import Sleep
from bloodglucose import Glucose

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__(parent = None)

		# Global variables
		self.blood_glucose = "BG"
		self.food_intake = "Food"
		self.sleep_hours = "Sleep"
		self.walk_steps = "Walk"

		self.window_width = 1200
		self.window_height = 700

		self.margin = 50

		self.sub_window_width = (self.window_width - self.margin) / 2
		self.sub_window_height = (self.window_height - self.margin) / 2

		# Prepare the main area
		self.mdi = QMdiArea()
		self.setCentralWidget(self.mdi)

		# Prepare the toolbar
		self.toolbar = self.addToolBar("Toolbar")
		self.toolbar.setMovable(False)

		# Create each toolbar action
		actions = [QAction("Blood Glucose", self),
		QAction("Food Intake", self),
		QAction("Hours of Sleep", self),
		QAction("Steps Walked", self),
		QAction("Notifications", self),
		QAction("Graph of all data", self)
		]

		# Setup the toolbar and actions
		for i in actions:
			self.toolbar.addAction(i)
			self.toolbar.insertSeparator(i)
		self.toolbar.insertSeparator(None)

		# Create each of the sub windows
		self.input_windows = {self.blood_glucose: Glucose(), self.food_intake: Foodlist(), self.sleep_hours: Sleep(), self.walk_steps: Exercise()}
		self.graph_windows = {self.blood_glucose: InputWindow(), self.food_intake: InputWindow(), self.sleep_hours: InputWindow(), self.walk_steps: InputWindow()}
		self.recommended_windows = {self.blood_glucose: InputWindow(), self.food_intake: InputWindow(), self.sleep_hours: InputWindow(), self.walk_steps: InputWindow()}
		self.log_windows = {self.blood_glucose: InputWindow(), self.food_intake: InputWindow(), self.sleep_hours: InputWindow(), self.walk_steps: InputWindow()}

		# Hide everything but the blood glucose and add it all to the main window
		for k in self.input_windows:
			self.mdi.addSubWindow(self.input_windows[k])
			self.mdi.addSubWindow(self.graph_windows[k])
			self.mdi.addSubWindow(self.recommended_windows[k])
			self.mdi.addSubWindow(self.log_windows[k])
			self.input_windows[k].setGeometry(0, 0, self.sub_window_width, self.sub_window_height)
			self.graph_windows[k].setGeometry(self.window_width - self.sub_window_width, 0, self.sub_window_width, self.sub_window_height)
			self.recommended_windows[k].setGeometry(0, self.window_height - self.sub_window_height, self.sub_window_width, self.sub_window_height)
			self.log_windows[k].setGeometry(self.window_width - self.sub_window_width, self.window_height - self.sub_window_height, self.sub_window_width, self.sub_window_height)
			if k != self.blood_glucose:
				self.input_windows[k].setVisible(False)
				self.graph_windows[k].setVisible(False)
				self.recommended_windows[k].setVisible(False)
				self.log_windows[k].setVisible(False)

		self.setGeometry(100, 30, self.window_width, self.window_height)
		self.show()

app = QApplication(sys.argv)
inp = MainWindow()
sys.exit(app.exec_())