from InputWindow import InputWindow

class Glucose(InputWindow):

	def __init__(self, parent):
		super(Glucose, self).__init__(parent, "Please enter the blood glucose level")

		self.show()

	# Function for submitting data
	def submit(self):
		try:
			super(Glucose, self).log_input(1, [])
		except Exception as e:
			super().error_lbl.setText("Invalid Input")
			super().error_lbl.adjustSize()