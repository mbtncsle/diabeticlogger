import pyodbc
import datetime
from database_files import db
from database_files import meal_item_crud

table_name = "Meal"


class MealRecord:
    """
    Meal record class with constructor
    """

    def __init__(self, meal_id=-1, meal="", reading=0, record_date=datetime.datetime.now(), notes="", meal_items=None):
        self.meal_id = meal_id
        self.meal = meal
        self.reading = reading
        self.record_date = record_date
        self.notes = notes

        if meal_items is None:
            self.meal_items = []


# ==============================================================================
# Meal & Meal Item record operations
# ==============================================================================
def meal_insert(meal_record):
    """
    Inserts a meal record
    :param meal_record: MealRecord instance
    :return: MealId of inserted record
    """

    sql_statement = "INSERT INTO " + table_name + " (Meal, Reading, RecordDate, Notes) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += "'" + str(meal_record.meal) + "', "
    sql_statement += str(meal_record.reading) + ", "
    sql_statement += "'" + meal_record.record_date.strftime("%Y-%m-%d %H:%M:%S") + "', "
    sql_statement += "'" + str(meal_record.notes) + "'"
    sql_statement += ");"

    # Insert the meal record
    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_id = cursor.fetchone()[0]

    # Insert the meal item records
    for meal_item in meal_record.meal_items:
        meal_item.meal_id = return_id
        meal_item_crud.meal_item_insert(meal_item)

    return return_id


def meal_select_by_id(meal_id):
    """
    Returns a meal record based on MealId
    :param meal_id: StepsId of record
    :return: StepsRecord instance
    """

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE " + table_name + "Id = " + \
                    str(meal_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return MealRecord(
                meal_id=row.MealId,
                meal=row.Meal,
                reading=row.Reading,
                record_date=row.RecordDate,
                notes=row.Notes,
                meal_items=meal_item_crud.meal_items_select_by_meal_id(row.MealId)
            )
        else:
            return None


def meal_select_by_days(days):
    """
    Returns a list of records from the previous number of days specified
    :param days: days in the past to include
    :return: List of MealRecords
    """
    oldest_date = datetime.datetime.today() - datetime.timedelta(days=days)

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes" + \
                    " FROM " + table_name + " WHERE RecordDate > \'{0}\' ORDER BY RecordDate DESC ;".format(
                        oldest_date.strftime("%Y-%m-%d 00:00:00"))

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_meal_records = []
        row = cursor.fetchone()

        while row:
            return_meal_records.append(
                MealRecord(
                    meal_id=row.MealId,
                    meal=row.Meal,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes,
                    meal_items=meal_item_crud.meal_items_select_by_meal_id(row.MealId)
                )
            )
            row = cursor.fetchone()

    return return_meal_records


def meal_select_by_date(start_date, include_days):
    """
    Returns a list of records from the date specified backwards in time for the number of days specified
    :param start_date: Date to start from and go back in time
    :param include_days: days in the past to include
    :return: List of MealRecords
    """
    oldest_date = start_date - datetime.timedelta(days=include_days)

    sql_statement = "SELECT " + table_name + "Id, Meal, Reading, RecordDate, Notes " + \
                    "FROM " + table_name + " WHERE RecordDate >= '" + oldest_date.strftime("%Y-%m-%d 00:00:00' ") + \
                    "AND RecordDate <= '" + start_date.strftime("%Y-%m-%d 23:59:59' ") + \
                    "ORDER BY RecordDate DESC;"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_meal_records = []
        row = cursor.fetchone()

        while row:
            return_meal_records.append(
                MealRecord(
                    meal_id=row.MealId,
                    meal=row.Meal,
                    reading=row.Reading,
                    record_date=row.RecordDate,
                    notes=row.Notes,
                    meal_items=meal_item_crud.meal_items_select_by_meal_id(row.MealId)
                )
            )
            row = cursor.fetchone()

    return return_meal_records


def meal_delete(meal_id):
    """
    Deletes a meal record and the associated meal item records based on MealId
    :param meal_id: MealId of record
    :return: row count is returned
    """

    # Delete the associated meal item records
    deleted_meal_item_count = meal_item_crud.meal_item_delete_by_meal_id(meal_id)
    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(meal_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount + deleted_meal_item_count
        except pyodbc.Error as ex:
            print(ex.args)
            return 0
