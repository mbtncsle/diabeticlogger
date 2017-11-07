'''
This is a very simple window for logging steps
It doesn't do a lot or look like a lot and it doesn't even take in time, but only date
It does, however, take in the number of steps on a particular date and store that information in a file with a very simple formatting system
'''

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication, QPushButton, QDateEdit)
from datetime import datetime
from functools import partial

class Exercise(QWidget):

	FILE_NAME = "log.txt"

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# Create the labels
		self.step_lbl = QLabel(self)
		self.error_lbl = QLabel(self)
		self.date_lbl = QLabel(self)

		# Create the editing box
		self.step_qle = QLineEdit(self)

		# Create the date box
		self.date_qde = QDateEdit(self)

		# Create the submit button
		self.qpb = QPushButton(self)

		# Create the numpad buttons
		self.backspace = QPushButton(self)
		self.numpad = []
		for i in range(0, 10):
			self.numpad.append(QPushButton(self))

		'''
		# Create the graph button
		self.graph = QPushButton(self)
		'''

		# Move the labels and set their text
		self.step_lbl.move(100, 80)
		self.step_lbl.setText("Enter number of steps")
		self.step_lbl.adjustSize()
		self.error_lbl.move(100, 120)
		self.date_lbl.move(300, 80)
		self.date_lbl.setText("Enter date")
		self.step_lbl.adjustSize()

		# Move the editing box and setup the return signal
		self.step_qle.move(100, 100)
		self.step_qle.returnPressed.connect(self.submit)

		# Move the date box and setup the format, popup and date
		self.date_qde.move(300, 100)
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		# Move the submit button, set the text and prepare an event for when clicked
		self.qpb.move(230, 120)
		self.qpb.setText("Submit")
		self.qpb.adjustSize()
		self.qpb.clicked.connect(self.submit)

		# Move the numpad, set all the buttons' text and prepare events for being clicked
		self.backspace.move(100, 270)
		self.backspace.setText("Backspace")
		self.backspace.adjustSize()
		self.backspace.clicked.connect(self.delete)
		default_x = 20
		x = default_x
		y = 150
		for i in range(1, 11):
			if i == 10:
				i, x, y = 0, 100, 240
			self.numpad[i].move(x, y)
			self.numpad[i].setText(str(i))
			self.numpad[i].adjustSize()
			self.numpad[i].clicked.connect(partial(self.numbs, i))
			if i == 0:
				break
			x += 80
			if i % 3 == 0:
				x = default_x
				y += 30

		'''
		# Move the graphing button, set its text and prepare the event of being clicked
		self.graph.move(60, 150)
		self.graph.setText("Show Graph")
		self.graph.adjustSize()
		self.graph.clicked.connect(self.show_graph)
		'''

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
		# Get the text from the editing and date boxes
		temp_steps = self.step_qle.text()
		temp_date = self.date_qde.text()
		if len(temp_steps) == 0:
			temp_steps = "0"
		try:
			# Ensure that the format of the text is correct
			steps = int(temp_steps)
			date = datetime.strptime(temp_date, "%m/%d/%Y")
			# If all is well then clear the error label and ready the file
			self.error_lbl.setText("")
			f = open(self.FILE_NAME, "r+")

			# Find any entries already for this date
			goLine = 0
			while True:
				goLine = f.tell()
				line = f.readline()
				s = line.split(",")
				if len(s) == 2 and s[1][:-1] == temp_date:
					try:
						newSteps = int(s[0])
						temp_steps = str(int(temp_steps) + newSteps)
						break
					except Exception as e:
						pass
				if line == "":
					break

			# Either add the steps to the pre-written entry or make a new entry
			f.seek(goLine)
			f.write(temp_steps + "," + temp_date + "\n")
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