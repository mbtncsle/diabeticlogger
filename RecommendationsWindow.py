from PyQt5.QtWidgets import QMdiSubWindow, QLabel, QScrollArea,QFrame,QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMdiSubWindow, QVBoxLayout, QScrollArea, QLabel, QFrame, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot
from datetime import datetime, timedelta
import sys
sys.path.insert(0, "./database_files")
import db
import pyodbc


class RecommendationsWindow(QMdiSubWindow):

	def __init__(self, parent):
		super(RecommendationsWindow, self).__init__(parent = None)

		self.parent = parent

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4
		self.data = self.blood_glucose

		self.scrollarea = QScrollArea(self)
		self.scrollarea.setWidgetResizable(True)
		self.frame = QFrame(self.scrollarea)
		self.frame.setLayout(QVBoxLayout())
		self.scrollarea.setWidget(self.frame)
		self.scrollarea.setGeometry(0, 0, 505, 325)

		self.show()
	# Change which data logs are shown
	def change_data(self, data):
		self.data = data


	# Clear frames layout
	def clear_layout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.clear_layout(item.layout())

	# Get logs and show them
	def update(self, previous_days):
		self.clear_layout(self.frame.layout())
		
		if self.data == self.blood_glucose:
			is_bg_in_range(self)
			get_montly_bg_average(self)
			
		elif self.data == self.food_list:
		
			what_to_eat(self, previous_days)
			
		elif self.data == self.sleep:
			
			how_is_sleep_affecting_bg(self)
			get_average_sleep(self, previous_days)
		else:
			self.frame.layout().addWidget(QLabel(""))


def get_montly_bg_average(self):
	query= "SELECT TOP 1 READING, MEAL FROM BLOODGLUCOSE ORDER BY RecordDate DESC"
	reading, meal = execute_sql_fetchone(query)
	sql = "EXEC USR_USP_GET_MONTHLY_BG_AVERAGE @READING = " + str(reading) + ", @MEAL = '" + str(meal) + "'"
	(recommendation,) = execute_sql_fetchone(sql)
	self.frame.layout().addWidget(QLabel(str(recommendation)))

def is_bg_in_range(self):
	query= "SELECT TOP 1 READING FROM BLOODGLUCOSE ORDER BY RecordDate DESC"
	(reading,) = execute_sql_fetchone(query)
	sql = "EXEC USR_USP_IS_BG_IN_RANGE @READING = " + str(reading)
	(recommendation,) = execute_sql_fetchone(sql)
	self.frame.layout().addWidget(QLabel(str(recommendation)))

def what_to_eat(self, previous_days):
	query= "EXEC USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES @DAYS = '" + str(previous_days) + "'"
	reading = execute_sql_fetchall(query)
	for recommendation in reading:
		self.frame.layout().addWidget(QLabel(recommendation))

def how_is_sleep_affecting_bg(self):
	query= "EXEC USR_USP_SLEEP_AFFECTS_BG"
	reading = execute_sql_fetchall(query)
	for recommendation in reading:
		self.frame.layout().addWidget(QLabel(recommendation))

def get_average_sleep(self, previous_days):
	query = "EXEC USR_USP_GET_AVERAGE_SLEEP @DAYS = " + str(previous_days) 
	reading = execute_sql_fetchall(query)
	for recommendation in reading:
		self.frame.layout().addWidget(QLabel(recommendation))

def execute_sql_fetchone(query):
	result= []
	with db.Db() as cursor:
		try:
			cursor.execute(query)
			result = cursor.fetchone()
		except pyodbc.Error as ex:
			print(ex.args)
	
	return result


def execute_sql_fetchall(query):
	result= []
	with db.Db() as cursor:
		try:
			cursor.execute(query)
			table = cursor.fetchall()
		except pyodbc.Error as ex:
			print(ex.args)

	for row in table:
		result.append(row[0])
	return result
	