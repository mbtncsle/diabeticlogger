from PyQt5.QtWidgets import QMdiSubWindow, QSizePolicy
from PyQt5.QtCore import Qt
import sys
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
sys.path.insert(0, "./database_files")
import blood_glucose_crud, meal_crud, meal_item_crud, sleep_crud, steps_crud

class GraphWindow(QMdiSubWindow):

	def __init__(self):
		super(GraphWindow, self).__init__(parent = None)

		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)

		# Setup constants
		self.blood_glucose = 1
		self.sleep = 2
		self.exercise = 3
		self.food_list = 4
		self.data = self.blood_glucose

		self.graph = PlotCanvas(self)
		self.graph.setGeometry(0, 0, 550, 320)

		self.update()

		self.show()

	# Change which data is graphed
	def change_data(self, data):
		self.data = data
		self.update()

	# Get data and graph it
	def update(self, begin = datetime.now() - timedelta(days = 30), end = datetime.now()):
		days = 10
		x_axis = []
		y_axis = []
		xl = "Days Passed"
		if self.data == self.blood_glucose:
			yl = "Blood Glucose"
			for log in blood_glucose_crud.blood_glucose_select_by_days(days):
				d = (datetime.now() - log.record_date).days
				if not (d in x_axis):
					x_axis.append(d)
					y_axis.append([log.reading])
				else:
					y_axis[x_axis.index(d)].append(log.reading)
			for i in range(0, len(y_axis)):
				total = 0
				for y in y_axis[i]:
					total += y
				total /= len(y_axis[i])
				y_axis[i] = total
			x_axis, y_axis = self.update_sort(x_axis, y_axis)
		elif self.data == self.sleep:
			yl = "Hours Slept"
			for log in sleep_crud.sleep_select_by_days(days):
				d = (datetime.now() - log.record_date).days
				if not (d in x_axis):
					x_axis.append(d)
					y_axis.append(log.reading)
				else:
					y_axis[x_axis.index(d)] += log.reading
		elif self.data == self.exercise:
			yl = "Steps Walked"
			for log in steps_crud.steps_select_by_days(days):
				d = (datetime.now() - log.record_date).days
				if not (d in x_axis):
					x_axis.append(d)
					y_axis.append(log.reading)
				else:
					y_axis[x_axis.index(d)] += log.reading
		else:
			yl = "Carbs ate"
			for log in meal_crud.meal_select_by_days(days):
				d = (datetime.now() - log.record_date).days
				total = 0
				for m in log.meal_items:
					total += m.total_carbs
				if not (d in x_axis):
					x_axis.append(d)
					y_axis.append(total)
				else:
					y_axis[x_axis.index(d)] += total
		self.graph.plot([x_axis, y_axis], yl, xl)

	def update_sort(self, m, two):
		if len(m) <= 1:
			return m, two

		middle = len(m) // 2
		left = m[:middle]
		right = m[middle:]

		left, l = self.update_sort(left, two[:middle])
		right, r = self.update_sort(right, two[middle:])
		final_m = []
		final_two = []
		li = 0
		ri = 0
		while li < len(left) and ri < len(right):
			if left[li] < right[ri]:
				final_m.append(left[li])
				final_two.append(l[li])
				li += 1
			else:
				final_m.append(right[ri])
				final_two.append(r[ri])
				ri += 1
		if li < len(left):
			final_m.extend(left[li:])
			final_two.extend(l[li:])
		elif ri < len(right):
			final_m.extend(right[ri:])
			final_two.extend(r[ri:])
		return final_m, final_two

class PlotCanvas(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.fig.subplots_adjust(top = .9, bottom = 0.2)

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
 

	def plot(self, nums, ylabel, xlabel):
		data = nums
		self.axes.clear()
		self.axes.plot(data[0], data[1], 'r-')
		self.axes.set_ylabel(ylabel)
		self.axes.set_xlabel(xlabel)
		self.draw()