from PyQt5.QtWidgets import QMdiArea, QApplication, QPushButton, QMainWindow, QAction
from PyQt5.QtCore import Qt
import sys
from InputWindow import InputWindow
from exercise import Exercise
from foodlist import Foodlist
from sleep import Sleep
from bloodglucose import Glucose
from RecommendationsWindow import RecommendationsWindow
from GraphWindow import GraphWindow
from LogWindow import LogWindow
sys.path.insert(0, "./database_files")
import blood_glucose_crud

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

		self.setWindowTitle("Diabetic Logger        A1C Level: " + str(round(self.get_a1c(), 2)))

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
		self.toolbar.actionTriggered[QAction].connect(self.tool_button_pressed)

		# Create each of the sub windows
		self.input_windows = {self.blood_glucose: Glucose(self), self.food_intake: Foodlist(self), self.sleep_hours: Sleep(self), self.walk_steps: Exercise(self)}
		self.graph_window = GraphWindow()
		self.recommended_window = RecommendationsWindow()
		self.log_window = LogWindow(self)

		# Hide everything but the blood glucose and add it all to the main window
		self.mdi.addSubWindow(self.graph_window)
		self.mdi.addSubWindow(self.recommended_window)
		self.mdi.addSubWindow(self.log_window)
		self.graph_window.setGeometry(self.window_width - self.sub_window_width, 0, self.sub_window_width, self.sub_window_height)
		self.recommended_window.setGeometry(0, self.window_height - self.sub_window_height, self.sub_window_width, self.sub_window_height)
		self.log_window.setGeometry(self.window_width - self.sub_window_width, self.window_height - self.sub_window_height, self.sub_window_width, self.sub_window_height)
		for k in self.input_windows:
			self.mdi.addSubWindow(self.input_windows[k])
			self.input_windows[k].setGeometry(0, 0, self.sub_window_width, self.sub_window_height)
			if k != self.blood_glucose:
				self.input_windows[k].setVisible(False)

		self.setGeometry(100, 30, self.window_width, self.window_height)
		self.show()

	# determine the a1c
	def get_a1c(self):
		total = 0
		logs = blood_glucose_crud.blood_glucose_select_by_days(30)
		for log in logs:
			total += log.reading
		total /= len(logs)
		return total

	# update the windows with new data
	def update_data(self):
		self.setWindowTitle("Diabetic Logger        A1C Level: " + str(round(self.get_a1c(), 2)))
		self.graph_window.update()
		#self.recommended_window.update()
		self.log_window.update()

	def tool_button_pressed(self, button):
		bt = button.text()
		num = 0
		if bt == "Blood Glucose":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.blood_glucose].setVisible(True)
			num = 1
		elif bt == "Hours of Sleep":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.sleep_hours].setVisible(True)
			num = 2
		elif bt == "Steps Walked":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.walk_steps].setVisible(True)
			num = 3
		elif bt == "Food Intake":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.food_intake].setVisible(True)
			num = 4
		if num != 0:
			self.graph_window.change_data(num)
			self.log_window.change_data(num)

app = QApplication(sys.argv)
inp = MainWindow()
sys.exit(app.exec_())