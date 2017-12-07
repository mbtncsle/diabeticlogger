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

    IF OBJECT_ID('tempdb.dbo.#SLEEP') IS NOT NULL
        DROP TABLE #SLEEP;

    SELECT AVG_SLEEP = AVG(s.Reading)
    INTO #SLEEP
    FROM dbo.S AS s
    WHERE s.RecordDate > GETDATE() - @DAYS_local;


    SELECT MESSAGE = CONCAT(
                               'On average, during the past ' , @DAYS , ' days you have sleep for ' , AVG_SLEEP, ' hours.')
                             
                           
    FROM #SLEEP AS s;



END;
GO
EXEC dbo.USR_USP_GET_AVERAGE_SLEEP @DAYS = 30; -- date
