from InputWindow import InputWindow

class Sleep(InputWindow):

	def __init__(self, parent):
		super(Sleep, self).__init__(parent, "Please enter the hours of sleep")

		self.show()

	# Function for submitting data
	def submit(self):
		try:
			super(Sleep, self).log_input(2, [])
		except Exception as e:
			super(Sleep, self).set_error("Invalid Input")