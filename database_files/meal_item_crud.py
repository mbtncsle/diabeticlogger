import pyodbc
from database_files import db

table_name = "MealItem"


class MealItemRecord:
    """
    Meal item record class with constructor
    """
    def __init__(self, meal_item_id=-1, meal_id=-1, description="", portions=0, carbs_per_portion=0, total_carbs=0):
        self.meal_item_id = meal_item_id
        self.meal_id = meal_id
        self.description = description
        self.portions = portions
        self.carbs_per_portion = carbs_per_portion
        self.total_carbs = total_carbs


# ==============================================================================
# Meal Item record operations
# ==============================================================================
def meal_item_insert(meal_item_record):
    """
    Inserts a meal item record
    :param meal_item_record: MealItemRecord instance
    :return: MealItemId of inserted record
    """

    sql_statement = "INSERT INTO " + table_name + \
                    " (MealId, Description, Portions, CarbsPerPortion, TotalCarbs) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += str(meal_item_record.meal_id) + ", "
    sql_statement += "'" + str(meal_item_record.description) + "', "
    sql_statement += str(meal_item_record.portions) + ", "
    sql_statement += str(meal_item_record.carbs_per_portion) + ", "
    sql_statement += str(meal_item_record.total_carbs)
    sql_statement += ");"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_id = cursor.fetchone()[0]
        return return_id


def meal_items_select_by_meal_id(meal_id):
    """
    Returns a list of records based on the MealId
    :param meal_id: MealId of meal to retrieve records for
    :return: List of MealRecords
    """
    sql_statement = "SELECT " + table_name + "Id, MealId, Description, Portions, CarbsPerPortion, TotalCarbs " + \
                    "FROM " + table_name + " WHERE MealId = " + \
                    str(meal_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return

        return_meal_items_records = []
        row = cursor.fetchone()

        while row:
            return_meal_items_records.append(
                MealItemRecord(
                    meal_item_id=row.MealItemId,
                    meal_id=row.MealId,
                    description=row.Description,
                    portions=row.Portions,
                    carbs_per_portion=row.CarbsPerPortion,
                    total_carbs=row.TotalCarbs
                )
            )
            row = cursor.fetchone()

    return return_meal_items_records


def meal_item_select_by_id(meal_item_id):

    """
    Returns a meal item record based on MealItemId
    :param meal_item_id: MealItemId of record
    :return: MealItemRecord instance
    """

    sql_statement = "SELECT " + table_name + "Id, MealId, Description, Portions, CarbsPerPortion, TotalCarbs " + \
                    "FROM " + table_name + " WHERE " + table_name + "Id = " + \
                    str(meal_item_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return MealItemRecord(
                meal_item_id=row.MealItemId,
                meal_id=row.MealId,
                description=row.Description,
                portions=row.Portions,
                carbs_per_portion=row.CarbsPerPortion,
                total_carbs=row.TotalCarbs
            )
        else:
            return None


def meal_item_delete(meal_item_id):
    """
    Deletes a meal item record based on MealItemId
    :param meal_item_id: MealItemId of record
    :return: Nothing is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(meal_item_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return 0


def meal_item_delete_by_meal_id(meal_id):
    """
    Deletes all meal item records for the associated MealId
    :param meal_id: MealId of record
    :return: row count is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE MealId = " + str(meal_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return 0
