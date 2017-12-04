from PyQt5.QtWidgets import QMdiSubWindow, QPushButton, QDialog, QLabel, QLineEdit, QDateEdit, QTimeEdit
from PyQt5.QtCore import Qt, pyqtSlot, QTime
from datetime import datetime
import sys
sys.path.insert(0, "./database_files")
import blood_glucose_crud, meal_crud, meal_item_crud, sleep_crud, steps_crud

class InputWindow(QMdiSubWindow):
	
	def __init__(self, parent, main_text):
		super(InputWindow, self).__init__(parent = None)

		self.parent = parent
		
		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4

		self.setFocusPolicy(Qt.NoFocus)

		# Create the labels, setting their text, and their locations
		self.main_lbl = QLabel(self)
		self.main_lbl.setText(main_text)
		self.main_lbl.adjustSize()

		self.error_lbl = QLabel(self)
		#self.error_lbl.setText("Incorrect input")

		self.date_lbl = QLabel(self)
		self.date_lbl.setText("Please pick a date")
		self.date_lbl.adjustSize()
		
		self.time_lbl = QLabel(self)
		self.time_lbl.setText("Please pick a time")
		self.time_lbl.adjustSize()

		# Create the editing box
		self.main_qle = QLineEdit(self)

		# Create the date box
		self.date_qde = QDateEdit(self)

		# Create the submit button
		self.submit_qpb = QPushButton(self)
		self.submit_qpb.setText("Submit")

		# Create the numpad buttons
		self.backspace_qpb = QPushButton(self)
		self.num_buttons = dict()
		self.backspace_qpb.setText("Del")
		self.backspace_qpb.clicked.connect(self.delete)
		for i in range(0, 10):
			self.num_buttons["numpad" + str(i)] = QPushButton(self)
			self.num_buttons["numpad" + str(i)].setText(str(i))
			self.num_buttons['numpad' + str(i)].setGeometry(40, 40, 40, 40)
			self.num_buttons['numpad' + str(i)].clicked.connect(self.numbs)

		self.num_buttons['numpad' + str(1)].move(100, 90)
		self.num_buttons['numpad' + str(2)].move(140, 90)
		self.num_buttons['numpad' + str(3)].move(180, 90)
		self.num_buttons['numpad' + str(4)].move(100, 130)
		self.num_buttons['numpad' + str(5)].move(140, 130)
		self.num_buttons['numpad' + str(6)].move(180, 130)
		self.num_buttons['numpad' + str(7)].move(100, 170)
		self.num_buttons['numpad' + str(8)].move(140, 170)
		self.num_buttons['numpad' + str(9)].move(180, 170)
		self.num_buttons['numpad' + str(0)].setGeometry(40, 40, 80, 40)
		self.num_buttons['numpad' + str(0)].move(100, 210)



		# what happens when they press enter with the textbox selected
		self.main_qle.returnPressed.connect(self.submit)

		# The date of the date input, whether it has a calendar popup arrow and what date it is initialized to
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# What happens when the submit button is clicked
		self.submit_qpb.clicked.connect(self.submit)

		self.time = QTimeEdit(self)
		self.time.setDisplayFormat("hh:mm")
		self.time.setTime(QTime())
		#self.time.adjustSize()

		self.error_lbl = QLabel(self)

		self.main_lbl.move(100, 30)
		self.date_lbl.move(290, 195)
		self.time_lbl.move(293, 115)
		self.main_qle.setGeometry(100, 45, 120, 40)
		self.date_qde.setGeometry(275, 210, 120, 40)
		self.submit_qpb.setGeometry(0, 294.5, 504, 30)
		self.backspace_qpb.setGeometry(180, 210, 40, 40)
		self.time.setGeometry(275, 130, 120, 40)
		self.error_lbl.move(255, 85)

	@pyqtSlot()
	def numbs(self):
		self.main_qle.setText(self.main_qle.text() + str(self.sender().text()))

	# Function for deleting the last number
	def delete(self):
		string = self.main_qle.text()
		if len(string) > 0:
			self.main_qle.setText(string[:-1])

	# Log the given input
	def log_input(self, input_type, data):
		dt = datetime.strptime(self.date_qde.date().toString("yyyy-MM-dd") + " " + self.time.time().toString("hh:mm") + ":00", "%Y-%m-%d %H:%M:%S")
		breakfast = 8
		lunch = 12
		dinner = 20
		if input_type == self.blood_glucose:
			blood_glucose_crud.blood_glucose_insert(blood_glucose_crud.BloodGlucoseRecord(meal = data[0], reading = int(self.main_qle.text()), record_date = dt))
		elif input_type == self.sleep:
			sleep_crud.sleep_insert(sleep_crud.SleepRecord(reading = int(self.main_qle.text()), record_date = dt))
		elif input_type == self.exercise:
			steps_crud.steps_insert(steps_crud.StepsRecord(reading = int(self.main_qle.text()), record_date = dt))
		else:
			id = None
			for m in meal_crud.meal_select_by_days((datetime.now() - dt).days + 1):
				if m.record_date == dt:
					id = m.meal_id
					break
			if id == None:
				id = meal_crud.meal_insert(meal_crud.MealRecord(meal = data[2], reading = int(self.main_qle.text()) * int(data[0]), record_date = dt))
			meal_item_crud.meal_item_insert(meal_item_crud.MealItemRecord(meal_id = id, description = data[1], portions = int(self.main_qle.text()), carbs_per_portion = int(data[0]), total_carbs = int(self.main_qle.text()) * int(data[0])))
		self.parent.update_data()
		note = QDialog()
		note_lbl = QLabel(note)
		note_button = QPushButton("Okay", note)
		note_lbl.setText("Data Submitted")
		note_lbl.adjustSize()
		note_button.move(0, 25)
		note_button.clicked.connect(note.accept)
		note.exec_()