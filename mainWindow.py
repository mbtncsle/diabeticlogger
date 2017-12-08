from PyQt5.QtWidgets import QPushButton, QMdiArea, QApplication, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot
import qdarkstyle
from datetime import datetime
import sys


from exercise import Exercise
from foodlist import Foodlist
from sleep import Sleep
from bloodglucose import Glucose


from RecommendationsWindow import RecommendationsWindow
from GraphWindow import GraphWindow
from LogWindow import LogWindow
from AllGraph import AllGraph

'''
The main window has the task of instantiating all of the main windows: blood glucose input, carb input, sleep input, exercise input, graph, log, recommendations
It also creates the toolbar and regular buttons for switching which windows are visible,
deciding how long ago to pull data from,
displaying the multigraph or allgraph

Beyond this the main window also facilitates the update of the graph and logs including rereading data as well as changing what data is displayed
'''

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__(parent = None)

		# set the title for the window
		self.setWindowTitle("Diabetic Logger")

		# Keep the window at this fixed size
		#self.setFixedSize(509, 746)

		# NEW setup stylesheet
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

		# Variable to keep track of duration of data (defaults to a month)
		self.days = 30

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		CREATION SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Create all of the windows
		self.input_windows = [
		Glucose(self),
		Foodlist(self),
		Sleep(self),
		Exercise(self)
		]
		self.data_windows = [
		GraphWindow(),
		LogWindow(self),
		RecommendationsWindow(self)
		]

		# Create the data duration buttons
		self.date_buttons = [
		QPushButton("1 Day", self),
		QPushButton("1 Week", self),
		QPushButton("1 Month", self),
		QPushButton("1 Year", self)
		]

		# Create the data window changing buttons
		self.data_buttons = [
		QPushButton("Graph", self),
		QPushButton("Data Sheet", self),
		QPushButton("Recommendation", self)
		]

		# Create the toolbar
		self.toolbar = self.addToolBar("Toolbar")
		self.toolbar.setMovable(False)

		# Create the actions for the toolbar
		actions = [
		QAction("Blood Glucose", self),
		QAction("Food Intake", self),
		QAction("Hours of Sleep", self),
		QAction("Steps Walked", self),
		QAction("Graph of all data", self)
		]

		# Create the layouts
		self.main_layout = QVBoxLayout()
		self.date_layout = QHBoxLayout()
		self.data_layout = QHBoxLayout()

		# Create the window spaces
		self.input_mdi = QMdiArea()
		self.data_mdi = QMdiArea()

		# Create the main widget
		self.central_widget = QWidget()

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		SETUP SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Add the actions to the toolbar
		for act in actions:
			self.toolbar.addAction(act)
			self.toolbar.insertSeparator(act)
		self.toolbar.insertSeparator(None)

		# Add the windows to the window spaces
		for wind in self.input_windows:
			self.input_mdi.addSubWindow(wind)
		for wind in self.data_windows:
			self.data_mdi.addSubWindow(wind)

		# Add the date and data buttons to their layouts
		self.date_layout.addStretch(1)
		self.data_layout.addStretch(1)
		for date in self.date_buttons:
			date.setFixedSize(100, 30)
			self.date_layout.addWidget(date)
		for data in self.data_buttons:
			data.setFixedSize(100, 30)
			self.data_layout.addWidget(data)
		self.date_layout.addStretch(1)
		self.data_layout.addStretch(1)


		# Add everything to the main layout
		self.main_layout.addWidget(self.input_mdi)
		self.main_layout.addLayout(self.date_layout)
		self.main_layout.addLayout(self.data_layout)
		self.main_layout.addWidget(self.data_mdi)

		# Set the main layout
		self.central_widget.setLayout(self.main_layout)
		self.setCentralWidget(self.central_widget)

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		SIGNAL SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Setup the clicked signal for all the actions
		self.toolbar.actionTriggered[QAction].connect(self.tool_button_pressed)

		# Setup the clicked signal for the date buttons
		for date in self.date_buttons:
			date.clicked.connect(self.days_button_pressed)

		# Setup the clicked signal for the data buttons
		for data in self.data_buttons:
			data.clicked.connect(self.window_button_pressed)

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		FINISH SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Make default settings
		actions[0].trigger()
		self.date_buttons[2].click()
		self.data_buttons[0].click()

		# Show the window
		self.show()

	'''
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	METHOD SECTION
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	'''

	# Update the data windows with new data
	def update_data(self):
		for wind in self.data_windows:
			wind.update(self.days)
		
	# Update the duration of the data
	@pyqtSlot()
	def days_button_pressed(self):
		if self.sender().text() == "1 Day":
			self.days = 1
		elif self.sender().text() == "1 Week":
			self.days = 7
		elif self.sender().text() == "1 Month":
			self.days = 30
		else:
			self.days = 365
		self.update_data()

	# Update which data window is shown
	@pyqtSlot()
	def window_button_pressed(self):
		for wind in self.data_windows:
			if self.sender().text() != wind.get_name():
				wind.setVisible(False)
			else:
				wind.setVisible(True)

	# Update which input window is shown or show the allgraph
	def tool_button_pressed(self, button):
		if button.text() == "Graph of all data":
			self.all_graph = AllGraph()
		else:
			for wind_index in range(0, len(self.input_windows)):
				if button.text() == self.input_windows[wind_index].get_name():
					self.input_windows[wind_index].setVisible(True)
					for wind in self.data_windows:
						wind.change_data(wind_index)
				else:
					self.input_windows[wind_index].setVisible(False)
			self.update_data()
			

app = QApplication(sys.argv)
inp = MainWindow()
sys.exit(app.exec_())