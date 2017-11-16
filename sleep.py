import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from datetime import datetime
from functools import partial
import window

class Exercise():

	FILE_NAME = "sleep.txt"

	def __init__(self):
		self.wind = window.Window(300, 300, 500, 300, "Sleep Window")
		self.graphWind = window.Window(500, 500, 300, 300, "Sleep Graph")
		self.initUI()

	def initUI(self):
		# Create the labels
		self.wind.addWidget("sleep_lbl", QLabel)
		self.wind.addWidget("error_lbl", QLabel)
		self.wind.addWidget("date_lbl", QLabel)

		# Create the editing box
		self.wind.addWidget("sleep_qle", QLineEdit)

		# Create the date box
		self.wind.addWidget("date_qde", QDateEdit)

		# Create the submit button
		self.wind.addWidget("qpb", QPushButton)

		# Create the graphing button
		self.wind.addWidget("graph", QPushButton)

		# Move the labels and set their text
		self.wind.topLeftWindowAlign("sleep_lbl")
		self.wind.setText("sleep_lbl", "Enter hours of sleep")
		self.wind.topWindowAlign("error_lbl")
		self.wind.toRight("sleep_lbl", "error_lbl")
		self.wind.topWindowAlign("date_lbl")
		self.wind.leftXAlign("date_lbl", self.wind.getWidget("error_lbl").pos().x() + self.wind.getWidget("error_lbl").width() * 2)
		self.wind.setText("date_lbl", "Enter date")

		# Move the editing box and setup the return signal
		self.wind.rightBelow("sleep_lbl", "sleep_qle")
		self.wind.leftWidgetAlign("sleep_lbl", "sleep_qle")
		self.wind.getWidget("sleep_qle").returnPressed.connect(self.submit)

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

		# Move the graphing button, set the text and prepare an event for when clicked
		self.wind.bottomRightWindowAlign("graph")
		self.wind.setText("graph", "Show Graph")
		self.wind.getWidget("graph").clicked.connect(self.graph)

		# Prepare the actual window
		self.wind.adjustSize()
		self.wind.makeWindow()

	# Function for showing a graph of data
	def graph(self):
		try:
			f = open(self.FILE_NAME, "r")
			tempSteps = dict()
			dates = []
			for line in f:
				newLine = line.split(",")
				tempSteps[newLine[1][:-1]] = int(newLine[0])
				dates.append(datetime.strptime(newLine[1][:-1], "%m/%d/%Y"))
			dates = sorted(dates)
			steps = []
			for d in dates:
				steps.append(tempSteps[datetime.strftime(d, "%m/%d/%Y")])
			stringDates = []
			for d in dates:
				stringDates.append(datetime.strftime(d, "%m/%d/%Y"))
			plt.plot(stringDates, steps)
			plt.ylabel("Number of steps")
			plt.xlabel("Date")
			plt.show()
		except Exception as e:
			self.wind.setText("error_lbl", "No data to graph")

	# Function for deleting the last number
	def delete(self):
		string = self.wind.getWidget("sleep_qle").text()
		if len(string) > 0:
			self.wind.setText("sleep_qle", string[:-1])

	# Function for when the button was clicked
	def submit(self):
		# Get the text from the editing and date boxes
		temp_steps = self.wind.getWidget("sleep_qle").text()
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

			# Either add the hours to the pre-written entry or make a new entry
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
