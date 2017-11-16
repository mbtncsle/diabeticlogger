import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QComboBox, QApplication, QPushButton
from PyQt5.QtCore import QSize

class HelloWindow(QWidget):

    FILE_NAME = "log.txt"
    
    def __init__(self):
        super().__init__()        
        self.initUI()
              
    def initUI(self): 
    
        self.error_lbl = QLabel(self)
        #creates variable lvl and sets name as food lists
        self.lbl = QLabel("Food List", self) 
        #set combo and calls the combobox function to be able to modify a drop box
        self.combo = QComboBox(self)	
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
        self.setWindowTitle('Diabetic Logger')
        self.show()
        
    def handleActivated(self, index):
        print(self.combo.itemText(index))
        print(self.combo.itemData(index))
        temp_food = self.combo.itemData(index)
        f = open(self.FILE_NAME, "r+")
        goLine = 0
        temp_food = str(temp_food)
        # Either add the steps to the pre-written entry or make a new entry
        f.seek(goLine)
        f.write(temp_food + "\n")
        f.close()

            # Function for when the button was clicked
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = HelloWindow()
    mainWin.show()
    sys.exit( app.exec_() )

