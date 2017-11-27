from PyQt5.QtWidgets import QMdiSubWindow, QPushButton, QDialog, QLabel
from PyQt5.QtCore import Qt
from datetime import datetime
import sys
sys.path.insert(0, "./database_files")
import blood_glucose_crud, meal_crud, meal_item_crud, sleep_crud, steps_crud

class InputWindow(QMdiSubWindow):
	
	def __init__(self):
		super(InputWindow, self).__init__(parent = None)
		
		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4

	# Log the given input
	def log_input(self, input_type, data, date, time):
		dt = datetime.strptime(date.toString("yyyy-MM-dd") + " " + time.toString("hh:mm") + ":00", "%Y-%m-%d %H:%M:%S")
		breakfast = 8
		lunch = 12
		dinner = 20
		if input_type == self.blood_glucose:
			hour = time.hour()
			if hour < breakfast:
				meal = "Before Breakfast"
			elif hour < (lunch + breakfast) / 2:
				meal = "After Breakfast"
			elif hour < lunch:
				meal = "Before Lunch"
			elif hour < (dinner + lunch) / 2:
				meal = "After Lunch"
			elif hour < dinner:
				meal = "Before Dinner"
			else:
				meal = "After Dinner"
			blood_glucose_crud.blood_glucose_insert(blood_glucose_crud.BloodGlucoseRecord(meal = meal, reading = int(data), record_date = dt))
		elif input_type == self.sleep:
			sleep_crud.sleep_insert(sleep_crud.SleepRecord(reading = int(data), record_date = dt))
		elif input_type == self.exercise:
			steps_crud.steps_insert(steps_crud.StepsRecord(reading = int(data), record_date = dt))
		else:
			hour = time.hour()
			if abs(hour - breakfast) <= 1:
				meal = "Breakfast"
			elif abs(hour - lunch) <= 1:
				meal = "Lunch"
			elif abs(hour - dinner) <= 1:
				meal = "Dinner"
			else:
				meal = "Snack"
			id = None
			for m in meal_crud.meal_select_by_days((datetime.now() - dt).days + 1):
				if m.record_date == dt:
					id = m.meal_id
					break
			if id == None:
				id = meal_crud.meal_insert(meal_crud.MealRecord(meal = meal, reading = int(data[0]) * int(data[1]), record_date = dt))
			meal_item_crud.meal_item_insert(meal_item_crud.MealItemRecord(meal_id = id, description = data[2], portions = int(data[0]), carbs_per_portion = int(data[1]), total_carbs = int(data[0]) * int(data[1])))
		note = QDialog()
		note_lbl = QLabel(note)
		note_button = QPushButton("Okay", note)
		note_lbl.setText("Data Submitted")
		note_lbl.adjustSize()
		note_button.move(0, 25)
		note_button.clicked.connect(note.accept)
		note.exec_()