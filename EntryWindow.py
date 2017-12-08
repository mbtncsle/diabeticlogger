from PyQt5.QtWidgets import QLabel, QPushButton, QMdiSubWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot

class EntryWindow(QMdiSubWindow):

	def __init__(self, main_text, parent):
		super(EntryWindow, self).__init__(parent = None)

		self.parent = parent
		
		# Prepare the window
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setFocusPolicy(Qt.NoFocus)

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		CREATION SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Create the labels
		self.main_lbl = QLabel(main_text, self)
		self.unit_lbl = QLabel(self)

		# Create the buttons
		self.submit_qpb = QPushButton("Submit", self)
		self.backspace_qpb = QPushButton("Del", self)

		# Create the numpad
		self.num_buttons = [0]*10
		for i in range(0, 10):
			self.num_buttons[i] = QPushButton(str(i), self)

		# Create the edit box
		self.main_qle = QLineEdit(self)

		# Create the layouts
		self.main_layout = QVBoxLayout()
		self.rows = [QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()]

		# Create the main widget
		self.main_widget = QWidget()

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		SETUP SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Make the first row
		self.rows[0].addWidget(self.main_lbl)

		# Make the second row
		self.rows[1].addWidget(self.main_qle)
		self.rows[1].addWidget(self.unit_lbl)

		# Make the third row
		for i in range(1, 4):
			self.rows[2].addWidget(self.num_buttons[i])

		# Make the fourth row
		for i in range(4, 7):
			self.rows[3].addWidget(self.num_buttons[i])

		# Make the fifth row
		for i in range(7, 10):
			self.rows[4].addWidget(self.num_buttons[i])

		# Make the sixth row
		self.rows[5].addWidget(self.num_buttons[0])
		self.rows[5].addWidget(self.backspace_qpb)

		# Make the main layout
		for i in range(0, len(self.rows)):
			self.main_layout.addLayout(self.rows[i])
		self.main_layout.addWidget(self.submit_qpb)

		# Setup the main widget
		self.main_widget.setLayout(self.main_layout)
		self.setWidget(self.main_widget)

		'''
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		SIGNAL SECTION
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		'''

		# Setup the numpad clicked signals
		self.submit_qpb.clicked.connect(self.submit)
		self.backspace_qpb.clicked.connect(self.delete)
		for num in self.num_buttons:
			num.clicked.connect(self.numbs)

		# Setup the return pressed signal for the main edit box
		self.main_qle.returnPressed.connect(self.submit)

	'''
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	METHOD SECTION
	--------------------------------------------------------------------------------------------------------------------------------------------------------------
	'''

	# Adds numbers to the text edit based on keypad entry
	@pyqtSlot()
	def numbs(self):
		self.main_qle.setText(self.main_qle.text() + str(self.sender().text()))

	# Deletes text from the text edit when the backspace button is clicked
	def delete(self):
		string = self.main_qle.text()
		if len(string) > 0:
			self.main_qle.setText(string[:-1])

	# Submits the current data
	def submit(self):
		self.parent.submit()

	# Returns the text edit value
	def get_input(self):
		return self.main_qle.text()

	# Sets the units
	def set_unit(self, unit):
		self.unit_lbl.setText(unit)
		self.adjustSize()