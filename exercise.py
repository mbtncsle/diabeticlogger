import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateEdit, QPushButton, QMdiSubWindow, QTimeEdit
from PyQt5.QtCore import QTime, Qt
from datetime import datetime
from InputWindow import InputWindow

class Exercise(InputWindow):

	def __init__(self, parent):
		super(Exercise, self).__init__(parent)

		self.setFocusPolicy(Qt.NoFocus)

		# Create the labels, setting their text, and their locations
		self.step_lbl = QLabel(self)
		self.step_lbl.setText("Please enter the number of steps")
		self.step_lbl.adjustSize()

		self.error_lbl = QLabel(self)
		#self.error_lbl.setText("Incorrect input")

		self.date_lbl = QLabel(self)
		self.date_lbl.setText("Please pick a date")
		self.step_lbl.adjustSize()
		
		self.time_lbl = QLabel(self)
		self.time_lbl.setText("Please pick a time")
		self.time_lbl.adjustSize()

		# Create the editing box
		self.step_qle = QLineEdit(self)

		# Create the date box
		self.date_qde = QDateEdit(self)

		# Create the submit button
		self.submit_qpb = QPushButton(self)
		self.submit_qpb.setText("Submit")

		# Create the numpad buttons
		self.backspace_qpb = QPushButton(self)
		self.num_buttons = dict()
		self.backspace_qpb.setText("Backspace")
		self.backspace_qpb.clicked.connect(self.delete)

		for i in range(0, 10):
			self.num_buttons["numpad" + str(i)] = QPushButton(self)
			self.num_buttons["numpad" + str(i)].setText(str(i))
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
		self.step_qle.returnPressed.connect(self.submit)

		# The date of the date input, whether it has a calendar popup arrow and what date it is initialized to
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# What happens when the submit button is clicked
		self.submit_qpb.clicked.connect(self.submit)

		self.time = QTimeEdit(self)
		self.time.setDisplayFormat("hh:mm")
		self.time.setTime(QTime())
		self.time.setGeometry(275, 130, 120, 40)
		#self.time.adjustSize()

		self.show()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.step_qle.setText(self.step_qle.text() + str(self.sender().text()))

	# Function for deleting the last number
	def delete(self):
		string = self.step_qle.text()
		if len(string) > 0:
			self.step_qle.setText(string[:-1])

	# Function for submitting data
	def submit(self):
		try:
			int(self.step_qle.text())
			self.error_lbl.setText("")
			super(Exercise, self).log_input(3, self.step_qle.text(), self.date_qde.date(), self.time.time())
		except Exception as e:
			self.error_lbl.setText("Invalid input")
			self.error_lbl.adjustSize()
