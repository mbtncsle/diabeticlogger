'''
This is a very simple window for logging steps
It doesn't do a lot or look like a lot and it doesn't even take in time, but only date
It does, however, take in the number of steps on a particular date and store that information in a file with a very simple formatting system
'''

import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QApplication, QPushButton)
from datetime import datetime

class Exercise(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# Create the labels (one for the steps, one for the date and one for errors)
		self.step_lbl = QLabel(self)
		self.date_lbl = QLabel(self)
		self.error_lbl = QLabel(self)

		# Create the editing boxes (one for the steps and one for the date)
		self.step_qle = QLineEdit(self)
		self.date_qle = QLineEdit(self)

		# Create the button
		self.qpb = QPushButton(self)

		# Move the labels and set their text
		self.step_lbl.move(60, 80)
		self.step_lbl.setText("Enter number of steps")
		self.step_lbl.adjustSize()
		self.date_lbl.move(200, 80)
		self.date_lbl.setText("Enter the date (mm/dd/yyyy)")
		self.date_lbl.adjustSize()
		self.error_lbl.move(60, 140)

		# Move the editing boxes
		self.step_qle.move(60, 100)
		self.date_qle.move(200, 100)

		# Move the button, set the text and prepare an event for when clicked
		self.qpb.move(60, 120)
		self.qpb.setText("Submit")
		self.qpb.adjustSize()
		self.qpb.clicked.connect(self.submit)

		# Prepare the actual window
		self.setGeometry(300, 300, 500, 170)
		self.setWindowTitle("Exercise Window")
		self.show()

	# Function for when the button was clicked
	def submit(self):
		# Get the text from the editing boxes
		temp_steps = self.step_qle.text()
		temp_date = self.date_qle.text()
		try:
			# Ensure that the format of the text is correct
			steps = int(temp_steps)
			date = datetime.strptime(temp_date, "%m/%d/%Y")

			# If all is well then clear the error label and write the values to a log file
			self.errorLbl.setText("")
			f = open("log.txt", "a")
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