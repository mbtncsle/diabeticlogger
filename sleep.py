from module_references import *


class Sleep(InputWindow):

    def __init__(self, parent):
        super(Sleep, self).__init__(parent, "Please enter the hours of sleep")

        super(Sleep, self).set_units("hours")

        self.show()

    # Function for submitting data
    def submit(self):
        inputs = super(Sleep, self).get_inputs()
        try:
            int(inputs[0])
            inputs[1].toString("yyyy-MM-dd")
            inputs[2].toString("hh:mm")
        except Exception as e:
            super(Sleep, self).set_error("Invalid Input")
            return
        dt = datetime.strptime(inputs[1].toString("yyyy-MM-dd") + " " + inputs[2].toString("hh:mm") + ":00",
                               "%Y-%m-%d %H:%M:%S")
        sleep_crud.sleep_insert(sleep_crud.SleepRecord(reading=int(inputs[0]), record_date=dt))
        super(Sleep, self).update()
        super(Sleep, self).submit_notify()
