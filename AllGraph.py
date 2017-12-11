from module_references import *

# Class for the extra graph that can show all data against each other
class AllGraph(QDialog):
	def __init__(self):
		super(AllGraph, self).__init__(parent = None)

		# Setup the checkboxes
		self.BG_check = QCheckBox("Blood Glucose", self)
		self.sleep_check = QCheckBox("Hours of Sleep", self)
		self.step_check = QCheckBox("Steps walked", self)
		self.food_check = QCheckBox("Carbs ate", self)

		# Adding comment to test push
		self.BG_check.setChecked(True)
		self.sleep_check.setChecked(True)
		self.step_check.setChecked(True)
		self.food_check.setChecked(True)

		self.BG_check.stateChanged.connect(self.update)
		self.sleep_check.stateChanged.connect(self.update)
		self.step_check.stateChanged.connect(self.update)
		self.food_check.stateChanged.connect(self.update)

		self.BG_check.move(0, 30)
		self.sleep_check.move(0, 50)
		self.step_check.move(0, 70)
		self.food_check.move(0, 90)

		self.graph = PlotCanvas(self)
		self.graph.setGeometry(self.sleep_check.pos().x() + self.sleep_check.size().width() + 10, 0, 550, 320)

		self.update()

		self.show()

	# Turn a list into percentages
	def get_percentage(self, l):
		if len(l) == 0:
			return l

		maxi = l[0]
		mini = l[0]

		for log in l:
			if log > maxi:
				maxi = log
			elif log < mini:
				mini = log

		maxi -= mini
		maxi /= 100

		for log in range(0, len(l)):
			l[log] -= mini
			if max > 0:
				l[log] /= maxi

		return l

	# Update the view
	def update(self):
		previous_days = 30
		y_axis = {"BG": [], "sleep": [], "steps": [], "food": []}
		x_axis = {"BG": [], "sleep": [], "steps": [], "food": []}

		if self.BG_check.isChecked():
			for log in blood_glucose_crud.blood_glucose_select_by_days(previous_days):
				d = (datetime.now() - log.record_date).days
				if d >= 0:
					if not (d in x_axis["BG"]):
						x_axis["BG"].append(d)
						y_axis["BG"].append([log.reading])
					else:
						y_axis["BG"][x_axis["BG"].index(d)].append(log.reading)
			for i in range(0, len(y_axis["BG"])):
				total = 0
				for y in y_axis["BG"][i]:
					total += y
				if len(y_axis["BG"][i]) > 0:
					total /= len(y_axis["BG"][i])
				y_axis["BG"][i] = total

		if self.sleep_check.isChecked():
			for log in sleep_crud.sleep_select_by_days(previous_days):
				d = (datetime.now() - log.record_date).days
				if d >= 0:
					if not (d in x_axis["sleep"]):
						x_axis["sleep"].append(d)
						y_axis["sleep"].append(log.reading)
					else:
						y_axis["sleep"][x_axis["sleep"].index(d)] += log.reading

		if self.step_check.isChecked():
			for log in steps_crud.steps_select_by_days(previous_days):
				d = (datetime.now() - log.record_date).days
				if d >= 0:
					if not (d in x_axis["steps"]):
						x_axis["steps"].append(d)
						y_axis["steps"].append(log.reading)
					else:
						y_axis["steps"][x_axis["steps"].index(d)] += log.reading

		if self.food_check.isChecked():
			for log in meal_crud.meal_select_by_days(previous_days):
				d = (datetime.now() - log.record_date).days
				if d >= 0:
					total = 0
					for m in log.meal_items:
						total += m.total_carbs
					if not (d in x_axis["food"]):
						x_axis["food"].append(d)
						y_axis["food"].append(total)
					else:
						y_axis["food"][x_axis["food"].index(d)] += total

		for key in y_axis:
			y_axis[key] = self.get_percentage(y_axis[key])

		colors = {"BG": "r-", "sleep": "b-", "steps": "g-", "food": "y-"}
		labels = {"BG": "Blood Glucose", "sleep": "Sleep", "steps": "Steps", "food": "Carbs"}
		self.graph.plot(x_axis, y_axis, "Percentage", "Days before", colors, labels)

class PlotCanvas(FigureCanvas):

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		self.fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = self.fig.add_subplot(111)
		self.fig.subplots_adjust(top = .9, bottom = 0.2)

		FigureCanvas.__init__(self, self.fig)
		self.setParent(parent)
 

	def plot(self, x_axis, y_axis, ylabel, xlabel, colors, labels):
		self.axes.clear()
		for k in y_axis:
			if len(y_axis[k]) > 0:
				self.axes.plot(x_axis[k], y_axis[k], colors[k], label = labels[k])
		self.axes.invert_xaxis()
		self.axes.legend()
		self.axes.set_ylabel(ylabel)
		self.axes.set_xlabel(xlabel)
		self.draw()