import sys
from PyQt5.QtWidgets import *

class Window():

	# Setup the position, dimensions, title and widget array for the window
	def __init__(self, width, height):
		super().__init__()
		self.windowWidth = width
		self.windowHeight = height

	# Align a widget's left side with the left side of the window
	def leftWindowAlign(self, widget):
		widget.move(0, widget.pos().y())

	# Align a widget's right side with the right side of the window
	def rightWindowAlign(self, widget):
		widget.move(self.windowWidth - widget.width(), widget.pos().y())

	# Align a widget's top with the top of the window
	def topWindowAlign(self, widget):
		widget.move(widget.pos().x(), 0)

	# Align a widget's bottom with the bottom of the window
	def bottomWindowAlign(self, widget):
		widget.move(widget.pos().x(), self.windowHeight - widget.height())

	# Place a widget in the top left corner
	def topLeftWindowAlign(self, widget):
		self.topWindowAlign(widget)
		self.leftWindowAlign(widget)

	# Place a widget in the top right corner
	def topRightWindowAlign(self, widget):
		self.topWindowAlign(widget)
		self.rightWindowAlign(widget)

	# Place a widget in the bottom left corner
	def bottomLeftWindowAlign(self, widget):
		self.bottomWindowAlign(widget)
		self.leftWindowAlign(widget)

	# Place a widget in the bottom right corner
	def bottomRightWindowAlign(self, widget):
		self.bottomWindowAlign(widget)
		self.rightWindowAlign(widget)

	# Center a widget on the center width of the window
	def centerXWindowAlign(self, widget):
		widget.move(self.windowWidth / 2 - widget.width() / 2, widget.pos().y())

	# Center a widget on the center height of the window
	def centerYWindowAlign(self, widget):
		widget.move(widget.pos().x(), self.windowHeight / 2 - widget.height() / 2)

	# Place the widget moving right above the widget still
	def rightAbove(self, still, moving):
		moving.move(moving.pos().x(), still.pos().y() - moving.height())

	# Place the widget moving right below the widget still
	def rightBelow(self, still, moving):
		moving.move(moving.pos().x(), still.pos().y() + still.height())

	# Place the widget moving to the right of the widget still
	def toRight(self, still, moving):
		moving.move(still.pos().x() + still.width(), moving.pos().y())

	# Place the widget moving to the left of the widget still
	def toLeft(self, still, moving):
		moving.move(still.pos().x() - moving.width(), moving.pos().y())

	# Align the left of moving with the left of still
	def leftWidgetAlign(self, still, moving):
		moving.move(still.pos().x(), moving.pos().y())

	# Align the right of moving with the right of still
	def rightWidgetAlign(self, still, moving):
		moving.move(still.pos().x() - (moving.width() - still.width()), moving.pos().y())

	# Align the top of moving with the top of still
	def topWidgetAlign(self, still, moving):
		moving.move(moving.pos().x(), still.pos().y())

	# Align the bottom of moving with the bottom of still
	def bottomWidgetAlign(self, still, moving):
		moving.move(moving.pos().x(), still.pos().y() - (moving.height() - still.height()))

	# Align the center of the width of moving with the center of the width of still
	def centerXWidgetAlign(self, still, moving):
		moving.move(still.pos().x() - (moving.width() / 2 - still.width() / 2), moving.pos().y())

	# Align the center of the height of moving with the center of the height of still
	def centerYWidgetAlign(self, still, moving):
		moving.move(moving.pos().x(), still.pos().y() - (moving.height() / 2 - still.height() / 2))

	# Place the center of the height of name at the yValue
	def centerYAlign(self, widget, yValue):
		widget.move(widget.pos().x(), yValue - widget.height() / 2)

	# Place the center of the width of name at the xValue
	def centerXAlign(self, widget, xValue):
		widget.move(xValue - widget.width() / 2, widget.pos().y())

	# Place the top of name at the yValue
	def topYAlign(self, widget, yValue):
		widget.move(widget.pos().x(), yValue)

	# Place the left of name at the xValue
	def leftXAlign(self, widget, xValue):
		widget.move(xValue, widget.pos().y())

	# Place the bottom of name at the yValue
	def bottomYAlign(self, widget, yValue):
		widget.move(widget.pos().x(), yValue - widget.height())

	# Place the right of name at the xValue
	def rightXAlign(self, widget, xValue):
		widget.move(xValue - widget.width(), widget.pos().y())

	# Set the text of name (takes care of adjusting the size)
	def setText(self, widget, text):
		widget.setText(text)
		widget.adjustSize()

	# Adjust the size of the window to fit the widgets
	def adjustSize(self, widgets):
		maxX = 0
		maxY = 0
		for i in widgets:
			x = widgets[i].pos().x() + widgets[i].width()
			y = widgets[i].pos().y() + widgets[i].height()
			if x > maxX:
				maxX = x
			if y > maxY:
				maxY = y
		self.windowWidth = maxX
		self.windowHeight = maxY
		return maxX, maxY
