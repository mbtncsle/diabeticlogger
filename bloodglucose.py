from module_references import *

class Glucose(InputWindow):

	def __init__(self, parent):
		super(Glucose, self).__init__(parent, "Please enter the blood glucose level")

		#creates variable lbl and sets name as meal list
		self.lbl = QLabel("Meal List", self) 
		#set combo and calls the combobox function to be able to modify a drop box
		self.combo = QComboBox(self)	
		self.combo.addItem("Before Breakfast", "Before Breakfast")
		self.combo.addItem("After Breakfast", "After Breakfast")
		self.combo.addItem("Before Lunch", "Before Lunch")
		self.combo.addItem("After Lunch", "After Lunch")
		self.combo.addItem("Before Dinner", "Before Dinner")
		self.combo.addItem("After Dinner", "After Dinner")

		self.combo.setGeometry(275, 45, 120, 40)
		self.lbl.setGeometry(308, 30, 25, 25)
		self.lbl.adjustSize()

		super(Glucose, self).set_units("mg/dL")

		self.show()

	# Function for submitting data
	def submit(self):
		inputs = super(Glucose, self).get_inputs()
		try:
			int(inputs[0])
			inputs[1].toString("yyyy-MM-dd")
			inputs[2].toString("hh:mm")
		except Exception as e:
			super(Glucose, self).set_error("Invalid Input")
			return
		dt = datetime.strptime(inputs[1].toString("yyyy-MM-dd") + " " + inputs[2].toString("hh:mm") + ":00", "%Y-%m-%d %H:%M:%S")
		blood_glucose_crud.blood_glucose_insert(blood_glucose_crud.BloodGlucoseRecord(meal = self.combo.currentText(), reading = int(inputs[0]), record_date = dt))
		super(Glucose, self).update()
		super(Glucose, self).submit_notify()