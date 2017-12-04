from PyQt5.QtWidgets import QLabel, QComboBox
from InputWindow import InputWindow

class Foodlist(InputWindow):

	def __init__(self, parent):
		super(Foodlist, self).__init__(parent, "Input the number of servings")

		#creates variable lbl and sets name as food lists
		self.lbl = QLabel("Food List", self) 
		#set combo and calls the combobox function to be able to modify a drop box
		self.combo = QComboBox(self)	
		self.combo.addItem("Bread - 11g", 11)
		self.combo.addItem("Rice - 44g", 44)
		self.combo.addItem("Ice Cream - 16g", 16)
		self.combo.addItem("Milk - 12g", 12)
		self.combo.addItem("Stir Fry - 7g", 7)

		self.combo.activated.connect(self.handleActivated)

		self.lbl_meal = QLabel("Meal List", self)

		self.combo_meal = QComboBox(self)
		self.combo_meal.addItem("Breakfast")
		self.combo_meal.addItem("Lunch")
		self.combo_meal.addItem("Dinner")
		self.combo_meal.addItem("Snack")

		self.combo_meal.setGeometry(400, 45, 80, 40)
		self.combo.setGeometry(275, 45, 120, 40)
		self.lbl_meal.move(423, 30)
		self.lbl.move(308, 30)
		self.lbl_meal.adjustSize()
		self.lbl.adjustSize()

		self.show()

	def handleActivated(self, index):
		try:		
			carbValue = self.combo.itemData(index)
			totalCarbs = carbValue * int(super().serving_qle.text())
			super().error_lbl.setText("")
		except Exception as e:
			super().error_lbl.setText("Wrong input on the serving size")
			super().error_lbl.adjustSize()

		#calculates number of carbs times the serving size


		#Obtained the string name of the food and number of carbs
		#self.combo.itemText(index)

	# Function for submitting data
	def submit(self):
		try:
			int(self.combo.itemData(self.combo.currentIndex()))
			super().log_input(4, [self.combo.itemData(self.combo.currentIndex()), self.combo.currentText().split("-")[0][:-1]])
		except Exception as e:
			self.error_lbl.setText("Invalid Input")
			self.error_lbl.adjustSize()