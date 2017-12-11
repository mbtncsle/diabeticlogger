from module_references import *


class GraphWindow(QMdiSubWindow):

    def __init__(self):
        super(GraphWindow, self).__init__(parent=None)

        # Prepare the window
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Setup constants
        self.types = ["Blood Glucose Level", "Hours of Sleep", "Steps Walked", "Carbohydrate Intake"]
        self.blood_glucose = 1
        self.sleep = 2
        self.exercise = 3
        self.food_list = 4
        self.data = self.blood_glucose

        self.graph = PlotCanvas(self)
        #self.graph.setGeometry(0, 0, 550, 320)
        self.graph.setGeometry(0, 0, 1100, 320)

        self.show()

    # Change which data is graphed
    def change_data(self, data):
        self.data = data

    # Get data and graph it
    def update(self, previous_days):

        if self.data == self.blood_glucose:
            yl = "Blood Glucose"

            max_value = 300
            y_axis = {"upper": [], "data": [], "lower": []}
            x_axis = {"upper": [], "data": [], "lower": []}
            colors = {"upper": "r-", "data": "b-", "lower": "g-"}
            labels = {"upper": "Upper Bound", "data": yl, "lower": "Lower Bound"}

            upper = 150.0
            lower = 75.0
            for log in blood_glucose_crud.blood_glucose_select_by_days(previous_days):
                axis_date = log.record_date.strftime("%x")
                if not (axis_date in x_axis["data"]):
                    x_axis["upper"].append(axis_date)
                    y_axis["upper"].append([upper])
                    x_axis["lower"].append(axis_date)
                    y_axis["lower"].append([lower])
                    x_axis["data"].append(axis_date)
                    y_axis["data"].append([log.reading])
                else:
                    y_axis["upper"][x_axis["upper"].index(axis_date)].append(upper)
                    y_axis["data"][x_axis["data"].index(axis_date)].append(log.reading)
                    y_axis["lower"][x_axis["lower"].index(axis_date)].append(lower)

            for i in range(0, len(y_axis["data"])):
                total = 0
                uppertotal = 0
                lowertotal = 0

                for y in y_axis["upper"][i]:
                    uppertotal += y
                for y in y_axis["data"][i]:
                    total += y
                for y in y_axis["lower"][i]:
                    lowertotal += y

                uppertotal /= len(y_axis["upper"][i])
                total /= len(y_axis["data"][i])
                lowertotal /= len(y_axis["lower"][i])

                y_axis["upper"][i] = uppertotal
                y_axis["data"][i] = total
                y_axis["lower"][i] = lowertotal

        # Sleep
        elif self.data == self.sleep:
            yl = "Hours Slept"

            max_value = 24
            y_axis = {"upper": [], "data": []}
            x_axis = {"upper": [], "data": []}
            colors = {"upper": "r-", "data": "b-"}
            labels = {"upper": "Recommended", "data": yl}

            upper = 8
            for log in sleep_crud.sleep_select_by_days(previous_days):
                axis_date = log.record_date.strftime("%x")
                if not (axis_date in x_axis["data"]):
                    x_axis["upper"].append(axis_date)
                    y_axis["upper"].append([upper])
                    x_axis["data"].append(axis_date)
                    y_axis["data"].append([log.reading])
                else:
                    y_axis["upper"][x_axis["upper"].index(axis_date)].append(upper)
                    y_axis["data"][x_axis["data"].index(axis_date)].append(log.reading)

        # Steps
        elif self.data == self.exercise:
            yl = "Steps Walked"

            max_value = 20000
            y_axis = {"upper": [], "data": []}
            x_axis = {"upper": [], "data": []}
            colors = {"upper": "r-", "data": "b-"}
            labels = {"upper": "Recommended", "data": yl}

            upper = 5000

            for log in steps_crud.steps_select_by_days(previous_days):
                axis_date = log.record_date.strftime("%x")
                if not (axis_date in x_axis["data"]):
                    x_axis["upper"].append(axis_date)
                    y_axis["upper"].append([upper])
                    x_axis["data"].append(axis_date)
                    y_axis["data"].append([log.reading])
                else:
                    y_axis["data"][x_axis["data"].index(axis_date)][0] += log.reading
        # Carbs
        else:

            yl = "Carbohydrate Intake"

            max_value = 500
            y_axis = {"upper": [], "data": []}
            x_axis = {"upper": [], "data": []}
            colors = {"upper": "r-", "data": "b-"}
            labels = {"upper": "Recommended", "data": yl}

            upper = 250

            for log in meal_crud.meal_select_by_days(previous_days):
                axis_date = log.record_date.strftime("%x")
                if not (axis_date in x_axis["data"]):
                    x_axis["upper"].append(axis_date)
                    y_axis["upper"].append([upper])
                    x_axis["data"].append(axis_date)
                    y_axis["data"].append([log.reading])
                else:
                    y_axis["data"][x_axis["data"].index(axis_date)][0] += log.reading

        self.graph.plot(x_axis, y_axis, yl, "", colors, labels, max_value)

    def update_sort(self, m, two):
        if len(m) <= 1:
            return m, two

        middle = len(m) // 2
        left = m[:middle]
        right = m[middle:]

        left, l = self.update_sort(left, two[:middle])
        right, r = self.update_sort(right, two[middle:])
        final_m = []
        final_two = []
        li = 0
        ri = 0
        while li < len(left) and ri < len(right):
            if left[li] < right[ri]:
                final_m.append(left[li])
                final_two.append(l[li])
                li += 1
            else:
                final_m.append(right[ri])
                final_two.append(r[ri])
                ri += 1
        if li < len(left):
            final_m.extend(left[li:])
            final_two.extend(l[li:])
        elif ri < len(right):
            final_m.extend(right[ri:])
            final_two.extend(r[ri:])
        return final_m, final_two


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig = plt.figure()
        self.fig.subplots_adjust(top=.9, bottom=0.2)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def plot(self, x_axis, y_axis, ylabel, xlabel, colors, labels, max_value):

        self.axes.clear()
        self.axes.set_ylim((0, max_value))

        for k in y_axis:
            if len(y_axis[k]) > 0:
                self.axes.plot(x_axis[k], y_axis[k], colors[k], label=labels[k])

        self.axes.legend()
        self.axes.set_ylabel(ylabel)
        self.axes.set_xlabel(xlabel)
        self.fig.autofmt_xdate()
        self.draw()
