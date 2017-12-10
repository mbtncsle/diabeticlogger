from module_references import *

table_name = "Sleep"


class SleepRecord:
    """
    Sleep record class with constructor
    """
    def __init__(self, sleep_id=-1, reading=0, record_date=datetime.now(), notes=""):
        self.sleep_id = sleep_id
        self.reading = reading
        self.record_date = record_date
        self.notes = notes


# ==============================================================================
# Sleep record operations
# ==============================================================================
def sleep_insert(sleep_record):
    """
    Inserts a sleep record
    :param sleep_record: SleepRecord instance
    :return: SleepId of inserted record
    """

    sql_statement = "INSERT INTO " + table_name + " (Reading, RecordDate, Notes) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += str(sleep_record.reading) + ", "
    sql_statement += "'" + sleep_record.record_date.strftime("%Y-%m-%d %H:%M:%S") + "', "
    sql_statement += "'" + str(sleep_record.notes) + "'"
    sql_statement += ");"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_id = cursor.fetchone()[0]
        return return_id


def sleep_select_by_id(sleep_id):
    """
    Returns a sleep record based on SleepId
    :param sleep_id: SleepId of record
    :return: SleepRecord instance
    """

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes FROM " +\
                    table_name + " WHERE " + table_name + "Id = " + str(sleep_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return SleepRecord(
                sleep_id=row.SleepId,
                reading=row.Reading,
                record_date=row.RecordDate,
                notes=row.Notes
            )
        else:
            return None


def sleep_select_by_days(days):
    """
    Returns a list of records from the previous number of days specified
    :param days: days in the past to include
    :return: List of SleepRecords
    """
    oldest_date = datetime.today() - timedelta(days=days)

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes" + \
                    " FROM " + table_name + " WHERE RecordDate > \'{0}\' ORDER BY RecordDate DESC ;".format(
                        oldest_date.strftime("%Y-%m-%d 00:00:00"))

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_sleep_records = []
        row = cursor.fetchone()

        while row:
            return_sleep_records.append(
                SleepRecord(
                    sleep_id=row.SleepId,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_sleep_records


def select_by_date(start_date, include_days):
    """
    Returns a list of records from the date specified backwards in time for the number of days specified
    :param start_date: Date to start from and go back in time
    :param include_days: days in the past to include
    :return: List of SleepRecords
    :return: List of SleepRecords
    """
    oldest_date = start_date - timedelta(days=include_days)

    sql_statement = "SELECT " + table_name + "Id, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE RecordDate >= '" + oldest_date.strftime("%Y-%m-%d 00:00:00' ") +\
                    "AND RecordDate <= '" + start_date.strftime("%Y-%m-%d 23:59:59' ") +\
                    "ORDER BY RecordDate DESC;"

    print(sql_statement)

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_sleep_records = []
        row = cursor.fetchone()

        while row:
            return_sleep_records.append(
                SleepRecord(
                    sleep_id=row.SleepId,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes
                )
            )
            row = cursor.fetchone()

    return return_sleep_records


def sleep_delete(sleep_id):
    """
    Deletes a sleep record based on SleepId
    :param sleep_id: SleepId of record
    :return: row count is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(sleep_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return 0
