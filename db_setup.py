import datetime
import random
import pyodbc
import db
import blood_glucose_crud
import sleep_crud
import steps_crud
import meal_crud
import meal_item_crud

# Number of days to create records for
days_of_records = 90


# ==============================================================================
# Setup
# ==============================================================================
def setup():
    create_database()
    create_sleep_table()
    populate_sleep_table()
    create_steps_table()
    populate_steps_table()
    create_blood_glucose_table()
    populate_blood_glucose_table()
    create_meal_table()
    create_meal_items_table()
    populate_meal_tables()
    create_recommendation_table()


def create_database():
    """ Sets up the database """

    server_name = ".\SQLExpress"
    db_name = "DiabeticLogger"
    user_id = "sa"
    password = "Vampires6!"

    connection_string = "DRIVER={SQL Server Native Client 11.0};"
    connection_string += "SERVER=" + server_name + ";"
    connection_string += "DATABASE=master;"
    connection_string += "UID=" + user_id + ";"
    connection_string += "PWD=" + password

    create_sql_statement = "CREATE DATABASE " + db_name + ";"
    drop_sql_statement = "DROP DATABASE " + db_name + ";"

    try:
        connection = pyodbc.connect(connection_string, autocommit=True)
        cursor = connection.cursor()

    except pyodbc.Error as ex:
        print(ex.args)
        return

    try:
        cursor.execute(create_sql_statement)
    except pyodbc.Error as ex:
        cursor.execute(drop_sql_statement)
        cursor.execute(create_sql_statement)
        print(ex.args)
    finally:
        cursor.close()
        del cursor
        connection.close()


