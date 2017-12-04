USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES') IS NOT NULL
    DROP PROC dbo.USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES;
GO
CREATE PROC dbo.USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES
(
    @START_DATE DATE,
    @END_DATE DATE
)
AS
BEGIN


    IF @START_DATE IS NULL
       OR @END_DATE IS NULL
    BEGIN
        SELECT @START_DATE = GETDATE() - 1;
        SELECT @END_DATE = GETDATE() + 1;
    END;



    IF OBJECT_ID('tempdb.dbo.#BG_DIFF') IS NOT NULL
        DROP TABLE #BG_DIFF;

    SELECT af.RecordDate,
           af.Meal,
           DIFF = af.Reading - bef.Reading
    INTO #BG_DIFF
    FROM dbo.BG AS bef
        INNER JOIN dbo.BG AS af
            ON af.RecordDate = bef.RecordDate
               AND af.Meal = bef.Meal
               AND af.Mark <> bef.Mark
    WHERE bef.Mark = 'BEFORE'
          AND af.Mark = 'AFTER'
          AND af.RecordDate
          BETWEEN @START_DATE AND DATEADD(d, 1, @END_DATE);

    IF OBJECT_ID('tempdb.dbo.#M_DIFF') IS NOT NULL
        DROP TABLE #M_DIFF;

    SELECT bd.RecordDate,
           bd.Meal,
           bd.DIFF,
           m.TotalCarbs,
           m.MealId
    INTO #M_DIFF
    FROM #BG_DIFF AS bd
        INNER JOIN dbo.M AS m
            ON m.RecordDate = bd.RecordDate
               AND m.Meal = bd.Meal;



    SELECT Month = DATEPART(M, bd.RecordDate),
           bd.Meal,
           BG_AVG = AVG(bd.DIFF),
           CARB_AVG = AVG(md.TotalCarbs),
           AVG_CARB_RATIO = ROUND(AVG(CAST(bd.DIFF AS FLOAT) / CAST(md.TotalCarbs AS FLOAT)), 2)
    FROM #BG_DIFF AS bd
        INNER JOIN #M_DIFF AS md
            ON md.RecordDate = bd.RecordDate
               AND md.Meal = bd.Meal
    GROUP BY bd.Meal,
             DATEPART(M, bd.RecordDate);

END;
GO
EXEC dbo.USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES @START_DATE = '2017-10-04', -- date
                                                             @END_DATE = '2017-12-04';   -- date
