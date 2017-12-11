USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_HOW_LAST_MEAL_AFFECTED_BG') IS NOT NULL
    DROP PROC dbo.USR_USP_HOW_LAST_MEAL_AFFECTED_BG;
GO
CREATE PROC dbo.USR_USP_HOW_LAST_MEAL_AFFECTED_BG
--(
--    @DAYS NVARCHAR(20)
--)
AS
BEGIN


    SET NOCOUNT ON;

    --DECLARE @DAYS_local INT = --CAST(@DAYS AS INT)
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

    DECLARE @BG_MESSAGE_INCREASE NVARCHAR(MAX)
        = 'Your last meal was <MEAL>, you consumed <CARB> carbs - increasing your BG level by <BG> mg/dl.';
    DECLARE @BG_MESSAGE_DECREASE NVARCHAR(MAX)
        = 'Your last meal was <MEAL>, you consumed <CARB> carbs - decreasing your BG level by <BG> mg/dl.';
    DECLARE @BG_MESSAGE_SAME NVARCHAR(MAX)
        = 'Your last meal was <MEAL>, you did not consumed any carbs. Your new BG level is <BG> mg/dl.';

    DECLARE @MEAL NVARCHAR(MAX),
            @CARB INT,
            @BG INT,
            @ID INT,
            @DATE DATE;

    IF OBJECT_ID('tempdb.dbo.#BG_DIFF') IS NOT NULL
        DROP TABLE #BG_DIFF;

    SELECT TOP 1
        af.RecordDate,
        af.Meal,
        DIFF = af.Reading - bef.Reading
    INTO #BG_DIFF
    FROM #BG AS bef
        INNER JOIN #BG AS af
            ON af.RecordDate = bef.RecordDate
               AND af.Meal = bef.Meal
               AND af.Mark <> bef.Mark
    WHERE bef.Mark = 'BEFORE'
          AND af.Mark = 'AFTER'
    -- AND af.RecordDate > GETDATE() - @DAYS_local 
    ORDER BY af.RecordDate DESC,
             bef.RecordDateTime DESC;

    IF OBJECT_ID('tempdb.dbo.#M_DIFF') IS NOT NULL
        DROP TABLE #M_DIFF;

    SELECT bd.RecordDate,
           bd.Meal,
           bd.DIFF,
           m.TotalCarbs,
           m.MealId
    INTO #M_DIFF
    FROM #BG_DIFF AS bd
        INNER JOIN #M AS m
            ON m.RecordDate = bd.RecordDate
               AND m.Meal = bd.Meal;

    IF OBJECT_ID('tempdb.dbo.#RESULT_SET') IS NOT NULL
        DROP TABLE #RESULT_SET;

    CREATE TABLE #RESULT_SET
    (
        DATE DATE,
        MESSAGE NVARCHAR(MAX)
    );

    WHILE EXISTS (SELECT * FROM #M_DIFF)
    BEGIN

        SELECT TOP 1
            @ID = md.MealId,
            @MEAL = md.Meal,
            @CARB = md.TotalCarbs,
            @BG = md.DIFF,
            @DATE = md.RecordDate
        FROM #M_DIFF AS md;

        PRINT (@BG);


        IF @BG > 0
        BEGIN
            SELECT @BG_MESSAGE_INCREASE = REPLACE(@BG_MESSAGE_INCREASE, '<MEAL>', @MEAL);
            SELECT @BG_MESSAGE_INCREASE = REPLACE(@BG_MESSAGE_INCREASE, '<CARB>', @CARB);
            SELECT @BG_MESSAGE_INCREASE = REPLACE(@BG_MESSAGE_INCREASE, '<BG>', @BG);

            INSERT INTO #RESULT_SET
            (
                DATE,
                MESSAGE
            )
            SELECT @DATE,
                   @BG_MESSAGE_INCREASE;
        END;
        IF @BG < 0
        BEGIN
            SELECT @BG_MESSAGE_DECREASE = REPLACE(@BG_MESSAGE_DECREASE, '<MEAL>', @MEAL);
            SELECT @BG_MESSAGE_DECREASE = REPLACE(@BG_MESSAGE_DECREASE, '<CARB>', @CARB);
            SELECT @BG_MESSAGE_DECREASE = REPLACE(@BG_MESSAGE_DECREASE, '<BG>', @BG);

            INSERT INTO #RESULT_SET
            (
                DATE,
                MESSAGE
            )
            SELECT @DATE,
                   @BG_MESSAGE_DECREASE;
        END;

        DELETE FROM #M_DIFF
        WHERE MealId = @ID;


        SELECT @BG_MESSAGE_INCREASE = 'For <MEAL>, you consumed <CARB> carbs - increasing your BG level by <BG> mg/dl.';
        SELECT @BG_MESSAGE_DECREASE = 'For <MEAL>, you consumed <CARB> carbs - decreasing your BG level by <BG> mg/dl.';
        SELECT @BG_MESSAGE_SAME = 'For <MEAL>, you did not consumed any carbs. Your new BG level is <BG> mg/dl.';

    END;


    SELECT MESSAGE
    FROM #RESULT_SET;


END;
GO
EXEC dbo.USR_USP_HOW_LAST_MEAL_AFFECTED_BG; --@DAYS = '30'   -- date
