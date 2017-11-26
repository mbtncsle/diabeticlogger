import recommendation_crud


# =============================================================================
# Tests to determine if a Recommendation record can be inserted and then
# retrieved by id
# Acceptance Criteria for DIAB-125
#       A record is inserted into the database with specific values
# Author: Tim Camp
# Date Created: 11/25/2017
# =============================================================================
def test_insert():

    # Specific values
    recommendation_type = "blood_glucose"
    lower_bound = 90
    upper_bound = 120
    recommendation = "Recommendation for test_insert"
    use_count = 100

    # Insert the record
    inserted_id = recommendation_crud.recommendation_insert(
        recommendation_crud.RecommendationRecord(
            recommendation_type=recommendation_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            recommendation=recommendation,
            use_count=use_count
        )
    )

    # Retrieve the record
    retrieved_record = recommendation_crud.recommendation_select_by_id(inserted_id)

    # Perform tests
    assert retrieved_record.recommendation_id == inserted_id
    assert retrieved_record.recommendation_type == recommendation_type
    assert retrieved_record.lower_bound == lower_bound
    assert retrieved_record.upper_bound == upper_bound
    assert retrieved_record.recommendation == recommendation
    assert retrieved_record.use_count == use_count

    # Need to clean up after insert
    recommendation_crud.recommendation_delete(inserted_id)


# =============================================================================
# Tests to determine if recommendation records can be retrieved for the past
# number of days
# Acceptance Criteria for
# =============================================================================
def test_select_by_bounds():

    # Specific values
    recommendation_type = "blood_glucose"
    lower_bound = 90
    upper_bound = 120
    recommendation = "Recommendation for test_select_by_bounds"
    use_count = 100

    # Insert the record
    inserted_id = recommendation_crud.recommendation_insert(
        recommendation_crud.RecommendationRecord(
            recommendation_type=recommendation_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            recommendation=recommendation,
            use_count=use_count
        )
    )

    reading = 90

    # Retrieve the record
    record = recommendation_crud.recommendation_select_by_bounds(reading, recommendation_type)
    assert record.lower_bound <= reading
    assert record.upper_bound >= reading

    reading = 120

    # Retrieve the record
    record = recommendation_crud.recommendation_select_by_bounds(reading, recommendation_type)
    assert record.lower_bound <= reading
    assert record.upper_bound >= reading

    reading = 100

    # Retrieve the record
    record = recommendation_crud.recommendation_select_by_bounds(reading, recommendation_type)
    assert record.lower_bound <= reading
    assert record.upper_bound >= reading

    reading = 89

    # Retrieve the record
    record = recommendation_crud.recommendation_select_by_bounds(reading, recommendation_type)
    assert record is None

    reading = 121

    # Retrieve the record
    record = recommendation_crud.recommendation_select_by_bounds(reading, recommendation_type)
    assert record is None

    recommendation_crud.recommendation_delete(inserted_id)


# =============================================================================
# Tests to determine if a recommendation record is deleted
# Acceptance Criteria for
# =============================================================================
def test_delete():

    # Specific values
    recommendation_type = "meal"
    lower_bound = 200
    upper_bound = 300
    recommendation = "Recommendation for test_delete"
    use_count = 1

    # Insert the record
    inserted_id = recommendation_crud.recommendation_insert(
        recommendation_crud.RecommendationRecord(
            recommendation_type=recommendation_type,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            recommendation=recommendation,
            use_count=use_count
        )
    )

    # Test that a record was inserted and a non-zero ID was returned
    assert inserted_id != 0

    # Retrieve the record and test that it was the same as the one inserted
    retrieved_record = recommendation_crud.recommendation_select_by_id(inserted_id)
    assert retrieved_record.recommendation_id == inserted_id

    # Test that 1 record and only 1 is deleted
    deleted_rows = recommendation_crud.recommendation_delete(inserted_id)
    assert deleted_rows == 1

    # Test that no record is deleted when we have already deleted it
    deleted_rows = recommendation_crud.recommendation_delete(inserted_id)
    assert deleted_rows == 0

