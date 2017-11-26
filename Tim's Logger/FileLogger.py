from datetime import datetime

# Log a number and date to a file
def log(file, number, date, increase):

	# Ensure that each input has something in it
	if len(file) == 0:
		file = "default"
	if len(number) == 0:
		number = "0"
	if len(date) == 0:
		date = "1/1/2001"

	# Test that the number and date inputs are an integer and a date
	try:
		int(number)
		datetime.strptime(date, "%m/%d/%Y")

		# Open the file or create it and then open it if it does not already exist
		try:
			f = open(file, "r+")
		except Exception as e:
			f = open(file, "a")
			f.close()
			f = open(file, "r+")

		# Find entries in the file that already contain this date if any exist
		if increase:
			go_to_line_number = 0
			while True:
				go_to_line_number = f.tell()
				line = f.readline()
				if line == "":
					break
				s = line.split(",")
				if len(s) == 2 and s[1][:-1] == date:
					number = str(int(number) + int(s[0]))
					break

			# Go to the correct location in the file and write the number and date
			f.seek(go_to_line_number)
		else:
			f.seek(0, 2)
		f.write(number + "," + date + "\n")
		f.close()
	except Exception as e:
		print(e)

# Get a number from a file based on date
def read_number(file, date):

	# Ensure that each input has something in it
	if len(file) == 0:
		file = "default"
	if len(date) == 0:
		date = "1/1/2001"

	# Test that the date is a date
	try:
		datetime.strptime(date, "%m/%d/%Y")

		# Open the file or just return None
		try:
			f = open(file, "r")
		except Exception as e:
			return None

		# Find the entry, if it exists, and return it
		while True:
			line = f.readline()
			if line == "":

				# If we have not found the date in the whole file then just return None
				return None
			s = line.split(",")
			if len(s) == 2 and s[1][:-1] == date:
				return s[0]
	except Exception as e:
		print(e)

# Get a list of dates from a file based on number
def read_date(file, number):

	# Ensure that each input has something in it
	if len(file) == 0:
		file = "default"
	if len(number) == 0:
		number = "0"

	# Test that the number is a number
	try:
		int(number)

		# Open the file or just return nothing
		try:
			f = open(file, "r")
		except Exception as e:
			return []

		dates = []

		# Find the entry, if it exists, and return it
		while True:
			line = f.readline()
			if line == "":

				# If we have not found the date in the whole file then just return nothing
				break
			s = line.split(",")
			if len(s) == 2 and s[0] == number:
				dates.append(s[1][:-1])
		return dates
	except Exception as e:
		print(e)