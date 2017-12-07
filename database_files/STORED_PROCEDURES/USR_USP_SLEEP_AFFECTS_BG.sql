USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_SLEEP_AFFECTS_BG') IS NOT NULL
    DROP PROC dbo.USR_USP_SLEEP_AFFECTS_BG;
GO
CREATE PROC dbo.USR_USP_SLEEP_AFFECTS_BG
AS
BEGIN
    SET NOCOUNT ON;
    --cast and prevent parameter sniffing


    IF OBJECT_ID('tempdb.dbo.#SLEEP') IS NOT NULL
        DROP TABLE #SLEEP;

    SELECT s.Reading,
           BG_CHANGE = AVG(td.Reading - yd.Reading)
    INTO #SLEEP
    FROM dbo.BG AS td
        INNER JOIN dbo.BG AS yd
            ON td.RecordDate = DATEADD(d, -1, yd.RecordDate)
        INNER JOIN dbo.S AS s
            ON s.RecordDate
               BETWEEN td.RecordDate AND DATEADD(d, -1, yd.RecordDate)
    WHERE td.Meal = 'BREAKFAST'
          AND td.Mark = 'BEFORE'
          AND yd.Meal = 'DINNER'
          AND yd.Mark = 'AFTER'
    GROUP BY s.Reading
	ORDER BY s.Reading DESC;


    SELECT MESSAGE = CONCAT(
                               'On average, when you get ',
                               s.Reading,
                               ' hours of sleep, your blood glucose level changes by ',
                               s.BG_CHANGE
                           )
    FROM #SLEEP AS s 
	UNION 
	SELECT MESSAGE = 'There more you rest, the more your blood glucose reduces!'



END;
GO
EXEC dbo.USR_USP_SLEEP_AFFECTS_BG; -- date
