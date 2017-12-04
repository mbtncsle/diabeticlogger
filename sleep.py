from InputWindow import InputWindow

class Sleep(InputWindow):

	def __init__(self, parent):
		super(Sleep, self).__init__(parent, "Please enter the hours of sleep")

		self.show()

	# Function for submitting data
	def submit(self):
		try:
			super().log_input(2, [])
		except Exception as e:
			super().error_lbl.setText("Invalid Input")
			super().error_lbl.adjustSize()