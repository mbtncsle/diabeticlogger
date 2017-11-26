from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

# Main parent class for the windows
class WindowParent(QMdiSubWindow):

	# Basic init
	def __init__(self, title, icon):
		super(WindowParent, self).__init__(parent = None)
		self.window_widget = QWidget()
		self.window_layout = QFormLayout()
		self.window_widget.setLayout(self.window_layout)
		self.window_widget.setWindowTitle(title)
		self.setWindowIcon(QIcon(QPixmap(icon)))
		self.setWidget(self.window_widget)

	# Add a row of widgets to the window
	def add_row(self, widget_list):
		HBox = QHBoxLayout()
		for i in widget_list:
			HBox.addWidget(i)
		self.window_layout.addRow(HBox)