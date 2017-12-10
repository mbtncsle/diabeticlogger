from module_references import *

table_name = "Recommendation"


class RecommendationRecord:
    """
    Recommendation record class with constructor
    """

    def __init__(self, recommendation_id=-1,
                 recommendation_type="",
                 lower_bound=0,
                 upper_bound=999999,
                 recommendation="",
                 use_count=0):
        self.recommendation_id = recommendation_id
        self.recommendation_type = recommendation_type
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.recommendation = recommendation
        self.use_count = use_count


# ==============================================================================
# Recommendation record operations
# ==============================================================================
def recommendation_insert(recommendation_record):
    """
    Inserts a recommendation record
    :param recommendation_record: RecommendationRecord instance
    :return: recommendationId of inserted record
    """

    sql_statement = "INSERT INTO " + table_name + \
                    " (RecommendationType, LowerBound, UpperBound, Recommendation, UseCount) OUTPUT INSERTED."
    sql_statement += table_name + "Id"
    sql_statement += " VALUES ("
    sql_statement += "'" + str(recommendation_record.recommendation_type) + "', "
    sql_statement += str(recommendation_record.lower_bound) + ", "
    sql_statement += str(recommendation_record.upper_bound) + ", "
    sql_statement += "'" + recommendation_record.recommendation + "', "
    sql_statement += str(recommendation_record.use_count)
    sql_statement += ");"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        return_id = cursor.fetchone()[0]
        return return_id


def recommendation_select_by_id(recommendation_id):
    """
    Returns a recommendation record based on RecommendationId
    :param recommendation_id: RecommendationId of record
    :return: RecommendationRecord instance
    """

    sql_statement = "SELECT " + table_name + \
                    "Id, RecommendationType, LowerBound, UpperBound, Recommendation, UseCount FROM " + \
                    table_name + " WHERE " + table_name + "Id = " + str(recommendation_id) + ";"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return RecommendationRecord(
                recommendation_id=row.RecommendationId,
                recommendation_type=row.RecommendationType,
                lower_bound=row.LowerBound,
                upper_bound=row.UpperBound,
                recommendation=row.Recommendation,
                use_count=row.UseCount
            )
        else:
            return None


def recommendation_select_by_bounds(reading, recommendation_type):
    """
    Returns a list of records based on a reading
    :param reading: reading from blood glucose, steps, sleep, or meal
    :param recommendation_type: "blood_glucose", "steps", "sleep", "meal"
    :return: List of recommendationRecords
    """
    sql_statement = "SELECT " + table_name + \
                    "Id, RecommendationType, LowerBound, UpperBound, Recommendation, UseCount" + \
                    " FROM " + table_name + " WHERE (LowerBound <= " + str(reading) + \
                    " AND UpperBound >= " + str(reading) + ") AND RecommendationType = '" + str(recommendation_type) + \
                    "';"

    with db.Db() as cursor:
        try:
            cursor.execute(sql_statement)
        except pyodbc.Error as ex:
            print(ex.args)
            return None

        row = cursor.fetchone()

        if row:
            return_record = RecommendationRecord(
                recommendation_id=row.RecommendationId,
                recommendation_type=row.RecommendationType,
                lower_bound=row.LowerBound,
                upper_bound=row.UpperBound,
                recommendation=row.Recommendation,
                use_count=row.UseCount
            )

            return return_record
        else:
            return None


def recommendation_delete(recommendation_id):
    """
    Deletes a recommendation record based on recommendationId
    :param recommendation_id: recommendationId of record
    :return: row count is returned
    """

    sql_statement = "DELETE FROM " + table_name + " WHERE " + table_name + "Id = " + str(recommendation_id) + ";"

    with db.Db() as cursor:
        try:
            return cursor.execute(sql_statement).rowcount
        except pyodbc.Error as ex:
            print(ex.args)
            return 0
