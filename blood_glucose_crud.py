from module_references import *


table_name = "BloodGlucose"


class BloodGlucoseRecord:
    """
    Blood Glucose record class with constructor
    """
    def __init__(self, blood_glucose_id=-1, meal="", reading=0, record_date=datetime.now(), notes=""):
        self.blood_glucose_id = blood_glucose_id
        self.meal = meal
        self.reading = reading
        self.record_date = record_date
        self.notes = notes


# ==============================================================================
# Blood Glucose record operations
# ==============================================================================
def blood_glucose_insert(blood_glucose_record):
    """
    Inserts a blood glucose record
    :param blood_glucose_record: Blo
    :return: BloodGlucoseId of inserted record
    """
    sql_statement = "INSERT INTO " + table_name + " (Meal, Reading, RecordDate, Notes) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += "'" + str(blood_glucose_record.meal) + "', "
    sql_statement += str(blood_glucose_record.reading) + ", "
    sql_statement += "'" + str(blood_glucose_record.record_date.strftime("%Y-%m-%d %H:%M:%S")) + "', "
    sql_statement += "'" + str(blood_glucose_record.notes) + "'"
    sql_statement += ");"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_id = cursor.fetchone()[0]
        return return_id


def blood_glucose_select_by_id(blood_glucose_id):
    """
    Returns a blood glucose record based on BloodGlucoseId
    :param blood_glucose_id: BloodGlucoseId of record
    :return: BloodGlucoseRecord instance
    """

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE " + table_name + "Id = " + \
                    str(blood_glucose_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return BloodGlucoseRecord(
                blood_glucose_id=row.BloodGlucoseId,
                meal=row.Meal,
                reading=row.Reading,
                record_date=row.RecordDate,
                notes=row.Notes
            )
        else:
            return None


def blood_glucose_select_by_days(days):
    """
    Returns a list of records from the previous number of days specified
    :param days: days in the past to include
    :return: List of BloodGlucoseRecords
    """
    oldest_date = datetime.today() - timedelta(days=days)

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes" + \
                    " FROM " + table_name + " WHERE RecordDate > \'{0}\' ORDER BY RecordDate DESC ;".format(
                        oldest_date.strftime("%Y-%m-%d 00:00:00"))

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_blood_glucose_records = []
        row = cursor.fetchone()

        while row:
            return_blood_glucose_records.append(
                BloodGlucoseRecord(
                    blood_glucose_id=row.BloodGlucoseId,
                    meal=row.Meal,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_blood_glucose_records


def select_by_date(start_date, include_days):
    """
    Returns a list of records from the date specified backwards in time for the number of days specified
    :param start_date: Date to start from and go back in time
    :param include_days: days in the past to include
    :return: List of BloodGlucoseRecords
    """
    oldest_date = start_date - timedelta(days=include_days)

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE RecordDate >= '" + oldest_date.strftime("%Y-%m-%d 00:00:00' ") +\
                    "AND RecordDate <= '" + start_date.strftime("%Y-%m-%d 23:59:59' ") +\
                    "ORDER BY RecordDate DESC;"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_blood_glucose_records = []
        row = cursor.fetchone()

        while row:
            return_blood_glucose_records.append(
                BloodGlucoseRecord(
                    blood_glucose_id=row.BloodGlucoseId,
                    meal=row.Meal,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_blood_glucose_records


def blood_glucose_delete(blood_glucose_id):
    """
    Deletes a blood glucose record based on BloodGlucoseId
    :param blood_glucose_id: BloodGlucoseId of record
    :return: row count is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(blood_glucose_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return None
