import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateEdit, QPushButton, QMdiSubWindow
from datetime import datetime
from InputWindow import InputWindow

class Exercise(InputWindow):

	def __init__(self):
		super(Exercise, self).__init__()

		# Create the labels
		self.step_lbl = QLabel(self)
		self.error_lbl = QLabel(self)
		self.date_lbl = QLabel(self)

		# Create the editing box
		self.step_qle = QLineEdit(self)

		# Create the date box
		self.date_qde = QDateEdit(self)

		# Create the submit button
		self.submit_qpb = QPushButton(self)

		# Create the numpad buttons
		self.backspace_qpb = QPushButton(self)
		self.num_buttons = dict()
		for i in range(0, 10):
			self.num_buttons["numpad" + str(i)] = QPushButton(self)

		# what happens when they press enter with the textbox selected
		self.step_qle.returnPressed.connect(self.submit)

		# The date of the date input, whether it has a calendar popup arrow and what date it is initialized to
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# What happens when the submit button is clicked
		self.submit_qpb.clicked.connect(self.submit)

		self.show()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.step_qle.setText(self.step_qle.text() + str(number))
		self.step_qle.adjustSize()

	# Function for deleting the last number
	def delete(self):
		string = self.step_qle.text()
		if len(string) > 0:
			self.step_qle.setText(string[:-1])
			self.step_qle.adjustSize()

	# Function for submitting data
	def submit(self):
		super(Exercise, self).log_input()