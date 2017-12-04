from InputWindow import InputWindow

class Exercise(InputWindow):

	def __init__(self, parent):
		super(Exercise, self).__init__(parent, "Please enter the number of steps")

		self.show()

	# Function for submitting data
	def submit(self):
		try:
			super().log_input(3, [])
		except Exception as e:
			super().error_lbl.setText("Invalid input")
			super().error_lbl.adjustSize()
