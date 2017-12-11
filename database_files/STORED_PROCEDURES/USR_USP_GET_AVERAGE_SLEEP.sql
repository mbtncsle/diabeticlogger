USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_GET_AVERAGE_SLEEP') IS NOT NULL
    DROP PROC dbo.USR_USP_GET_AVERAGE_SLEEP;
GO
CREATE PROC dbo.USR_USP_GET_AVERAGE_SLEEP (@DAYS NVARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON;
    --cast and prevent parameter sniffing
	DECLARE @DAYS_local INT = CAST(@DAYS AS INT)

	    IF OBJECT_ID('tempdb.dbo.#BG') IS NOT NULL
        DROP TABLE #BG;

    SELECT bg.BloodGlucoseId,
           Meal = CAST(REPLACE(REPLACE(bg.Meal, 'BEFORE ', ''), 'AFTER ', '') AS NVARCHAR(50)),
           Mark = CAST(REPLACE(REPLACE(REPLACE(bg.Meal, ' DINNER', ''), ' BREAKFAST', ''), ' LUNCH', '') AS NVARCHAR(50)),
           bg.Reading,
           RecordDate = CAST(bg.RecordDate AS DATE),
           RecordDateTime = CAST(bg.RecordDate AS DATETIME),
           bg.Notes
    INTO #BG
    FROM dbo.BloodGlucose AS bg;

    CREATE NONCLUSTERED INDEX [idx_p]
    ON #BG
    (
        Meal,
        Mark,
        RecordDate
    )
    INCLUDE (BloodGlucoseId);

    IF OBJECT_ID('tempdb.dbo.#M') IS NOT NULL
        DROP TABLE #M;

    SELECT m.MealId,
           Meal = CAST(REPLACE(REPLACE(m.Meal, 'BEFORE ', ''), 'AFTER ', '') AS NVARCHAR(50)),
           Mark = CAST(REPLACE(REPLACE(REPLACE(m.Meal, ' DINNER', ''), ' BREAKFAST', ''), ' LUNCH', '') AS NVARCHAR(50)),
           TotalCarbs = m.Reading,
           RecordDate = CAST(m.RecordDate AS DATE),
           RecordDateTime = CAST(m.RecordDate AS DATETIME),
           m.Notes
    INTO #M
    FROM dbo.Meal AS m;


    CREATE NONCLUSTERED INDEX [idx_p]
    ON #M
    (
        Meal,
        Mark,
        RecordDate
    )
    INCLUDE (MealId);

    IF OBJECT_ID('tempdb.dbo.#S') IS NOT NULL
        DROP TABLE #S;
    CREATE TABLE #S
    (
        [SleepId] [INT],
        [Reading] [FLOAT] NOT NULL,
        [RecordDate] [DATE] NOT NULL,
        [RecordDateTime] [DATETIME] NOT NULL,
        [Notes] [NVARCHAR](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
    ) ON [PRIMARY];

    INSERT INTO #S
    (
        SleepId,
        Reading,
        RecordDate,
        RecordDateTime,
        Notes
    )
    SELECT s.SleepId,
           s.Reading,
           RecordDate = CAST(s.RecordDate AS DATE),
           RecordDateTime = CAST(s.RecordDate AS DATETIME),
           s.Notes
    FROM dbo.Sleep AS s;


    IF OBJECT_ID('tempdb.dbo.#SLEEP') IS NOT NULL
        DROP TABLE #SLEEP;

    SELECT AVG_SLEEP = AVG(s.Reading)
    INTO #SLEEP
    FROM #S AS s
    WHERE s.RecordDate > GETDATE() - @DAYS_local;


    SELECT MESSAGE = CONCAT(
                               'On average, during the past ' , @DAYS , ' days you have sleep for ' , AVG_SLEEP, ' hours.')
                             
                           
    FROM #SLEEP AS s;



END;
GO
EXEC dbo.USR_USP_GET_AVERAGE_SLEEP @DAYS = 30; -- date
