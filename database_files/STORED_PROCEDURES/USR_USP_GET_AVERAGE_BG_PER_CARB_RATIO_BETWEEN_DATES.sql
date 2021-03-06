USE [DiabeticLogger];
GO

/****** Object:  StoredProcedure [dbo].[USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES]    Script Date: 12/7/2017 10:56:15 AM ******/
IF OBJECT_ID('[DiabeticLogger].[dbo].[USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES]') IS NOT NULL
    DROP PROCEDURE [dbo].[USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES];

GO


/****** Object:  StoredProcedure [dbo].[USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES]    Script Date: 12/7/2017 10:56:15 AM ******/
SET ANSI_NULLS ON;
GO

SET QUOTED_IDENTIFIER ON;
GO

CREATE PROC [dbo].[USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES] (@DAYS NVARCHAR(20))
AS
BEGIN
    SET NOCOUNT ON;
    --cast and prevent parameter sniffing
    DECLARE @DAYS_local INT = CAST(@DAYS AS INT);

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

    IF OBJECT_ID('tempdb.dbo.#BG_DIFF') IS NOT NULL
        DROP TABLE #BG_DIFF;

    SELECT af.RecordDate,
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
          AND af.RecordDate > GETDATE() - @DAYS_local;

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



    SELECT RECOMMENDATION = CAST(CONCAT(
                                           'During the past ',
                                           @DAYS,
                                           ' days, during ',
                                           bd.Meal,
                                           ' your average blood glucose level has been ',
                                           AVG(bd.DIFF),
                                           ' and your average carb intake ',
                                           AVG(md.TotalCarbs),
                                           '. This means that your sugar goes up by ',
                                           ROUND(AVG(CAST(bd.DIFF AS FLOAT) / CAST(md.TotalCarbs AS FLOAT)), 2),
                                           ' per carb eaten.'
                                       ) AS NVARCHAR(MAX))
    FROM #BG_DIFF AS bd
        INNER JOIN #M_DIFF AS md
            ON md.RecordDate = bd.RecordDate
               AND md.Meal = bd.Meal
    GROUP BY bd.Meal;

END;
GO
EXEC dbo.USR_USP_GET_AVERAGE_BG_PER_CARB_RATIO_BETWEEN_DATES @DAYS = N'15' -- nvarchar(20)



