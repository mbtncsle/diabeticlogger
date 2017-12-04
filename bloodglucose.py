from PyQt5.QtWidgets import QLabel, QComboBox
from InputWindow import InputWindow

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

		self.show()

	# Function for submitting data
	def submit(self):
		try:
			super(Glucose, self).log_input(1, [self.combo.currentText()])
		except Exception as e:
			super().error_lbl.setText("Invalid Input")
			super().error_lbl.adjustSize()