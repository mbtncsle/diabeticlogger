USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_GET_MONTHLY_BG_AVERAGE') IS NOT NULL
    DROP PROC dbo.USR_USP_GET_MONTHLY_BG_AVERAGE;
GO
CREATE PROC dbo.USR_USP_GET_MONTHLY_BG_AVERAGE
(
    @READING INT,
    @MEAL NVARCHAR(MAX)
)
AS
BEGIN
	
	    IF OBJECT_ID('tempdb.dbo.#BG') IS NOT NULL
        DROP TABLE #BG;

    SELECT bg.BloodGlucoseId,
           Meal = REPLACE(REPLACE(bg.Meal, 'BEFORE ', ''), 'AFTER ', ''),
           Mark = REPLACE(REPLACE(REPLACE(bg.Meal, ' DINNER', ''), ' BREAKFAST', ''), ' LUNCH', ''),
           bg.Reading,
           RecordDate = CAST(bg.RecordDate AS DATE),
           RecordDateTime = CAST(bg.RecordDate AS DATETIME),
           bg.Notes
    INTO #BG
    FROM dbo.BloodGlucose AS bg;

	CREATE NONCLUSTERED INDEX [idx_p] ON #BG (Meal,Mark,RecordDate) INCLUDE(BloodGlucoseId)

    IF OBJECT_ID('tempdb.dbo.#M') IS NOT NULL
        DROP TABLE #M;

    SELECT m.MealId,
           Meal = REPLACE(REPLACE(m.Meal, 'BEFORE ', ''), 'AFTER ', ''),
           Mark = REPLACE(REPLACE(REPLACE(m.Meal, ' DINNER', ''), ' BREAKFAST', ''), ' LUNCH', ''),
           TotalCarbs = m.Reading,
           RecordDate = CAST(m.RecordDate AS DATE),
           RecordDateTime = CAST(m.RecordDate AS DATETIME),
           m.Notes
    INTO #M
    FROM dbo.Meal AS m;

	
	CREATE NONCLUSTERED INDEX [idx_p] ON #M (Meal,Mark,RecordDate) INCLUDE(MealId)

    DECLARE @START_DATE DATE,
            @END_DATE DATE,
            @MONTHLY_AVERAGE INT,
            @MARK NVARCHAR(MAX);

    SELECT @MARK = CASE
                       WHEN @MEAL LIKE 'BEFORE%' THEN
                           'BEFORE'
                       WHEN @MEAL LIKE 'AFTER%' THEN
                           'AFTER'
                   END;
    SELECT @MEAL = REPLACE(REPLACE(@MEAL, 'BEFORE ', ''), 'AFTER ', '');

    IF @START_DATE IS NULL
       OR @END_DATE IS NULL
    BEGIN
        SELECT @START_DATE = GETDATE() - 30;
        SELECT @END_DATE = GETDATE() + 1;
    END;


    SELECT @MONTHLY_AVERAGE = AVG(b.Reading)
    FROM #BG AS b
    WHERE b.RecordDate
          BETWEEN @START_DATE AND @END_DATE
          AND b.Meal = @MEAL
          AND b.Mark = @MARK;



    DECLARE @MESSAGE NVARCHAR(MAX)
        = 'In the past 30 days, your BG average <MARK> <MEAL> is <MONTHLY> and your current reading is <READING>';

    SELECT @MESSAGE = REPLACE(@MESSAGE, '<MONTHLY>', @MONTHLY_AVERAGE);
    SELECT @MESSAGE = REPLACE(@MESSAGE, '<READING>', @READING);
    SELECT @MESSAGE = REPLACE(@MESSAGE, '<MARK>', @MARK);
    SELECT @MESSAGE = REPLACE(@MESSAGE, '<MEAL>', @MEAL);

    DECLARE @RANGE_UPPER INT = 130,
            @RANGE_LOWER INT = 90;


    SELECT MESSAGE = @MESSAGE;

END;
GO
--TEST
EXEC dbo.USR_USP_GET_MONTHLY_BG_AVERAGE @READING = 120, @MEAL = 'AFTER BREAKFAST';