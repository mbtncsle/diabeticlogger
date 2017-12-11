from module_references import *

table_name = "Steps"


class StepsRecord:
    """
    Steps record class with constructor
    """
    def __init__(self, steps_id=-1, reading=0, record_date=datetime.now(), notes=""):
        self.steps_id = steps_id
        self.reading = reading
        self.record_date = record_date
        self.notes = notes


# ==============================================================================
# Steps record operations
# ==============================================================================
def steps_insert(steps_record):
    """
    Inserts a step record
    :param steps_record: StepsRecord instance
    :return: StepsId of inserted record
    """

    sql_statement = "INSERT INTO " + table_name + " (Reading, RecordDate, Notes) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += str(steps_record.reading) + ", "
    sql_statement += "'" + steps_record.record_date.strftime("%Y-%m-%d %H:%M:%S") + "', "
    sql_statement += "'" + str(steps_record.notes) + "'"
    sql_statement += ");"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return sql_statement

        return_id = cursor.fetchone()[0]
        return return_id


def steps_select_by_id(steps_id):
    """
    Returns a steps record based on StepsId
    :param steps_id: StepsId of record
    :return: StepsRecord instance
    """

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE " + table_name + "Id = " + \
                    str(steps_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return StepsRecord(
                steps_id=row.StepsId,
                reading=row.Reading,
                record_date=row.RecordDate,
                notes=row.Notes
            )
        else:
            return None


def steps_select_by_days(days):
    """
    Returns a list of records from the previous number of days specified
    :param days: days in the past to include
    :return: List of StepsRecords
    """
    oldest_date = datetime.today() - timedelta(days=days)

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes" + \
                    " FROM " + table_name + " WHERE RecordDate > \'{0}\' ORDER BY RecordDate;".format(
                        oldest_date.strftime("%Y-%m-%d 00:00:00"))

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_steps_records = []
        row = cursor.fetchone()

        while row:
            return_steps_records.append(
                StepsRecord(
                    steps_id=row.StepsId,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_steps_records


def select_by_date(start_date, include_days):
    """
    Returns a list of records from the date specified backwards in time for the number of days specified
    :param start_date: Date to start from and go back in time
    :param include_days: days in the past to include
    :return: List of StepsRecords
    """
    oldest_date = start_date - timedelta(days=include_days)

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE RecordDate >= '" + oldest_date.strftime("%Y-%m-%d 00:00:00' ") + \
                    "AND RecordDate <= '" + start_date.strftime("%Y-%m-%d 23:59:59' ") + \
                    "ORDER BY RecordDate DESC;"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_steps_records = []
        row = cursor.fetchone()

        while row:
            return_steps_records.append(
                StepsRecord(
                    steps_id=row.StepsId,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_steps_records


def steps_delete(steps_id):
    """
    Deletes a steps record based on StepsId
    :param steps_id: StepsId of record
    :return: row count is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(steps_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return 0
