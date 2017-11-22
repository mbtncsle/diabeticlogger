from PyQt5.QtWidgets import QMdiArea, QApplication, QPushButton, QMainWindow, QAction
from PyQt5.QtCore import Qt
import sys

# Import your class here
from InputWindow import InputWindow

class Test(QMainWindow):

	def __init__(self):
		super(Test, self).__init__(parent = None)

		self.mdi = QMdiArea()
		self.setCentralWidget(self.mdi)

		# Change this to your class
		self.wind = InputWindow()

		self.wind.make_window()

		self.mdi.addSubWindow(self.wind)

		self.setGeometry(100, 30, 500, 500)
		self.show()

app = QApplication(sys.argv)
inp = Test()
sys.exit(app.exec_())