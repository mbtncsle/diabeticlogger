'''
This is a very simple window for logging steps
It doesn't do a lot or look like a lot and it doesn't even take in time, but only date
It does, however, take in the number of steps on a particular date and store that information in a file with a very simple formatting system
'''

import sys
from PyQt5.QtWidgets import *
from datetime import datetime
from functools import partial
import window

class Exercise():

	FILE_NAME = "log.txt"

	def __init__(self):
		self.wind = window.Window(300, 300, 500, 300, "Exercise Window")
		self.initUI()

	def initUI(self):
		# Create the labels
		self.wind.addWidget("step_lbl", QLabel)
		self.wind.addWidget("error_lbl", QLabel)
		self.wind.addWidget("date_lbl", QLabel)

		# Create the editing box
		self.wind.addWidget("step_qle", QLineEdit)

		# Create the date box
		self.wind.addWidget("date_qde", QDateEdit)

		# Create the submit button
		self.wind.addWidget("qpb", QPushButton)

		# Create the numpad buttons
		self.wind.addWidget("backspace", QPushButton)
		for i in range(0, 10):
			self.wind.addWidget(str(i), QPushButton)

		'''
		# Create the graph button
		self.graph = QPushButton(self)
		'''

		# Move the labels and set their text
		self.wind.topLeftWindowAlign("step_lbl")
		self.wind.setText("step_lbl", "Enter number of steps")
		self.wind.topWindowAlign("error_lbl")
		self.wind.toRight("step_lbl", "error_lbl")
		self.wind.topWindowAlign("date_lbl")
		self.wind.leftXAlign("date_lbl", self.wind.getWidget("error_lbl").pos().x() + self.wind.getWidget("error_lbl").width() * 2)
		self.wind.setText("date_lbl", "Enter date")

		# Move the editing box and setup the return signal
		self.wind.rightBelow("step_lbl", "step_qle")
		self.wind.leftWidgetAlign("step_lbl", "step_qle")
		self.wind.getWidget("step_qle").returnPressed.connect(self.submit)

		# Move the date box and setup the format, popup and date
		self.wind.rightBelow("date_lbl", "date_qde")
		self.wind.leftWidgetAlign("date_lbl", "date_qde")
		self.wind.getWidget("date_qde").setDisplayFormat("MM/dd/yyyy")
		self.wind.getWidget("date_qde").setCalendarPopup(True)
		self.wind.getWidget("date_qde").setDate(datetime.now())

		# Move the submit button, set the text and prepare an event for when clicked
		self.wind.rightBelow("date_qde", "qpb")
		self.wind.leftWidgetAlign("date_qde", "qpb")
		self.wind.setText("qpb", "Submit")
		self.wind.getWidget("qpb").clicked.connect(self.submit)

		# Move the numpad, set all the buttons' text and prepare events for being clicked
		for i in range(1, 10):
			if i % 3 == 1:
				self.wind.leftWindowAlign(str(i))
			else:
				self.wind.toRight(str(i - 1), str(i))
			if i < 4:
				self.wind.rightBelow("qpb", str(i))
			else:
				self.wind.rightBelow(str(i - 3), str(i))
			self.wind.setText(str(i), str(i))
			self.wind.getWidget(str(i)).clicked.connect(partial(self.numbs, i))
		self.wind.leftWidgetAlign("8", "0")
		self.wind.rightBelow("8", "0")
		self.wind.setText("0", "0")
		self.wind.getWidget("0").clicked.connect(partial(self.numbs, 0))
		self.wind.leftWidgetAlign("0", "backspace")
		self.wind.rightBelow("0", "backspace")
		self.wind.setText("backspace", "Backspace")
		self.wind.getWidget("backspace").clicked.connect(self.delete)

		# Prepare the actual window
		self.wind.adjustSize()
		self.wind.makeWindow()

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.wind.setText("step_qle", self.wind.getWidget("step_qle").text() + str(number))

	# Function for deleting the last number
	def delete(self):
		string = self.wind.getWidget("step_qle").text()
		if len(string) > 0:
			self.wind.setText("step_qle", string[:-1])

	# Function for when the button was clicked
	def submit(self):
		# Get the text from the editing and date boxes
		temp_steps = self.wind.getWidget("step_qle").text()
		temp_date = self.wind.getWidget("date_qde").text()
		if len(temp_steps) == 0:
			temp_steps = "0"
		try:
			# Ensure that the format of the text is correct
			steps = int(temp_steps)
			date = datetime.strptime(temp_date, "%m/%d/%Y")
			# If all is well then clear the error label and ready the file
			self.wind.setText("error_lbl", "")
			try:
				f = open(self.FILE_NAME, "r+")
			except Exception as e:
				f = open(self.FILE_NAME, "a")
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
			self.wind.setText("error_lbl", "Error, incorrect input")

# Start up the whole thing
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Exercise()
    sys.exit(app.exec_())