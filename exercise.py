from datetime import datetime
from InputWindow import InputWindow
import sys
sys.path.insert(0, "./database_files")
import steps_crud

class Exercise(InputWindow):

	def __init__(self, parent):
		super(Exercise, self).__init__(parent, "Please enter the number of steps")

		self.show()

	# Function for submitting data
	def submit(self):
		inputs = super(Exercise, self).get_inputs()
		try:
			int(inputs[0])
			inputs[1].toString("yyyy-MM-dd")
			inputs[2].toString("hh:mm")
		except Exception as e:
			super(Exercise, self).set_error("Invalid Input")
			return
		dt = datetime.strptime(inputs[1].toString("yyyy-MM-dd") + " " + inputs[2].toString("hh:mm") + ":00", "%Y-%m-%d %H:%M:%S")
		steps_crud.steps_insert(steps_crud.StepsRecord(reading = int(inputs[0]), record_date = dt))
		super(Exercise, self).update()
		super(Exercise, self).submit_notify()