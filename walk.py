'''
This is a very simple window for logging steps
It doesn't do a lot or look like a lot and it doesn't even take in time, but only date
It does, however, take in the number of steps on a particular date and store that information in a file with a very simple formatting system
'''

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication, QPushButton)
from datetime import datetime
from functools import partial

class Exercise(QWidget):

	FILE_NAME = "log.txt"

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# Create the labels (one for the steps and one for errors)
		self.step_lbl = QLabel(self)
		self.error_lbl = QLabel(self)

		# Create the editing box (one for the steps)
		self.step_qle = QLineEdit(self)

		# Create the submit button
		self.qpb = QPushButton(self)

		# Create the numpad buttons
		self.backspace = QPushButton(self)
		self.numpad = []
		for i in range(0, 10):
			self.numpad.append(QPushButton(self))

		# Move the labels and set their text
		self.step_lbl.move(60, 80)
		self.step_lbl.setText("Enter number of steps")
		self.step_lbl.adjustSize()
		self.error_lbl.move(60, 140)

		# Move the editing box and setup the return signal
		self.step_qle.move(60, 100)
		self.step_qle.returnPressed.connect(self.submit)

		# Move the button, set the text and prepare an event for when clicked
		self.qpb.move(60, 120)
		self.qpb.setText("Submit")
		self.qpb.adjustSize()
		self.qpb.clicked.connect(self.submit)

		# Move the numpad, set all the buttons' text and prepare events for being clicked
		self.backspace.move(280, 180)
		self.backspace.setText("Backspace")
		self.backspace.adjustSize()
		self.backspace.clicked.connect(self.delete)
		x = 200
		y = 60
		for i in range(1, 11):
			if i == 10:
				i, x, y = 0, 280, 150
			self.numpad[i].move(x, y)
			self.numpad[i].setText(str(i))
			self.numpad[i].adjustSize()
			self.numpad[i].clicked.connect(partial(self.numbs, i))
			if i == 0:
				break
			x += 80
			if i % 3 == 0:
				x = 200
				y += 30

		# Prepare the actual window
		self.setGeometry(300, 300, 500, 300)
		self.setWindowTitle("Exercise Window")
		self.show()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.step_qle.setText(self.step_qle.text() + str(number))

	# Function for deleting the last number
	def delete(self):
		string = self.step_qle.text()
		if len(string) > 0:
			self.step_qle.setText(string[:-1])

	# Function for when the button was clicked
	def submit(self):
		# Get the text from the editing box
		temp_steps = self.step_qle.text()
		if len(temp_steps) == 0:
			temp_steps = "0"
		try:
			# Ensure that the format of the text is correct
			steps = int(temp_steps)

			# If all is well then clear the error label and write the values to a log file
			self.error_lbl.setText("")
			f = open(self.FILE_NAME, "a")
			f.write(temp_steps + "," + str(datetime.now()) + "\n")
			f.close()
		except Exception as e:
			# If any issues arise then set the error label because it should only be caused by bad formatting in the editing boxes
			self.error_lbl.setText("Error, incorrect input")
			self.error_lbl.adjustSize()

# Start up the whole thing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Exercise()
    sys.exit(app.exec_())