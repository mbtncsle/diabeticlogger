from PyQt5.QtWidgets import QMdiSubWindow, QDialog, QLabel, QDateEdit, QTimeEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTime


from datetime import datetime


from EntryWindow import EntryWindow


import sys

class InputWindow(QMdiSubWindow):
	
	def __init__(self, parent, main_text):
		super(InputWindow, self).__init__(parent = None)

		self.parent = parent
		
		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setFocusPolicy(Qt.NoFocus)
		self.move(0, 0)

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		CREATION SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Create the error label
		self.error_lbl = QLabel(self)

		# Create the entry window
		self.entry = EntryWindow(main_text, self)

		# Create the date and time boxes
		self.date_qde = QDateEdit(self)
		self.time_qte = QTimeEdit(self)

		# Create the layouts
		self.main_layout = QHBoxLayout()
		self.columns = [QVBoxLayout(), QVBoxLayout()]

		# Create the main widget
		self.main_widget = QWidget()

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		SETUP SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Setup the date and time
		self.date_qde.setDisplayFormat("MM/dd/yyyy")
		self.date_qde.setCalendarPopup(True)
		self.date_qde.setDate(datetime.now())

		self.time_qte.setDisplayFormat("hh:mm")
		self.time_qte.setTime(QTime())

		# Add the entry window to the first column
		self.columns[0].addWidget(self.entry)
		self.columns[0].addStretch(2)

		# Setup the second column
		self.columns[1].addWidget(self.error_lbl)
		self.columns[1].addWidget(self.time_qte)
		self.columns[1].addWidget(self.date_qde)
		self.columns[1].addStretch(2)

		# Make the main layout
		for i in range(0, len(self.columns)):
			self.main_layout.addLayout(self.columns[i])
			if i < len(self.columns) - 1:
				self.main_layout.addStretch(1)

		# Setup the main widget
		self.main_widget.setLayout(self.main_layout)
		self.setWidget(self.main_widget)

	'''
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	METHOD SECTION
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	'''

	# Display an error
	def set_error(self, text):
		self.error_lbl.setText(text)
		self.error_lbl.adjustSize()

	# Return all inputs necessary for logging inputs
	def get_inputs(self):
		return [self.entry.get_input(), self.date_qde.date(), self.time.time()]

	# Call parent update
	def update(self):
		self.parent.update_data()

	# Create a notification window for submission
	def submit_notify(self):
		note = QDialog()
		note_lbl = QLabel("Data Submitted", note)
		note_button = QPushButton("Okay", note)
		note_button.move(0, 25)
		note_button.clicked.connect(note.accept)
		note.exec_()

	# Log the given input
	def log_input(self, input_type, data):
		self.set_error("")
		self.update()

	# Set the units for the window
	def set_units(self, unit):
		self.entry.set_unit(unit)