def create_sleep_table():
    """ Create the sleep table """

    table_name = "[dbo].[Sleep]"
    field_list = [
        "[SleepId] [int] IDENTITY(1,1) NOT NULL",
        "[Reading] [float] NOT NULL",
        "[RecordDate] [datetime] NOT NULL",
        "[Notes] [nvarchar](255) NULL",
        "PRIMARY KEY CLUSTERED([SleepId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def populate_sleep_table():
    """ Populates the sleep table"""
    for day in range(days_of_records):
        sleep_hours = random.randint(500, 900) / 100
        sleep_crud.sleep_insert(
            sleep_crud.SleepRecord(reading=sleep_hours,
                                   record_date=datetime.datetime.today() - datetime.timedelta(days=day),
                                   notes="Slept for " + str(sleep_hours) + " hours")
        )


def create_steps_table():
    """ Create the steps table """

    table_name = "[dbo].[Steps]"
    field_list = [
        "[StepsId] [int] IDENTITY(1,1) NOT NULL",
        "[Reading] [int] NOT NULL",
        "[RecordDate] [datetime] NOT NULL",
        "[Notes] [nvarchar](255) NULL",
        "PRIMARY KEY CLUSTERED([StepsId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def populate_steps_table():
    """ Populates the steps table """

    for day in range(days_of_records):
        steps = random.randint(5000, 10000)
        steps_crud.steps_insert(
            steps_crud.StepsRecord(reading=steps,
                                   record_date=datetime.datetime.today() - datetime.timedelta(days=day),
                                   notes="Walked " + str(steps) + " steps")
        )


def create_blood_glucose_table():
    """ Create the blood glucose table """

    table_name = "[dbo].[BloodGlucose]"
    field_list = [
        "[BloodGlucoseId] [int] IDENTITY(1,1) NOT NULL",
        "[Meal] [nvarchar](20) NOT NULL",
        "[Reading] [int] NOT NULL",
        "[RecordDate] [datetime] NOT NULL",
        "[Notes] [nvarchar](255) NULL",
        "PRIMARY KEY CLUSTERED([BloodGlucoseId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def populate_blood_glucose_table():
    """ Populates the blood glucose table """

    meals = [
        ["Before Breakfast", "7:00:00"],
        ["After Breakfast", "9:00:00"],
        ["Before Lunch", "11:00:00"],
        ["After Lunch", "13:00:00"],
        ["Before Dinner", "17:00:00"],
        ["After Dinner", "19:00:00"],
    ]

    for day in range(days_of_records):
        for meal in meals:
            blood_glucose = random.randint(80, 200)
            record_date = (datetime.datetime.today() - datetime.timedelta(days=day)).strftime("%m-%d-%Y")
            record_time = meal[1]
            record_date_time_string = record_date + " " + record_time
            record_date_time = datetime.datetime.strptime(record_date_time_string, "%m-%d-%Y %H:%M:%S")

            blood_glucose_crud.blood_glucose_insert(
                blood_glucose_crud.BloodGlucoseRecord(
                    meal=meal[0],
                    reading=blood_glucose,
                    record_date=record_date_time,
                    notes="Blood Glucose " + str(blood_glucose) + "mg/dL " + meal[0])
            )


def create_meal_table():
    """ Create the meal table """

    table_name = "[dbo].[Meal]"
    field_list = [
        "[MealId] [int] IDENTITY(1,1) NOT NULL",
        "[Meal] [nvarchar](20) NOT NULL",
        "[Reading] [int] NOT NULL",
        "[RecordDate] [datetime] NOT NULL",
        "[Notes] [nvarchar](255) NULL",
        "PRIMARY KEY CLUSTERED([MealId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def create_meal_items_table():
    """ Create the meal items table """

    table_name = "[dbo].[MealItem]"
    field_list = [
        "[MealItemId] [int] IDENTITY(1,1) NOT NULL",
        "[MealId] [int] NOT NULL",
        "[Description] [nvarchar](255) NOT NULL",
        "[Portions] [float] NOT NULL",
        "[CarbsPerPortion] [int] NOT NULL",
        "[TotalCarbs] [int] NOT NULL",
        "PRIMARY KEY CLUSTERED([MealItemId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def populate_meal_tables():
    """ Populates the meal and meal items tables """

    meals = [
        ["Breakfast", "8:00:00"],
        ["Snack", "10:00:00"],
        ["Lunch", "12:00:00"],
        ["Snack", "15:00:00"],
        ["Dinner", "18:00:00"],
    ]

    meal_items_list = [
        ["Bagel – Lender’s frozen(1 plain bagel)", 30],
        ["Bagel – Panera(1 plain bagel)", 60],
        ["Bread(1 regular slice)", 23],
        ["Bread Stuffing(½ Cup)", 20],
        ["Breadstick-soft(1 bread stick)", 25],
        ["Bun: Hamburger or Hot dog(1 regular size)", 30],
        ["Corn Bread(2in cube)", 15],
        ["Croissant(Medium 2 oz)", 25],
        ["Croutons: from Italian Restaurant(½ Cup)", 15],
        ["Croutons: pkg from fast food restaurant(1 pkg)", 10],
        ["Dinner Roll(Small)", 15],
        ["English Muffin(1 whole)", 30],
        ["Pancake(6in diameter (avg size))", 30],
        ["Pita bread(Large 6in-9in)", 45],
        ["Tortilla-corn(7in)", 15],
        ["Waffle (frozen type)(1)", 15],
        ["Beans: refried(½ Cup)", 18],
        ["Oatmeal, cooked(½ Cup)", 10],
        ["Cream of Wheat, cooked(½ Cup)", 15],
        ["Cornmeal: dry(3 Tbsp)", 15],
        ["Beans/legumes/lentils as prepared(½ Cup)", 15],
        ["Flour: dry(3 Tbsp)", 15],
        ["Hummus(½ Cup)", 15],
        ["Pasta, cooked(1 Cup)", 45],
        ["Rice, cooked(1 Cup)", 45],
        ["Corn: cooked or canned(½ Cup)", 15],
        ["Corn Cob(6in-9in)", 45],
        ["Peas(½ Cup)", 15],
        ["Potato – Wendy’s(Avg baked (10 oz))", 60],
        ["Potatoes (hashed, mashed)(½ Cup)", 15],
        ["Squash (winter type: acorn, Hubbard, etc)(1 Cup)", 30],
        ["Sweet Potato/Yams-plain cooked(10oz baked)", 60],
        ["Cow’s milk (fat-free, 1%, 2%, Whole)(1 Cup)", 12],
        ["Rice Milk-Plain(1 Cup)", 20],
        ["Soy Milk (plain)(1 Cup)", 8],
        ["Yogurt (plain)(1 Cup)", 12],
        ["Yogurt- Dannon Light & Fit(1 serving (6oz))", 10],
        ["Yogurt-Yoplait Light (blue top)(1 serving (6 oz))", 19],
        ["Apple(4-8 oz)", 30],
        ["Applesauce-unsweetened(½ Cup)", 15],
        ["Apricots, dried(7 pieces)", 15],
        ["Banana(6in – 9in)", 45],
        ["Blackberries, Blueberries(1 Cup)", 20],
        ["Canned Fruit Cocktail-in its own juice(½ Cup)", 15],
        ["Cantaloupe, Honeydew Melons(1 Cup)", 15],
        ["Cherries(12)", 15],
        ["Dates-dried Medjool type(1)", 15],
        ["Grapefruit(½ Large)", 15],
        ["Grapes(15 small)", 15],
        ["Kiwi(1 small)", 15],
        ["Orange(1 medium)", 15],
        ["Peaches (canned-in its own juice)(½ Cup)", 15],
        ["Pear(6 oz)", 20],
        ["Pineapple(1 Cup diced)", 20],
        ["Prunes- dried(3)", 15],
        ["Raisins(35 or 1/8 Cup or 2 Tbsp.)", 15],
        ["Raspberries(1 Cup)", 15],
        ["Strawberries-fresh(1 Cup halves)", 12],
        ["Watermelon(1 Cup diced)", 12],
        ["Apple Juice 100%(½ Cup)", 15],
        ["Carrot Juice(1 Cup)", 12],
        ["Cranberry Juice Cocktail 100%(½ Cup)", 12],
        ["Cranberry Juice Cocktail- Light(1 Cup)", 10],
        ["Grape Juice 100%(½ Cup (4 oz))", 15],
        ["Orange Juice(½ Cup)", 13],
        ["Tomato or V8 juice(1 Cup (8oz))", 10],
        ["Biscuit (large Bob Evans)(1)", 30],
        ["Biscuit (small Pillsbury)(1)", 10],
        ["Brownie-large (Zimmerman’s)(1)", 70],
        ["Cake 2 layer frosted(4in square)", 80],
        ["Chocolate Chip cookie-refrigerator dough(1)", 15],
        ["Cupcake with frosting (Hostess)(1)", 30],
        ["Danish (large bakery type)(1)", 45],
        ["Donut (Dunkin Donuts-plain or jelly filled)(1)", 40],
        ["Donut (Krispy Kreme)(1)", 20],
        ["Apple Crisp(½ Cup)", 70],
        ["Fruit pie(1/8 of 9in pie)", 50],
        ["Muffin (homemade standard size)(1)", 30],
        ["Muffins (bakery type)(1)", 75],
        ["Dark Chocolate(1 oz)", 15],
        ["Dove Chocolate(3 pieces)", 15],
        ["French Fries-crinkle cut frozen type(10)", 15],
        ["French Fries-diner style(Side order)", 60],
        ["French Fries-fast food(Small order)", 30],
        ["Graham Cracker(3 squares)", 15],
        ["Granola: SEE LABEL(½ Cup)", 45],
        ["Hershey Kisses(5)", 15],
        ["Ice Cream- No Sugar Added(½ Cup)", 15],
        ["Ice Cream- plain vanilla(½ Cup)", 15],
        ["Jell-O(½ Cup)", 20],
        ["Jell-O-Sugar Free(½ Cup)", 0],
        ["Oyster Crackers(½ Cup)", 15],
        ["Popcorn(3 Cups)", 15],
        ["Potato Chips(1 oz (10-15 chips))", 15],
        ["Pretzels(11 small)", 15],
        ["Pudding-Regular(1 snack pack)", 30],
        ["Pudding-Sugar Free(1 snack pack)", 15],
        ["Saltine Crackers(7 squares)", 15],
        ["Sherbet(½ Cup)", 30],
        ["Sorbet(½ Cup)", 40],
        ["Tortilla Chips(1 oz (10-15 chips))", 20],
        ["Apple Butter(2 Tbsp)", 15],
        ["Barbeque Sauce BBQ(2 Tbsp)", 15],
        ["Cranberry Sauce-jellied(¼ Cup)", 25],
        ["Fat Free Mayo/Salad Dressing(2 Tbsp)", 5],
        ["Fruit Jam or Jelly(1 Tbsp)", 15],
        ["Fruit Spread- Jam- 100% Fruit-less sugar(1 Tbsp)", 10],
        ["Fruit Spread-Jams-Sugar Free(1 Tbsp)", 5],
        ["Gravy-brown prepared from mix(1 Cup)", 15],
        ["Hoisin Sauce(2 Tbsp)", 15],
        ["Hollandaise Sauce made from mix(2 Tbsp)", 5],
        ["Honey(1 Tbsp)", 15],
        ["Honey Mustard(2 Tbsp)", 7],
        ["Ketchup(¼ Cup)", 15],
        ["Marinara Sauce(½ Cup)", 15],
        ["Plum Sauce(2 Tbsp)", 15],
        ["Ranch- fat free(2 Tbsp)", 8],
        ["Ranch- regular(2 Tbsp)", 2],
        ["Sloppy Joe Sauce(¼ Cup)", 15],
        ["Sugar(1 Tbsp)", 15],
        ["Sweet and Sour Sauce(2-3 Tbsp)", 15],
        ["Syrup(1 Tbsp)", 15],
        ["Syrup- Lite(2 Tbsp)", 15],
        ["Szechuan sauce(1/3 Cup)", 15],
        ["Bean Soup (split pea, lentil, etc)(1 Cup)", 30],
        ["Beans & Cheese Burrito- avg frozen type(6 oz)", 60],
        ["Cabbage Roll with meat and rice(1 avg roll)", 15],
        ["Chicken Noodle Soup- from can(1 Cup)", 15],
        ["Chili with beans & meat(1 Cup)", 25],
        ["Chili-vegetarian(1 Cup)", 50],
        ["Cream Soup(1 Cup)", 15],
        ["Dumpling- Chinese type(3)", 20],
        ["Egg Roll(1 avg roll)", 25],
        ["Lasagna from restaurant(Avg serving)", 80],
        ["Macaroni & Cheese(1 Cup)", 45],
        ["Pizza (individual pan)(1 whole pizza)", 75],
        ["Pizza 12in(1 avg slice)", 30],
        ["Pot pie (small frozen)(1)", 30],
        ["Red Beans & Rice(1 Cup)", 45],
        ["Tuna Noodle Casserole(1 Cup)", 30],
    ]

    for day in range(days_of_records):
        for meal in meals:
            meal_items_count = random.randint(0, 1)
            record_date = (datetime.datetime.today() - datetime.timedelta(days=day)).strftime("%m-%d-%Y")
            record_time = meal[1]
            record_date_time_string = record_date + " " + record_time
            record_date_time = datetime.datetime.strptime(record_date_time_string, "%m-%d-%Y %H:%M:%S")

            meal_record = meal_crud.MealRecord(
                meal=meal[0],
                reading=0,
                record_date=record_date_time,
                notes=meal[0] + " for " + str(record_date_time)
            )

            if meal_items_count == 0:
                carb_intake = random.randint(200, 300)
            else:
                # Create a meal item record
                carb_intake = 0
                for count in range(1, meal_items_count + 1):
                    index = random.randint(0, 139)
                    portions = 1
                    carbs_per_portion = meal_items_list[index][1]
                    carb_intake += portions*carbs_per_portion
                    meal_record.meal_items.append(meal_item_crud.MealItemRecord(
                        description=meal_items_list[index][0],
                        portions=portions,
                        carbs_per_portion=carbs_per_portion,
                        total_carbs=portions*carbs_per_portion
                    ))
            meal_record.reading = carb_intake

            meal_crud.meal_insert(meal_record)


def create_recommendation_table():
    """ Create the Recommendation table """

    table_name = "[dbo].[Recommendation]"
    field_list = [
        "[RecommendationId] [int] IDENTITY(1,1) NOT NULL",
        "[RecommendationType] [nvarchar](20) NOT NULL",
        "[LowerBound] [int] NOT NULL",
        "[UpperBound] [int] NOT NULL",
        "[Recommendation] [nvarchar](255) NOT NULL",
        "[UseCount] [int] NOT NULL",
        "PRIMARY KEY CLUSTERED([RecommendationId] ASC)"
    ]
    create_sql_statement = "CREATE TABLE " + table_name + "("
    create_sql_statement += ", ".join(field_list)
    create_sql_statement += ");"

    drop_sql_statement = "DROP TABLE " + table_name + ";"

    create_table(create_sql_statement, drop_sql_statement)


def create_table(create_sql_statement, drop_sql_statement):
    """ Runs the create and if necessary the drop table SQL """
    with db.Db() as cursor:
        try:
            cursor.execute(create_sql_statement)
        except pyodbc.Error as ex:
            cursor.execute(drop_sql_statement)
            cursor.execute(create_sql_statement)
            print(ex.args)




setup()