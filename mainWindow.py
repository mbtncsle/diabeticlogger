import sys
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from datetime import datetime
from functools import partial
import window
import exercise

class MainWindow():

	def __init__(self, gui):

		# Preparing variables
		self.gui = gui
		self.x = 300
		self.y = 300
		self.width = 500
		self.height = 300
		self.title = "Main Window"
		self.wind = window.Window(self.width, self.height)
		self.guis = {"exercise": QDialog(self.gui)}
		self.windows = {"exercise": exercise.Exercise("log.txt", 300, 300, self.guis["exercise"])}
		self.widgets = dict()
		self.initUI()

	def initUI(self):

		# Create the drop down list of other windows
		self.widgets["accessWindows"] = QComboBox(self.gui)
		self.widgets["accessWindows"].addItem("None")
		for i in self.windows:
			self.widgets["accessWindows"].addItem(i.title() + " Window")
		self.widgets["accessWindows"].currentIndexChanged.connect(self.callGui)
		self.wind.topLeftWindowAlign(self.widgets["accessWindows"])

		# Create and prepare the simple a1c viewer
		self.widgets["a1c"] = QLabel(self.gui)
		self.wind.setText(self.widgets["a1c"], "Your current A1C is ") # Note: implement a1c calculation
		self.wind.topWindowAlign(self.widgets["a1c"])
		self.widgets["a1c"].move(200, 0)

		# Setup this window
		#self.width, self.height = self.wind.adjustSize(self.widgets)
		self.gui.setGeometry(self.x, self.y, self.width, self.height)
		self.gui.setWindowTitle(self.title)
		self.gui.show()

	# Function to open another window and reshow this one once that is closed
	def callGui(self):
		if self.widgets["accessWindows"].currentText() != "None":
			self.gui.setVisible(False)
			self.guis[self.widgets["accessWindows"].currentText()[:-7].lower()].exec()
			self.widgets["accessWindows"].setCurrentIndex(0)
			self.gui.setVisible(True)

# Start up the whole thing
if __name__ == "__main__":
	app = QApplication(sys.argv)
	mainGui = QDialog()
	ex = MainWindow(mainGui)
	sys.exit(app.exec_())