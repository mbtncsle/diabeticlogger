USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_GET_BG_AVERAGE') IS NOT NULL
    DROP PROC dbo.USR_USP_GET_BG_AVERAGE;
GO
CREATE PROC dbo.USR_USP_GET_BG_AVERAGE
(
    @READING INT,
    @MEAL NVARCHAR(MAX)
)
AS
BEGIN

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
    FROM dbo.BG AS b
    WHERE b.RecordDate
    BETWEEN @START_DATE AND @END_DATE
	AND b.Meal = @MEAL
	AND b.Mark = @MARK
	


    DECLARE @MESSAGE NVARCHAR(MAX) = '';

	IF @MONTHLY_AVERAGE < @READING
	SELECT CONCAT('Your monthly average is ' , @MONTHLY_AVERAGE , ' and your current reading is ' , @READING)

  
END;
GO
EXEC dbo.USR_USP_GET_BG_AVERAGE @READING = 120, @MEAL = 'BEFORE BREAKFAST'