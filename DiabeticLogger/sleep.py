'''
This is a very simple window for logging steps
It doesn't do a lot or look like a lot and it doesn't even take in time, but only date
It does, however, take in the number of steps on a particular date and store that information in a file with a very simple formatting system
'''

import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from datetime import datetime
from functools import partial
import window

class Sleep(QMdiSubWindow):

	def __init__(self, file, x, y):
		super(Sleep, self).__init__(parent = None)
		self.FILE_NAME = file
		self.x = x
		self.y = y
		self.windowWidth = 500
		self.windowHeight = 300
		self.windowTitle = "Sleep Window"
		self.wind = window.Window(self.windowWidth, self.windowHeight)
		self.widgets = dict()
		self.initUI()

	def initUI(self):

		# Create the QWidget
		wid = QWidget()

		# Create the labels
		self.widgets["sleep_lbl"] = QLabel(wid)
		self.widgets["error_lbl"] = QLabel(wid)
		self.widgets["date_lbl"] = QLabel(wid)

		# Create the editing box
		self.widgets["sleep_qle"] = QLineEdit(wid)

		# Create the date box
		self.widgets["date_qde"] = QDateEdit(wid)

		# Create the submit button
		self.widgets["qpb"] = QPushButton(wid)

		# Create the graphing button
		self.widgets["graph"] = QPushButton(wid)

		# Create the numpad buttons
		self.widgets["backspace"] = QPushButton(wid)
		for i in range(0, 10):
			self.widgets["numpad" + str(i)] = QPushButton(wid)

		# Move the labels and set their text
		self.wind.topLeftWindowAlign(self.widgets["sleep_lbl"])
		self.wind.setText(self.widgets["sleep_lbl"], "Enter number of hours")
		self.wind.topWindowAlign(self.widgets["error_lbl"])
		self.wind.toRight(self.widgets["sleep_lbl"], self.widgets["error_lbl"])
		self.wind.topWindowAlign(self.widgets["date_lbl"])
		self.wind.leftXAlign(self.widgets["date_lbl"], self.widgets["error_lbl"].pos().x() + self.widgets["error_lbl"].width() * 2)
		self.wind.setText(self.widgets["date_lbl"], "Enter date")

		# Move the editing box and setup the return signal
		self.wind.rightBelow(self.widgets["sleep_lbl"], self.widgets["sleep_qle"])
		self.wind.leftWidgetAlign(self.widgets["sleep_lbl"], self.widgets["sleep_qle"])
		self.widgets["sleep_qle"].returnPressed.connect(self.submit)

		# Move the date box and setup the format, popup and date
		self.wind.rightBelow(self.widgets["date_lbl"], self.widgets["date_qde"])
		self.wind.leftWidgetAlign(self.widgets["date_lbl"], self.widgets["date_qde"])
		self.widgets["date_qde"].setDisplayFormat("MM/dd/yyyy")
		self.widgets["date_qde"].setCalendarPopup(True)
		self.widgets["date_qde"].setDate(datetime.now())

		# Move the submit button, set the text and prepare an event for when clicked
		self.wind.rightBelow(self.widgets["date_qde"], self.widgets["qpb"])
		self.wind.leftWidgetAlign(self.widgets["date_qde"], self.widgets["qpb"])
		self.wind.setText(self.widgets["qpb"], "Submit")
		self.widgets["qpb"].clicked.connect(self.submit)

		# Set the text and prepare an event for when clicked for the graph button
		self.wind.setText(self.widgets["graph"], "Show Graph")
		self.widgets["graph"].clicked.connect(self.graph)

		# Move the numpad, set all the buttons' text and prepare events for being clicked
		for i in range(1, 10):
			if i % 3 == 1:
				self.wind.leftWindowAlign(self.widgets["numpad" + str(i)])
			else:
				self.wind.toRight(self.widgets["numpad" + str(i - 1)], self.widgets["numpad" + str(i)])
			if i < 4:
				self.wind.rightBelow(self.widgets["qpb"], self.widgets["numpad" + str(i)])
			else:
				self.wind.rightBelow(self.widgets["numpad" + str(i - 3)], self.widgets["numpad" + str(i)])
			self.wind.setText(self.widgets["numpad" + str(i)], str(i))
			self.widgets["numpad" + str(i)].clicked.connect(partial(self.numbs, i))
		self.wind.leftWidgetAlign(self.widgets["numpad8"], self.widgets["numpad0"])
		self.wind.rightBelow(self.widgets["numpad8"], self.widgets["numpad0"])
		self.wind.setText(self.widgets["numpad0"], "0")
		self.widgets["numpad0"].clicked.connect(partial(self.numbs, 0))
		self.wind.leftWidgetAlign(self.widgets["numpad0"], self.widgets["backspace"])
		self.wind.rightBelow(self.widgets["numpad0"], self.widgets["backspace"])
		self.wind.setText(self.widgets["backspace"], "Backspace")
		self.widgets["backspace"].clicked.connect(self.delete)

		# Prepare the actual window and align graph
		#self.windowWidth, self.windowHeight = self.wind.adjustSize(self.widgets)
		self.wind.bottomRightWindowAlign(self.widgets["graph"])
		self.setGeometry(self.x, self.y, self.windowWidth, self.windowHeight)
		wid.setWindowTitle(self.windowTitle)
		self.setWidget(wid)

	# Function for showing a graph of data
	def graph(self):
		try:

			# Open the file to read from
			f = open(self.FILE_NAME, "r")

			# Take each entry and split it into date and step counting lists (keep steps organized by date)
			tempSteps = dict()
			dates = []
			for line in f:
				newLine = line.split(",")
				tempSteps[newLine[1][:-1]] = int(newLine[0])
				dates.append(datetime.strptime(newLine[1][:-1], "%m/%d/%Y"))

			# Sort the dates and appropriately sort the step counts with them
			dates = sorted(dates)
			steps = []
			for d in dates:
				steps.append(tempSteps[datetime.strftime(d, "%m/%d/%Y")])

			# Change the dates into strings
			stringDates = []
			for d in dates:
				stringDates.append(datetime.strftime(d, "%m/%d/%Y"))

			# Create the line plot with dates as the x-axis and steps as the y-axis and label each axis appropriately
			plt.plot(stringDates, steps)
			plt.ylabel("Number of steps")
			plt.xlabel("Date")
			plt.show()
		except Exception as e:

			# If there is an issue it should be because the file does not exist
			self.wind.setText(self.widgets["error_lbl"], "No data to graph")

	# Function for entering numpad numbers into the text box
	def numbs(self, number):
		self.wind.setText(self.widgets["step_qle"], self.widgets["step_qle"].text() + str(number))

	# Function for deleting the last number
	def delete(self):
		string = self.widgets["step_qle"].text()
		if len(string) > 0:
			self.wind.setText(self.widgets["step_qle"], string[:-1])

	# Function for when the button was clicked
	def submit(self):
		# Get the text from the editing and date boxes
		temp_steps = self.widgets["sleep_qle"].text()
		temp_date = self.widgets["date_qde"].text()
		if len(temp_steps) == 0:
			temp_steps = "0"
		try:
			# Ensure that the format of the text is correct
			steps = int(temp_steps)
			date = datetime.strptime(temp_date, "%m/%d/%Y")
			# If all is well then clear the error label and ready the file
			self.wind.setText(self.widgets["error_lbl"], "")
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
			self.wind.setText(self.widgets["error_lbl"], "Error, incorrect input")