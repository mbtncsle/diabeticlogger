from PyQt5.QtWidgets import QLabel, QComboBox
from datetime import datetime
from InputWindow import InputWindow
import sys
sys.path.insert(0, "./database_files")
import meal_crud, meal_item_crud

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

		# Unnescesary
		# self.combo.activated.connect(self.handleActivated)

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

		super(Foodlist, self).set_units("servings")

		self.show()

	def get_name(self):
		return "Food Intake"

	# def handleActivated(self, index):
	# 	try:		
	# 		carbValue = self.combo.itemData(index)
	# 		totalCarbs = carbValue * int(super(Foodlist, self).main_qle.text())
	# 	except Exception as e:
	# 		super(Foodlist, self).set_error("Wrong input on the serving size")

	# 	#calculates number of carbs times the serving size


	# 	#Obtained the string name of the food and number of carbs
	# 	#self.combo.itemText(index)

	# Function for submitting data
	def submit(self):

		inputs = super(Foodlist, self).get_inputs()
		try:
			int(inputs[0])
			inputs[1].toString("yyyy-MM-dd")
			inputs[2].toString("hh:mm")
			int(self.combo.itemData(self.combo.currentIndex()))
		except Exception as e:
			super(Foodlist, self).set_error("Invalid Input")
			return
		dt = datetime.strptime(inputs[1].toString("yyyy-MM-dd") + " " + inputs[2].toString("hh:mm") + ":00", "%Y-%m-%d %H:%M:%S")

		id = None
		for m in meal_crud.meal_select_by_days((datetime.now() - dt).days + 1):
			if m.record_date == dt:
				id = m.meal_id
				break
		if id == None:
			id = meal_crud.meal_insert(meal_crud.MealRecord(meal = self.combo_meal.itemData(self.combo_meal.currentIndex()), reading = int(inputs[0]) * int(self.combo.itemData(self.combo.currentIndex())), record_date = dt))
		meal_item_crud.meal_item_insert(meal_item_crud.MealItemRecord(meal_id = id, description = self.combo.currentText().split("-")[0][:-1], portions = int(inputs[0]), carbs_per_portion = int(self.combo.itemData(self.combo.currentIndex())), total_carbs = int(inputs[0]) * int(self.combo.itemData(self.combo.currentIndex()))))

		super(Foodlist, self).update()
		super(Foodlist, self).submit_notify()