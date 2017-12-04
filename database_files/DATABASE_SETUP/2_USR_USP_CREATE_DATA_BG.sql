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
            @DATETIME DATETIME,
			@CONCAT NVARCHAR(MAX);

			SELECT @CONCAT = CONCAT(@MARK, ' ', @MEAL)
			

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
			FROM dbo.BloodGlucose AS b
			WHERE b.Meal = CONCAT('BEFORE', ' ', @MEAL)
			AND CAST(b.RecordDate AS DATE) = @DATE;

            SELECT @READING = @CURRENT_READING + CAST(10 + (50 - 10) * RAND() AS INT);
        
		END;
        -- THE FIRST INSERT WILL ALWAYS BE MARKED 'BEFORE'
        INSERT INTO dbo.BloodGlucose
        (
            Meal,
            Reading,
            RecordDate,
            Notes
        )
        VALUES
        (   @CONCAT,       -- Meal - nvarchar(20)
            @READING,         -- Reading - int
            @DATETIME, -- RecordDate - datetime
            N''        -- Notes - nvarchar(255)
            )
       

        SELECT @RECORD_DATE_START = DATEADD(d, 1, @RECORD_DATE_START);

    END; -- end of inner while lopp


END; -- END OF SP

