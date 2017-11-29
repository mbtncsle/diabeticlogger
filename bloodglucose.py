import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateEdit, QPushButton, QMdiSubWindow, QTimeEdit
from PyQt5.QtCore import QTime
from datetime import datetime
from InputWindow import InputWindow

class Glucose(InputWindow):

	def __init__(self, parent):
		super(Glucose, self).__init__(parent)

		# Create the labels, setting their text, and their locations
		self.glucose_lbl = QLabel(self)
		self.glucose_lbl.setText("Please enter the blood glucose level")
		self.glucose_lbl.move(77.5, 27)
		self.glucose_lbl.adjustSize()

		self.error_lbl = QLabel(self)
		#self.error_lbl.setText("Incorrect input")
		self.error_lbl.move(325, 275)
                
		self.date_lbl = QLabel(self)
		self.date_lbl.setText("Please pick a date")
		self.date_lbl.move(450, 18)
		self.glucose_lbl.adjustSize()
		
		self.time_lbl = QLabel(self)
		self.time_lbl.setText("Please pick a time")
		self.time_lbl.move(450, 137)
		self.time_lbl.adjustSize()

		# Create the editing box
		self.glucose_qle = QLineEdit(self)
		self.glucose_qle.move(107.5, 40)

		# Create the date box
		self.date_qde = QDateEdit(self)
		self.date_qde.move(450, 40)

                #Creating the time box
		self.time = QTimeEdit(self)
		self.time.setDisplayFormat("hh:mm")
		self.time.setTime(QTime())
		self.time.move(450, 150)
		#self.time.adjustSize()

		# Create the submit button
		self.submit_qpb = QPushButton(self)
		self.submit_qpb.move(450, 280)
		self.submit_qpb.setText("Submit")
		self.submit_qpb.adjustSize()

		# Create the numpad buttons
		self.backspace_qpb = QPushButton(self)
		self.num_buttons = dict()
		self.backspace_qpb.setText("Backspace")
		self.backspace_qpb.move(107.5, 280)
		self.backspace_qpb.clicked.connect(self.delete)
		for i in range(0, 10):
			self.num_buttons["numpad" + str(i)] = QPushButton(self)
			self.num_buttons["numpad" + str(i)].setText(str(i))
			self.num_buttons["numpad" + str(i)].adjustSize()
			self.num_buttons['numpad' + str(i)].move(75*i, 0)
			self.num_buttons['numpad' + str(i)].clicked.connect(self.numbs)

		self.num_buttons['numpad' + str(0)].move(20, 40)
		self.num_buttons['numpad' + str(1)].move(40, 120)
		self.num_buttons['numpad' + str(2)].move(120, 120)
		self.num_buttons['numpad' + str(3)].move(200, 120)
		self.num_buttons['numpad' + str(4)].move(40, 160)
		self.num_buttons['numpad' + str(5)].move(120, 160)
		self.num_buttons['numpad' + str(6)].move(200, 160)
		self.num_buttons['numpad' + str(7)].move(40, 200)
		self.num_buttons['numpad' + str(8)].move(120, 200)
		self.num_buttons['numpad' + str(9)].move(200, 200)
		self.num_buttons['numpad' + str(0)].move(120, 240)

		# what happens when they press enter with the textbox selected
		self.glucose_qle.returnPressed.connect(self.submit)

		# The date of the date input, whether it has a calendar popup arrow and what date it is initialized to
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# What happens when the submit button is clicked
		self.submit_qpb.clicked.connect(self.submit)

		self.show()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.glucose_qle.setText(self.glucose_qle.text() + str(self.sender().text()))
		
	# Function for deleting the last number
	def delete(self):
		string = self.glucose_qle.text()
		if len(string) > 0:
			self.glucose_qle.setText(string[:-1])

	# Function for submitting data
	def submit(self):
		try:
			int(self.glucose_qle.text())
			self.error_lbl.setText("")
			super(Glucose, self).log_input(1, self.glucose_qle.text(), self.date_qde.date(), self.time.time())
		except Exception as e:
			self.error_lbl.setText("Invalid Input")
			self.error_lbl.adjustSize()