USE DiabeticLogger;

GO

EXEC dbo.USR_USP_CREATE_BASE_TABLES;
GO

IF OBJECT_ID('diabeticlogger.dbo.USR_USP_CREATE_DATA_FOR_RECOMMENDATION') IS NOT NULL
    DROP PROC dbo.USR_USP_CREATE_DATA_FOR_RECOMMENDATION;
GO
CREATE PROC dbo.USR_USP_CREATE_DATA_FOR_RECOMMENDATION
AS
BEGIN
    TRUNCATE TABLE dbo.BG;
    TRUNCATE TABLE dbo.M;
    TRUNCATE TABLE dbo.S;


    INSERT INTO dbo.BG
    (
        Mark,
        Meal,
        Reading,
        RecordDate,
        RecordDateTime,
        Notes
    )
    SELECT Mark = CASE
                      WHEN Meal LIKE 'BEFORE%' THEN
                          'BEFORE'
                      WHEN Meal LIKE 'AFTER%' THEN
                          'AFTER'
                  END,
           Meal = REPLACE(REPLACE(Meal, 'BEFORE ', ''), 'AFTER ', ''),
           Reading,
           RecordDate = CAST(RecordDate AS DATE),
           RecordDate,
           N''
    FROM dbo.BloodGlucose;


    INSERT INTO dbo.M
    (
        Meal,
        TotalCarbs,
        RecordDate,
        RecordDateTime,
        Notes
    )
    SELECT Meal = REPLACE(REPLACE(Meal, 'BEFORE ', ''), 'AFTER ', ''),
           Reading,
           RecordDate = CAST(RecordDate AS DATE),
           RecordDate,
           N''
    FROM dbo.Meal;


    --INSERT INTO SLEEP
    INSERT INTO dbo.S
    (
        Reading,
        RecordDate,
        RecordDateTime,
        Notes
    )
    SELECT Reading,
           RecordDate = CAST(RecordDate AS DATE),
           RecordDate,
           N''
    FROM dbo.Sleep;

END;
GO
EXEC dbo.USR_USP_CREATE_DATA_FOR_RECOMMENDATION