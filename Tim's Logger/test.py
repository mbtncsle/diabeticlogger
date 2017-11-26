from WindowParent import WindowParent
import FileLogger as fl
from PyQt5.QtWidgets import *
import sys
from exercise import Exercise
from Foodlist import HelloWindow
from sleep import Sleep
from Logger import Logger

window = 1

app = QApplication(sys.argv)
if window == 1:
	test = Logger("blood_glucose")
elif window == 2:
	test = HelloWindow()
elif window == 3:
	test = Exercise("log.txt", 10, 50)
else:
	test = Sleep("sleep.txt", 10, 50)
test.show()
sys.exit(app.exec_())