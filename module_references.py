#all modules in one file.
# DO NOT ADD OR MODIFY UNLESS NECESARY
# DO NOT CHANGE ORDER!! CHANGING ORDER CAN MAKE THE APP FAIL BECAUSE OF DEPENDENCIES
# EXAMPLE: meal_item_crud, MUST BE LOADED BEFORE meal_crud

#sys module
import sys

#math modules
import random
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

#GUI module
import PyQt5
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QCheckBox, QComboBox, QMdiSubWindow, QPushButton, QDialog, QLineEdit, QDateEdit, QTimeEdit, QVBoxLayout, QScrollArea, QFrame, QMdiArea, QApplication, QMainWindow, QAction, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt , pyqtSlot, QTime
from PyQt5.QtGui import QFont

#theme module
import qdarkstyle

#database classes
import pyodbc
import db
import blood_glucose_crud, meal_item_crud,meal_crud, sleep_crud, steps_crud

#window classes for rendering
from RecommendationsWindow import RecommendationsWindow
from GraphWindow import GraphWindow
from LogWindow import LogWindow
from AllGraph import AllGraph
from InputWindow import InputWindow

#function classes
from exercise import Exercise
from foodlist import Foodlist
from sleep import Sleep
from bloodglucose import Glucose

