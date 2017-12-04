USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_CREATE_DATA_MEAL') IS NOT NULL
    DROP PROC dbo.USR_USP_CREATE_DATA_MEAL;
GO
CREATE PROC dbo.USR_USP_CREATE_DATA_MEAL
(
    @MEAL NVARCHAR(MAX),
    @RECORD_DATE_START DATE,
    @RECORD_DATE_END DATE
)
AS
BEGIN

    DECLARE @READING_BEFORE INT,
            @READING_AFTER INT,
            @CARB INT,
            @DIFF_READING INT,
            @DATE DATE,
            @DATETIME DATETIME;

    WHILE (@RECORD_DATE_START <= @RECORD_DATE_END)
    BEGIN

        SET @DATE = @RECORD_DATE_START;
        SET @DATETIME = @RECORD_DATE_START;


        SELECT @READING_BEFORE = b.Reading
        FROM dbo.BG AS b
        WHERE b.Meal = @MEAL
              AND b.Mark = 'BEFORE'
              AND b.RecordDate = @DATE;

        SELECT @READING_AFTER = b.Reading
        FROM dbo.BG AS b
        WHERE b.Meal = @MEAL
              AND b.Mark = 'AFTER'
              AND b.RecordDate = @DATE;


        -- FOR THE MEAL table
        -- start

        SELECT @DIFF_READING = @READING_AFTER - @READING_BEFORE;
        -- FOR MEALS
        SELECT @CARB = CASE
                           WHEN @DIFF_READING
                                BETWEEN 0 AND 10 THEN
                               CAST(1 + (5 - 1) * RAND() AS INT)
                           WHEN @DIFF_READING
                                BETWEEN 10 AND 20 THEN
                               CAST(5 + (10 - 5) * RAND() AS INT)
                           WHEN @DIFF_READING
                                BETWEEN 20 AND 30 THEN
                               CAST(10 + (15 - 10) * RAND() AS INT)
                           WHEN @DIFF_READING
                                BETWEEN 30 AND 40 THEN
                               CAST(15 + (20 - 15) * RAND() AS INT)
                           WHEN @DIFF_READING
                                BETWEEN 40 AND 50 THEN
                               CAST(20 + (25 - 20) * RAND() AS INT)
                       END; -- end case


        INSERT INTO dbo.M
        (
            Meal,
            TotalCarbs,
            RecordDate,
            RecordDateTime,
            Notes
        )
        VALUES
        (   @MEAL,     -- Meal - nvarchar(20)
            @CARB,     -- TotalCarbs - int
            @DATE,     -- RecordDate - date
            @DATETIME, -- RecordDateTime - datetime
            N''        -- Notes - nvarchar(255)
            );

        SELECT @RECORD_DATE_START = DATEADD(d, 1, @RECORD_DATE_START);

    END; -- end of inner while lopp


END; -- END OF SP