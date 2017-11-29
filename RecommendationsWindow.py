from PyQt5.QtWidgets import QMdiSubWindow, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import pandas as pd

import dateutil as date

import statistics as stats

import blood_glucose_crud as bgc

import importlib.util

import sys

class RecommendationsWindow(QMdiSubWindow):

	def __init__(self):
		super(RecommendationsWindow, self).__init__(parent = None)

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		self.tit = QLabel(self)
		self.tit.setFont(QFont("Times", 20, QFont.Bold))
		self.tit.setText("Stats and Recommendations")
		self.tit.adjustSize()
		self.tit.move(0, 0)

		self.high = QLabel(self)
		self.high.move(0, 50)

		self.low = QLabel(self)
		self.low.move(0, 80)

		self.avg = QLabel(self)
		self.avg.move(0, 110)

		self.update()

		self.show()

	# Get recommendation and show it
	def update(self):
				
		#returns a list of classes of the type Blood Glucose

		listOfBloodGlucoseClasses = bgc.blood_glucose_select_by_days(90)
		#get the attributes of the class

		BGcolumns = listOfBloodGlucoseClasses.pop().__dict__.keys()

		#create a dataframe with only columns
		df = pd.DataFrame(data=None,index=None,columns=BGcolumns)

		index = 0
		#add row by row to the dataframe
		for BG_Class in listOfBloodGlucoseClasses:
			df.loc[index] = [BG_Class.blood_glucose_id,BG_Class.meal,BG_Class.reading,BG_Class.record_date,BG_Class.notes]
			index = index + 1

		MaxBloodGlucoseReading = 500 #df.loc[df['reading'].argmax(),'reading']

		#MaxBloodGlucoseDate = df.loc[df['reading'].argmax(),'record_date']
		MinBloodGlucoseReading = 50 #df.loc[df['reading'].argmin(),'reading']

		#MinBloodGlucoseDate = df.loc[df['reading'].argmin(),'record_date']
		All_Average = 268 #df['reading'].mean()

		self.high.setText('Highest Blood Glucose Reading: ' + str(MaxBloodGlucoseReading))
		self.high.adjustSize()
		self.low.setText('Lowest Blood Glucose Reading: ' + str(MinBloodGlucoseReading))
		self.low.adjustSize()
		self.avg.setText('All-Time Average: ' + str(All_Average))
		self.avg.adjustSize()