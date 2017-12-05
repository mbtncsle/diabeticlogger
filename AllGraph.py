from PyQt5.QtWidgets import QDateEdit, QCheckBox, QDialog, QLabel
import sys
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
sys.path.insert(0, "./database_files")
import blood_glucose_crud, meal_crud, meal_item_crud, sleep_crud, steps_crud

# Class for the extra graph that can show all data against each other
class AllGraph(QDialog):
	def __init__(self):
		super(AllGraph, self).__init__(parent = None)

		# Setup the date selectors for the data with their label
		self.date_begin = QDateEdit(self)
		self.date_begin.move(0, 0)
		self.date_begin.setDisplayFormat("MM/dd/yyyy")
		self.date_begin.setCalendarPopup(True)
		self.date_begin.setDate(datetime.now() - timedelta(days = 30))
		self.date_begin.dateChanged.connect(self.update)

		self.date_lbl = QLabel("to", self)
		self.date_lbl.adjustSize()
		self.date_lbl.move(self.date_begin.size().width() + 10, self.date_begin.size().height() // 2 - self.date_lbl.size().height() // 2)

		self.date_end = QDateEdit(self)
		self.date_end.move(self.date_lbl.pos().x() + self.date_lbl.size().width() + 10, 0)
		self.date_end.setDisplayFormat("MM/dd/yyyy")
		self.date_end.setCalendarPopup(True)
		self.date_end.setDate(datetime.now())
		self.date_end.dateChanged.connect(self.update)

		# Setup the checkboxes
		self.BG_check = QCheckBox("Blood Glucose", self)
		self.sleep_check = QCheckBox("Hours of Sleep", self)
		self.step_check = QCheckBox("Steps walked", self)
		self.food_check = QCheckBox("Carbs ate", self)

		self.BG_check.setChecked(True)
		self.sleep_check.setChecked(True)
		self.step_check.setChecked(True)
		self.food_check.setChecked(True)

		self.BG_check.move(0, 30)
		self.sleep_check.move(0, 50)
		self.step_check.move(0, 70)
		self.food_check.move(0, 90)

		self.graph = PlotCanvas(self)
		self.graph.setGeometry(self.date_end.pos().x() + self.date_end.size().width() + 10, 0, 550, 320)

		self.update()

		self.show()

	# Update the view
	def update(self):
		temp_x_axis = {"BG": [], "sleep": [], "steps": [], "food": []}
		y_axis = []
		max_values = dict()
		min_values = dict()
		for i in range((datetime.now() - datetime.strptime(self.date_end.date().toString("MM/dd/yyyy"), "%m/%d/%Y")).days, -1, -1):
			y_axis.append(i)
			if self.BG_check.isChecked():
				avg = 0
				# Replace empty list with query method
				logs = []
				for log in logs:
					avg += log.reading
				if len(logs) > 0:
					avg /= len(logs)
				if not ("BG" in max_values) or avg > max_values["BG"]:
					max_values["BG"] = avg
				if not ("BG" in min_values) or avg < min_values["BG"]:
					min_values["BG"] = avg
				temp_x_axis["BG"].append(avg)
			if self.sleep_check.isChecked():
				total = 0
				# Replace empty list with query method
				logs = []
				for log in logs:
					total += log.reading
				if not ("sleep" in max_values) or total > max_values["sleep"]:
					max_values["sleep"] = total
				if not ("sleep" in min_values) or total < min_values["sleep"]:
					min_values["sleep"] = total
				temp_x_axis["sleep"].append(total)
			if self.step_check.isChecked():
				total = 0
				# Replace empty list with query method
				logs = []
				for log in logs:
					total += log.reading
				if not ("steps" in max_values) or total > max_values["steps"]:
					max_values["steps"] = total
				if not ("steps" in min_values) or total < min_values["steps"]:
					min_values["steps"] = total
				temp_x_axis["steps"].append(total)
			if self.food_check.isChecked():
				total = 0
				# Replace empty list with query method
				logs = []
				for log in logs:
					total += log.reading
				if not ("food" in max_values) or total > max_values["food"]:
					max_values["food"] = total
				if not ("food" in min_values) or total < min_values["food"]:
					min_values["food"] = total
				temp_x_axis["food"].append(total)
		for k in temp_x_axis:
			for i in temp_x_axis[k]:
				i -= min_values[k]
				if max_values[k] != min_values[k]:
					i /= (max_values[k] - min_values[k])
				i *= 100
		colors = {"BG": "r-", "sleep": "b-", "steps": "g-", "food": "y-"}
		self.graph.plot(temp_x_axis, y_axis, "Percentage", "Days before", colors)

class PlotCanvas(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.fig.subplots_adjust(top = .9, bottom = 0.2)

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
 

	def plot(self, x_axis, y_axis, ylabel, xlabel, colors):
		self.axes.clear()
		for k in x_axis:
			if len(x_axis[k]) > 0:
				self.axes.plot(x_axis[k], y_axis, colors[k])
		self.axes.set_ylabel(ylabel)
		self.axes.set_xlabel(xlabel)
		self.draw()