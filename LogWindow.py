from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QScrollArea, QLabel, QFrame
from PyQt5.QtCore import Qt
import sys
sys.path.insert(0, "./database_files")
import blood_glucose_crud, meal_crud, meal_item_crud, sleep_crud, steps_crud

class LogWindow(QMdiSubWindow):

	def __init__(self):
		super(LogWindow, self).__init__(parent = None)

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4
		self.data = self.blood_glucose

		self.scrollarea = QScrollArea(self)
		self.scrollarea.setWidgetResizable(True)
		self.frame = QFrame(self.scrollarea)
		self.frame.setLayout(QVBoxLayout())
		self.scrollarea.setWidget(self.frame)
		self.scrollarea.setGeometry(0, 0, 550, 250)

		self.update()

		self.show()

	# Change which data logs are shown
	def change_data(self, data):
		self.data = data
		self.update()

	# Get logs and show them
	def update(self):
		for i in reversed(range(self.frame.layout().count())): 
			self.frame.layout().itemAt(i).widget().setParent(None)

		if self.data == self.blood_glucose:
			for log in blood_glucose_crud.blood_glucose_select_by_days(30):
				self.frame.layout().addWidget(QLabel(log.meal + " blood glucose level was " + str(log.reading) + " on " + log.record_date.strftime("%Y-%m-%d %H:%M:%S")))
		elif self.data == self.food_list:
			for log in meal_crud.meal_select_by_days(30):
				st = ""
				total_carbs = 0
				for m in log.meal_items:
					st += m.description + ", "
					total_carbs += m.total_carbs
				st = st[:-2]
				self.frame.layout().addWidget(QLabel(log.meal + " was " + st + " at " + str(total_carbs) + " carbs on " + log.record_date.strftime("%Y-%m-%d %H:%M:%S")))
		elif self.data == self.sleep:
			for log in sleep_crud.sleep_select_by_days(30):
				self.frame.layout().addWidget(QLabel(str(log.reading) + " hours of sleep on " + log.record_date.strftime("%Y-%m-%d %H:%M:%S")))
		else:
			for log in steps_crud.steps_select_by_days(30):
				self.frame.layout().addWidget(QLabel(str(log.reading) + " steps walked on " + log.record_date.strftime("%Y-%m-%d %H:%M:%S")))