from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QFormLayout, QHBoxLayout, QPushButton,\
     QMdiSubWindow, QCalendarWidget
import datetime


# =====================================
# Team: Vampires
# Diabetic Logger logging form
# =====================================
class Logger(QMdiSubWindow):
    metric_label = "Unknown"
    metric_uom = "UK"
    form_title = "Unknown"
    form_icon = "diabetic_logger.jpg"

    # =====================================
    # Diabetic Logger logging form
    # =====================================
    def __init__(self, logger_type):

        super(Logger, self).__init__(parent=None)

        # Setup labels, titles, window icons
        self.setup_labels(logger_type)

        # Widget placed on form that holds
        # all the controls
        log_widget = QWidget()

        # Metric boxes and labels
        form_layout = QFormLayout()

        # Setup the labels and textbox for the metric
        # that we are recording
        label_metric = QLabel(self.metric_label)
        self.textbox_metric = QLineEdit()
        label_uom = QLabel(self.metric_uom)
        label_date = QLabel("Date")
        self.textbox_date = QLineEdit(datetime.datetime.now().strftime("%m/%d/%Y"))
        calendar_date = QCalendarWidget()
        calendar_date.selectionChanged.connect(self.set_date)

        # Create a horizontal box layout and add the
        # controls to it
        horizontal_box = QHBoxLayout()

        # Adding the controls
        horizontal_box.addWidget(label_metric)
        horizontal_box.addWidget(self.textbox_metric)
        horizontal_box.addWidget(label_uom)
        horizontal_box.addWidget(label_date)
        horizontal_box.addWidget(self.textbox_date)
        horizontal_box.addWidget(calendar_date)

        # Add the horizontal box layout to
        # the form layout
        form_layout.addRow(horizontal_box)

        HBoxSubmit = QHBoxLayout()

        submit = QPushButton("Submit", self)
        submit.clicked.connect(self.log)

        HBoxSubmit.addWidget(submit)

        form_layout.addRow(HBoxSubmit)

        # ===================
        # Number pad setup
        # ===================
        buttons = {}
        row_layouts = {}
        row = 1

        # Add the buttons to the rows and rows to the layout
        for i in range(1, 10, 3):
            row_layouts[row] = QHBoxLayout()
            for j in range(i, i + 3):
                buttons[j] = QPushButton(str(j), self)
                buttons[j].clicked.connect(self.button_click)
                # buttons[j].clicked.connect(lambda: self.button_click(buttons[j], str(j)))
                row_layouts[row].addWidget(buttons[j])
            form_layout.addRow(row_layouts[row])
            row = row + 1

        # Zero is at the bottom by itself so it is
        # a special case
        # TODO: This needs to be cleaned up, too many magic numbers
        row_layouts[4] = QHBoxLayout()
        buttons[10] = QPushButton(str(0), self)
        buttons[10].clicked.connect(self.button_click)
        row_layouts[4].addStretch()
        row_layouts[4].addWidget(buttons[10])
        row_layouts[4].addStretch()
        form_layout.addRow(row_layouts[row])

        # Add the form layout to the form widget
        log_widget.setLayout(form_layout)

        # Set the form title and icon
        log_widget.setWindowTitle(self.form_title)
        self.setWindowIcon(QIcon(QPixmap(self.form_icon)))

        # set the widget on the form to this widget
        self.setWidget(log_widget)

    # Handles the button clicks from the numeric keypad
    @pyqtSlot()
    def button_click(self):
        metric_text = self.textbox_metric.text()
        text = self.sender().text()
        self.textbox_metric.setText(metric_text + text)

    @pyqtSlot()
    def set_date(self):
        date = self.sender().selectedDate().toString("M/d/yyyy")
        self.textbox_date.setText(date)

    # Sets up the labels, uom, title, and icon
    def setup_labels(self, logger_type):
        if logger_type == "blood_glucose":
            self.metric_label = "Blood Glucose"
            self.metric_uom = "mg/dL"
            self.form_title = "Blood Glucose"
            self.form_icon = "blood_glucose.jpg"
        elif logger_type == "steps":
            self.metric_label = "Steps"
            self.metric_uom = ""
            self.form_title = "Steps"
            self.form_icon = "steps.png"
        elif logger_type == "sleep":
            self.metric_label = "Sleep"
            self.metric_uom = "hours"
            self.form_title = "Sleep"
            self.form_icon = "sleep.png"
        elif logger_type == "carbohydrates":
            self.metric_label = "Carbohydrates"
            self.metric_uom = "grams"
            self.form_title = "Carbohydrates"
            self.form_icon = "carbohydrates.jpg"

    def log(self):
        # Get the text from the editing and date boxes
        temp_glucose = self.textbox_metric.text()
        temp_date = self.textbox_date.text()
        if len(temp_glucose) == 0:
            temp_glucose = "0"
        try:
            # Ensure that the format of the text is correct
            glucose = int(temp_glucose)
            date = datetime.datetime.strptime(temp_date, "%m/%d/%Y")
            try:
                f = open("glucose.txt", "r+")
            except Exception as e:
                f = open("glucose.txt", "a")
                f = open("glucose.txt", "r+")
            f.write(temp_glucose + "," + temp_date + "\n")
            f.close()
        except Exception as e:
            print(e)