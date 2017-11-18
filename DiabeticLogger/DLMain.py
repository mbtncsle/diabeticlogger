import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QMdiArea
from exercise import Exercise
from sleep import Sleep
from Foodlist import HelloWindow
from Logger import Logger


# =====================================
# Team: Vampires
# Diabetic Logger main application
# =====================================
class DiabeticLogger(QMainWindow):
    # =====================================
    # Diabetic Logger Main Window
    # =====================================
    def __init__(self):

        # Setup the main window (Multiple Document Interface)
        super(DiabeticLogger, self).__init__(parent=None)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        # Setup the toolbar
        toolbar = self.addToolBar("Toolbar")
        toolbar.setIconSize(QSize(64, 64))
        toolbar.setStyleSheet("background-color: white;")

        # Exit button
        exit_action = QAction(QIcon("exit.jpg"), "exit", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

        # Blood glucose button
        blood_glucose_action = QAction(QIcon("blood_glucose.jpg"), "blood_glucose", self)
        toolbar.addAction(blood_glucose_action)

        # Carbohydrates button
        carbohydrate_action = QAction(QIcon("carbohydrates.jpg"), "carbohydrates", self)
        toolbar.addAction(carbohydrate_action)

        # Steps button
        steps_action = QAction(QIcon("steps.png"), "steps", self)
        toolbar.addAction(steps_action)

        # Sleep button
        sleep_action = QAction(QIcon("sleep.png"), "sleep", self)
        toolbar.addAction(sleep_action)

        # Connect the button click events
        toolbar.actionTriggered[QAction].connect(self.tool_button_pressed)
        self.setWindowTitle("Diabetic Logger")
        self.show()

    # =====================================
    #  Button press event handler
    # =====================================
    def tool_button_pressed(self, button_pushed):

        button_pushed_text = button_pushed.text()
        if button_pushed_text == "steps":
            log = Exercise("log.txt", 0, 0)
        elif button_pushed_text == "sleep":
            log = Sleep("sleep.txt", 0, 0)
        elif button_pushed_text == "carbohydrates":
            log = HelloWindow()
        else:
            log = Logger("blood_glucose")
        self.mdi.addSubWindow(log)
        log.show()


# =====================================
# Startup routine
# =====================================
def main():

    # Start up the application and show the main form
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("diabetic_logger.jpg"))
    diabetic_logger = DiabeticLogger()
    # Let it run
    sys.exit(app.exec_())


# =====================================
# This is here to prevent it from
# running if imported from another
# application
# =====================================
if __name__ == '__main__':
    main()
