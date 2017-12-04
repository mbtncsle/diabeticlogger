import sys
from PyQt5.QtWidgets import QLabel, QLineEdit, QDateEdit, QPushButton, QMdiSubWindow, QTimeEdit
from PyQt5.QtCore import QTime, Qt
from datetime import datetime
from InputWindow import InputWindow

class Sleep(InputWindow):

	def __init__(self, parent):
		super(Sleep, self).__init__(parent)

		self.setFocusPolicy(Qt.NoFocus)

		# Create the labels, setting their text, and their locations
		self.sleep_lbl = QLabel(self)
		self.sleep_lbl.setText("Please enter the hours of sleep")
		self.sleep_lbl.adjustSize()

		self.error_lbl = QLabel(self)
		#self.error_lbl.setText("Incorrect input")
		self.error_lbl.move(325, 275)
                
		self.date_lbl = QLabel(self)
		self.date_lbl.setText("Please pick a date")
		self.sleep_lbl.adjustSize()
		
		self.time_lbl = QLabel(self)
		self.time_lbl.setText("Please pick a time")
		self.time_lbl.adjustSize()

		# Create the editing box
		self.sleep_qle = QLineEdit(self)

		# Create the date box
		self.date_qde = QDateEdit(self)

                #Creating the time box
		self.time = QTimeEdit(self)
		self.time.setDisplayFormat("hh:mm")
		self.time.setTime(QTime())
		#self.time.adjustSize()

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
		self.sleep_qle.returnPressed.connect(self.submit)

		# The date of the date input, whether it has a calendar popup arrow and what date it is initialized to
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# What happens when the submit button is clicked
		self.submit_qpb.clicked.connect(self.submit)

		self.sleep_lbl.setGeometry(115, 30, 25, 25)
		self.date_lbl.setGeometry(290, 195, 25, 25)
		self.time_lbl.setGeometry(293, 115, 25, 25)
		self.sleep_qle.setGeometry(100, 45, 120, 40)
		self.date_qde.setGeometry(275, 210, 120, 40)
		self.submit_qpb.setGeometry(0, 294.5, 504, 30)
		self.backspace_qpb.setGeometry(180, 210, 40, 40)
		self.time.setGeometry(275, 130, 120, 40)

		self.show()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.sleep_qle.setText(self.sleep_qle.text() + str(self.sender().text()))

	# Function for deleting the last number
	def delete(self):
		string = self.sleep_qle.text()
		if len(string) > 0:
			self.sleep_qle.setText(string[:-1])

	# Function for submitting data
	def submit(self):
		try:
			int(self.sleep_qle.text())
			self.error_lbl.setText("")
			super(Sleep, self).log_input(2, self.sleep_qle.text(), self.date_qde.date(), self.time.time())
		except Exception as e:
			self.error_lbl.setText("Invalid Input")
			self.error_lbl.adjustSize()