import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox, QApplication, QPushButton, QMdiSubWindow
from PyQt5.QtCore import QSize

class HelloWindow(QMdiSubWindow):

    FILE_NAME = "logfood.txt"
    
    def __init__(self):
        super(HelloWindow, self).__init__(parent = None)        
        self.initUI()
              
    def initUI(self): 
        self.wid = QWidget()
        self.error_lbl = QLabel(self.wid)
        #creates variable lvl and sets name as food lists
        self.lbl = QLabel("Food List", self.wid) 
        #set combo and calls the combobox function to be able to modify a drop box
        self.combo = QComboBox(self.wid)	
        self.combo.addItem("Bread - 11g", 11)
        self.combo.addItem("Rice - 44g", 44)
        self.combo.addItem("Ice Cream - 16g", 16)
        self.combo.addItem("Milk - 12g", 12)
        self.combo.addItem("Stir Fry - 7g", 7)

        self.combo.activated.connect(self.handleActivated)

        self.combo.move(50, 50)					#Location of the dropdown box
        self.lbl.move(50, 35)				#Location of the label
        self.error_lbl.move(50, 75)  
         
        self.setGeometry(300, 300, 300, 200)
        self.wid.setWindowTitle('Diabetic Logger')
        self.setWidget(self.wid)
        
    def handleActivated(self, index):
        print(self.combo.itemText(index))
        print(self.combo.itemData(index))
        temp_food = self.combo.itemData(index)
        try:
            f = open(self.FILE_NAME, "r+")
        except Exception as e:
            f = open(self.FILE_NAME, "a")
            f = open(self.FILE_NAME, "r+")
        goLine = 0
        temp_food = str(temp_food)
        # Either add the steps to the pre-written entry or make a new entry
        f.seek(goLine)
        f.write(temp_food + "\n")
        f.close()