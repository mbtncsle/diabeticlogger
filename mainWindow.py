from PyQt5.QtWidgets import QPushButton, QMdiArea, QApplication, QMainWindow, QAction
from PyQt5.QtCore import Qt
import qdarkstyle
from datetime import datetime, timedelta
import sys
from InputWindow import InputWindow
from exercise import Exercise
from foodlist import Foodlist
from sleep import Sleep
from bloodglucose import Glucose
from RecommendationsWindow import RecommendationsWindow
from GraphWindow import GraphWindow
from LogWindow import LogWindow
from AllGraph import AllGraph
sys.path.insert(0, "./database_files")
import blood_glucose_crud

class MainWindow(QMainWindow):

	def __init__(self):
		super(MainWindow, self).__init__(parent = None)

		# Global variables
		self.blood_glucose = "BG"
		self.food_intake = "Food"
		self.sleep_hours = "Sleep"
		self.walk_steps = "Walk"

		self.window_width = 509
		self.window_height = 746

		self.margin = 50

		self.setFixedSize(509, 746)
		# NEW setup stylesheet
		app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

		self.oneDay_qpb = QPushButton("1 day", self)
		self.oneDay_qpb.setToolTip("This button displays graph for data collected within the day")
		self.oneDay_qpb.setGeometry(50, 365, 105, 25)

		self.oneWeek_qpb = QPushButton("1 Week", self)
		self.oneWeek_qpb.setToolTip("This button displays graph for data collected within the week")
		self.oneWeek_qpb.setGeometry(155, 365, 105, 25)

		self.oneMonth_qpb = QPushButton("1 Month", self)
		self.oneMonth_qpb.setToolTip("This button displays graph for data collected within the month")
		self.oneMonth_qpb.setGeometry(260, 365, 105, 25)

		self.oneYear_qpb = QPushButton("1 Year", self)
		self.oneYear_qpb.setToolTip("This button displays graph for data collected within the yar")
		self.oneYear_qpb.setGeometry(365, 365, 105, 25)

		self.graph_qpb = QPushButton("Graph", self)
		self.graph_qpb.setToolTip("This button will display a graphical representation of your blood glucose level")
		self.graph_qpb.setGeometry(50, 390, 140, 25)

		self.log_qpb = QPushButton("Data Sheet", self)
		self.log_qpb.setToolTip("This button will display your past inputs")
		self.log_qpb.setGeometry(190, 390, 140, 25)

		self.recommendation_qpb = QPushButton("Recommendation", self)
		self.recommendation_qpb.setToolTip("This button will display recommendations for you to take")
		self.recommendation_qpb.setGeometry(330, 390, 140, 25)

		self.setWindowTitle("Diabetic Logger        A1C Level: " + str(round(self.get_a1c(), 2)))

		# Prepare the main area
		self.mdi = QMdiArea()
		self.setCentralWidget(self.mdi)

		# Prepare the toolbar
		self.toolbar = self.addToolBar("Toolbar")
		self.toolbar.setMovable(False)

		# Create each toolbar action
		actions = [QAction("Blood Glucose", self),
		QAction("Food Intake", self),
		QAction("Hours of Sleep", self),
		QAction("Steps Walked", self),
		QAction("Graph of all data", self)
		]

		# Setup the toolbar and actions
		for i in actions:
			self.toolbar.addAction(i)
			self.toolbar.insertSeparator(i)
		self.toolbar.insertSeparator(None)
		self.toolbar.actionTriggered[QAction].connect(self.tool_button_pressed)

		# Create each of the sub windows
		self.input_windows = {self.blood_glucose: Glucose(self), self.food_intake: Foodlist(self), self.sleep_hours: Sleep(self), self.walk_steps: Exercise(self)}
		self.graph_window = GraphWindow()
		self.recommended_window = RecommendationsWindow()
		self.log_window = LogWindow(self)

		# Hide everything but the blood glucose and add it all to the main window
		self.mdi.addSubWindow(self.graph_window)
		self.mdi.addSubWindow(self.recommended_window)
		self.mdi.addSubWindow(self.log_window)
		self.graph_window.setGeometry(2, 385, 505, 325)
		self.recommended_window.setGeometry(2, 385, 505, 325)
		self.log_window.setGeometry(2, 385, 505, 325)
		for k in self.input_windows:
			self.mdi.addSubWindow(self.input_windows[k])
			self.input_windows[k].setGeometry(2, 2, 505, 385)
			if k != self.blood_glucose:
				self.input_windows[k].setVisible(False)

		self.show()

	# determine the a1c
	def get_a1c(self):
		total = 0
		logs = blood_glucose_crud.blood_glucose_select_by_days(30)
		for log in logs:
			total += log.reading
		total /= len(logs)
		return total

	# update the windows with new data
	def update_data(self):
		self.setWindowTitle("Diabetic Logger        A1C Level: " + str(round(self.get_a1c(), 2)))
		self.graph_window.update(datetime.strptime(self.date_begin.date().toString("MM/dd/yyyy"), "%m/%d/%Y"), datetime.strptime(self.date_end.date().toString("MM/dd/yyyy"), "%m/%d/%Y"))
		#self.recommended_window.update()
		self.log_window.update(datetime.strptime(self.date_begin.date().toString("MM/dd/yyyy"), "%m/%d/%Y"), datetime.strptime(self.date_end.date().toString("MM/dd/yyyy"), "%m/%d/%Y"))

	def tool_button_pressed(self, button):
		bt = button.text()
		num = 0
		if bt == "Blood Glucose":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.blood_glucose].setVisible(True)
			num = 1
		elif bt == "Hours of Sleep":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.sleep_hours].setVisible(True)
			num = 2
		elif bt == "Steps Walked":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.walk_steps].setVisible(True)
			num = 3
		elif bt == "Food Intake":
			for k in self.input_windows:
				self.input_windows[k].setVisible(False)
			self.input_windows[self.food_intake].setVisible(True)
			num = 4
		elif bt == "Graph of all data":
			self.all_graph = AllGraph()
		if num != 0:
			self.graph_window.change_data(num)
			self.log_window.change_data(num)

app = QApplication(sys.argv)
inp = MainWindow()
sys.exit(app.exec_())