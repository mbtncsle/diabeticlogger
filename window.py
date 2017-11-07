import sys
from PyQt5.QtWidgets import *

class Window(QWidget):

	# Setup the position, dimensions, title and widget array for the window
	def __init__(self, x, y, width, height, title):
		super().__init__()
		self.windowX = x
		self.windowY = y
		self.windowWidth = width
		self.windowHeight = height
		self.windowTitle = title
		self.widgets = dict()

	# Add a widget of type widget to the window with the name name
	def addWidget(self, name, widget):
		self.widgets[name] = widget(self)

	# Get the widget with the name name
	def getWidget(self, name):
		if name in self.widgets:
			return self.widgets[name]
		else:
			return None

	# Align a widget's left side with the left side of the window
	def leftWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(0, self.widgets[name].pos().y())

	# Align a widget's right side with the right side of the window
	def rightWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(self.windowWidth - self.widgets[name].width(), self.widgets[name].pos().y())

	# Align a widget's top with the top of the window
	def topWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), 0)

	# Align a widget's bottom with the bottom of the window
	def bottomWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), self.windowHeight - self.widgets[name].height())

	# Place a widget in the top left corner
	def topLeftWindowAlign(self, name):
		self.topWindowAlign(name)
		self.leftWindowAlign(name)

	# Place a widget in the top right corner
	def topRightWindowAlign(self, name):
		self.topWindowAlign(name)
		self.rightWindowAlign(name)

	# Place a widget in the bottom left corner
	def bottomLeftWindowAlign(self, name):
		self.bottomWindowAlign(name)
		self.leftWindowAlign(name)

	# Place a widget in the bottom right corner
	def bottomRightWindowAlign(self, name):
		self.bottomWindowAlign(name)
		self.rightWindowAlign(name)

	# Center a widget on the center width of the window
	def centerXWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(self.windowWidth / 2 - self.widgets[name].width() / 2, self.widgets[name].pos().y())

	# Center a widget on the center height of the window
	def centerYWindowAlign(self, name):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), self.windowHeight / 2 - self.widgets[name].height() / 2)

	# Place the widget moving right above the widget still
	def rightAbove(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[moving].pos().x(), self.widgets[still].pos().y() - self.widgets[moving].height())

	# Place the widget moving right below the widget still
	def rightBelow(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[moving].pos().x(), self.widgets[still].pos().y() + self.widgets[still].height())

	# Place the widget moving to the right of the widget still
	def toRight(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[still].pos().x() + self.widgets[still].width(), self.widgets[moving].pos().y())

	# Place the widget moving to the left of the widget still
	def toLeft(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[still].pos().x() - self.widgets[moving].width(), self.widgets[moving].pos().y())

	# Align the left of moving with the left of still
	def leftWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[still].pos().x(), self.widgets[moving].pos().y())

	# Align the right of moving with the right of still
	def rightWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[still].pos().x() - (self.widgets[moving].width() - self.widgets[still].width()), self.widgets[moving].pos().y())

	# Align the top of moving with the top of still
	def topWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[moving].pos().x(), self.widgets[still].pos().y())

	# Align the bottom of moving with the bottom of still
	def bottomWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[moving].pos().x(), self.widgets[still].pos().y() - (self.widgets[moving].height() - self.widgets[still].height()))

	# Align the center of the width of moving with the center of the width of still
	def centerXWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[still].pos().x() - (self.widgets[moving].width() / 2 - self.widgets[still].width() / 2), self.widgets[moving].pos().y())

	# Align the center of the height of moving with the center of the height of still
	def centerYWidgetAlign(self, still, moving):
		if still in self.widgets and moving in self.widgets:
			self.widgets[moving].move(self.widgets[moving].pos().x(), self.widgets[still].pos().y() - (self.widgets[moving].height() / 2 - self.widgets[still].height() / 2))

	# Place the center of the height of name at the yValue
	def centerYAlign(self, name, yValue):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), yValue - self.widgets[name].height() / 2)

	# Place the center of the width of name at the xValue
	def centerXAlign(self, name, xValue):
		if name in self.widgets:
			self.widgets[name].move(xValue - self.widgets[name].width() / 2, self.widgets[name].pos().y())

	# Place the top of name at the yValue
	def topYAlign(self, name, yValue):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), yValue)

	# Place the left of name at the xValue
	def leftXAlign(self, name, xValue):
		if name in self.widgets:
			self.widgets[name].move(xValue, self.widgets[name].pos().y())

	# Place the bottom of name at the yValue
	def bottomYAlign(self, name, yValue):
		if name in self.widgets:
			self.widgets[name].move(self.widgets[name].pos().x(), yValue - self.widgets[name].height())

	# Place the right of name at the xValue
	def rightXAlign(self, name, xValue):
		if name in self.widgets:
			self.widgets[name].move(xValue - self.widgets[name].width(), self.widgets[name].pos().y())

	# Set the text of name (takes care of adjusting the size)
	def setText(self, name, text):
		if name in self.widgets:
			self.widgets[name].setText(text)
			self.widgets[name].adjustSize()

	# Adjust the size of the window to fit the widgets
	def adjustSize(self):
		maxX = 0
		maxY = 0
		for i in self.widgets:
			x = self.widgets[i].pos().x() + self.widgets[i].width()
			y = self.widgets[i].pos().y() + self.widgets[i].height()
			if x > maxX:
				maxX = x
			if y > maxY:
				maxY = y
		self.windowWidth = maxX
		self.windowHeight = maxY

	# Display the window (note: only do this once all widgets are prepared)
	def makeWindow(self):
		self.setGeometry(self.windowX, self.windowY, self.windowWidth, self.windowHeight)
		self.setWindowTitle(self.windowTitle)
		self.show()