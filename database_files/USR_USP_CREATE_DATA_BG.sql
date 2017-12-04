USE DiabeticLogger;
GO
IF OBJECT_ID('diabeticlogger.dbo.USR_USP_CREATE_DATA_BG') IS NOT NULL
    DROP PROC dbo.USR_USP_CREATE_DATA_BG;
GO
CREATE PROC dbo.USR_USP_CREATE_DATA_BG
(
    @MEAL NVARCHAR(MAX),
    @MARK NVARCHAR(MAX),
    @RECORD_DATE_START DATE,
    @RECORD_DATE_END DATE,
    @BG_READING_RANGE_START INT,
    @BG_READING_RANGE_END INT
)
AS
BEGIN

    DECLARE @READING INT,
            @CURRENT_READING INT,
            @CARB INT,
            @DIFF_READING INT,
            @DATE DATE,
            @DATETIME DATETIME;

    WHILE (@RECORD_DATE_START <= @RECORD_DATE_END)
    BEGIN

        SET @DATE = @RECORD_DATE_START;
        SET @DATETIME = @RECORD_DATE_START;



        IF @MARK = 'BEFORE'
        BEGIN
            SET @READING
                = CAST(@BG_READING_RANGE_START + (@BG_READING_RANGE_END - @BG_READING_RANGE_START) * RAND() AS INT);
        END;

        IF @MARK = 'AFTER'
        BEGIN

            SELECT @CURRENT_READING = b.Reading
            FROM dbo.BG AS b
            WHERE b.Meal = @MEAL
                  AND b.Mark = 'BEFORE'
                  AND b.RecordDate = @DATE;

            SELECT @READING = @CURRENT_READING + CAST(10 + (50 - 10) * RAND() AS INT);
        END;
        -- THE FIRST INSERT WILL ALWAYS BE MARKED 'BEFORE'
        INSERT INTO dbo.BG
        (
            Mark,
            Meal,
            Reading,
            RecordDate,
            RecordDateTime,
            Notes
        )
        VALUES
        (   @MARK,     -- Mark - nvarchar(20)
            @MEAL,     -- Meal - nvarchar(20)
            @READING,  -- Reading - int
            @DATE,     -- RecordDate - datetime
            @DATETIME, -- RecordDateTime - datetime
            N''        -- Notes - nvarchar(255)
            );





        SELECT @RECORD_DATE_START = DATEADD(d, 1, @RECORD_DATE_START);

    END; -- end of inner while lopp


END; -- END OF SP