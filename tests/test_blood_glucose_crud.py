import sys
sys.path.insert(0, "../database_files")
import datetime
from database_files import blood_glucose_crud


# ==============================================================================
# Tests to determine if a Blood Glucose record can be inserted and then
# retrieved by id
# Acceptance Criteria for DIAB-125
#       A record is inserted into the database with specific values
# Author: Tim Camp
# Date Created: 11/24/2017
# ==============================================================================
def test_insert():

    # Specific values
    meal = "Before Breakfast"
    reading = 250

    # The code below converts datetime stamps to Microsoft SQL Server specific values
    # and then convert it back for comparison to the retrieved value from Microsoft SQL Server
    record_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_date = datetime.strptime(record_date, "%Y-%m-%d %H:%M:%S")

    notes = "test_insert unit test record at " + str(record_date)

    # Insert the record
    inserted_id = blood_glucose_crud.blood_glucose_insert(
        blood_glucose_crud.BloodGlucoseRecord(
            meal=meal,
            reading=reading,
            record_date=record_date,
            notes=notes
        )
    )

    # Retrieve the record
    retrieved_record = blood_glucose_crud.blood_glucose_select_by_id(inserted_id)

    # Perform tests
    assert retrieved_record.blood_glucose_id == inserted_id
    assert retrieved_record.meal == meal
    assert retrieved_record.reading == reading
    assert retrieved_record.record_date == record_date
    assert retrieved_record.notes == notes


# =============================================================================
# Tests to determine if a Blood Glucose records be retrieved for the past
# number of days
# Acceptance Criteria for DIAB-130
#       Retrieve records for a number of days in the past
# =============================================================================
def test_select_by_days():

    # Specific values
    days = 3

    # Retrieve the records
    record_list = blood_glucose_crud.blood_glucose_select_by_days(days=days)

    # This is done to correctly format the date time for use with Microsoft SQL Server
    oldest_date = datetime.today() - timedelta(days=days)
    oldest_date = oldest_date.strftime("%Y-%m-%d 00:00:00")
    oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d %H:%M:%S")

    # Test that all the records returned have a record date that is greater
    # than the oldest date that should be in the record set
    for record in record_list:
        assert record.record_date >= oldest_date


# =============================================================================
# Tests to determine if a Blood Glucose records be retrieved from the date
# parameter back in time for the number of days parameter
# TODO: Correct the acceptance criteria issue tag
# Acceptance Criteria for DIAB-130
#       Retrieve records for a number of days in the past
# =============================================================================
def test_select_by_date():

    # Specific values
    start_date = datetime.strptime('2017-11-25 23:59:59', '%Y-%m-%d %H:%M:%S')
    include_days = 3

    # Retrieve the records
    record_list = blood_glucose_crud.select_by_date(start_date=start_date, include_days=include_days)

    # This is done to correctly format the date time for use with Microsoft SQL Server
    oldest_date = start_date - timedelta(days=include_days)
    oldest_date = oldest_date.strftime("%Y-%m-%d 00:00:00")
    oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d %H:%M:%S")
    record_count = 0

    # Test that all the records returned have a record date that is greater
    # than or equal to the oldest date and less than or equal to the starting date
    for record in record_list:
        assert record.record_date >= oldest_date
        assert record.record_date <= start_date
        record_count += 1

    # This is a known number of records that are in the database
    # This number will change if we move to another database
    assert record_count == 38


# =============================================================================
# Tests to determine if a Blood Glucose record is deleted
# Acceptance Criteria for (Not in Sprint, included for completeness and testing)
# =============================================================================
def test_delete():

    # Specific values
    meal = "After Dinner"
    reading = 115

    # The code below converts datetime stamps to Microsoft SQL Server specific values
    # and then convert it back for comparison to the retrieved value from Microsoft SQL Server
    record_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    record_date = datetime.strptime(record_date, "%Y-%m-%d %H:%M:%S")

    notes = "test_delete unit test record at " + str(record_date)

    # Insert the record
    inserted_id = blood_glucose_crud.blood_glucose_insert(
        blood_glucose_crud.BloodGlucoseRecord(
            meal=meal,
            reading=reading,
            record_date=record_date,
            notes=notes
        )
    )

    # Test that a record was inserted and a non-zero ID was returned
    assert inserted_id != 0

    # Retrieve the record and test that it was the same as the one inserted
    retrieved_record = blood_glucose_crud.blood_glucose_select_by_id(inserted_id)
    assert retrieved_record.blood_glucose_id == inserted_id

    # Test that 1 record and only 1 is deleted
    deleted_rows = blood_glucose_crud.blood_glucose_delete(inserted_id)
    assert deleted_rows == 1

    # Test that no record is deleted when we have already deleted it
    deleted_rows = blood_glucose_crud.blood_glucose_delete(inserted_id)
    assert deleted_rows == 0
