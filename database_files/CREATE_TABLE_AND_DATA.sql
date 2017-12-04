USE DiabeticLogger;
GO
EXEC dbo.USR_USP_CREATE_BASE_TABLES;
GO

DECLARE @COUNTER_START INT = 1,
        @COUNTER_END INT = 3,
        @RECORD_DATE_START DATE = '2017-10-04',
        @RECORD_DATE_END DATE = '2017-12-04',
        @MEAL NVARCHAR(MAX),
        @BG_READING_RANGE_START INT = 90,
        @BG_READING_RANGE_END INT = 130;

WHILE (@COUNTER_START <= @COUNTER_END)
BEGIN
    IF @COUNTER_START = 1
    BEGIN
        SET @MEAL = 'BREAKFAST';

    END;
    ELSE IF (@COUNTER_START = 2)
    BEGIN
        SELECT @MEAL = 'LUNCH';
    END;
    ELSE IF (@COUNTER_START = 3)
    BEGIN
        SELECT @MEAL = 'DINNER';
    END;

    EXEC dbo.USR_USP_CREATE_DATA_BG @MEAL = @MEAL,                                     -- nvarchar(max)
                                    @MARK = N'BEFORE',                                 -- nvarchar(max)
                                    @RECORD_DATE_START = @RECORD_DATE_START,           -- date
                                    @RECORD_DATE_END = @RECORD_DATE_END,               -- date
                                    @BG_READING_RANGE_START = @BG_READING_RANGE_START, -- int
                                    @BG_READING_RANGE_END = @BG_READING_RANGE_END;     -- int

    EXEC dbo.USR_USP_CREATE_DATA_BG @MEAL = @MEAL,                                     -- nvarchar(max)
                                    @MARK = N'AFTER',                                  -- nvarchar(max)
                                    @RECORD_DATE_START = '2017-10-04',                 -- date
                                    @RECORD_DATE_END = '2017-12-04',                   -- date
                                    @BG_READING_RANGE_START = @BG_READING_RANGE_START, -- int
                                    @BG_READING_RANGE_END = @BG_READING_RANGE_END;     -- int

    EXEC dbo.USR_USP_CREATE_DATA_MEAL @MEAL = @MEAL,                           -- nvarchar(max)
                                      @RECORD_DATE_START = @RECORD_DATE_START, -- date
                                      @RECORD_DATE_END = @RECORD_DATE_END;

    SELECT @COUNTER_START = @COUNTER_START + 1;
END;

GO

EXEC dbo.USR_USP_CREATE_DATA_SLEEP;

GO

SELECT *
FROM dbo.BG AS b
ORDER BY b.RecordDate ASC,
         b.Meal ASC,
         b.Mark DESC;
SELECT *
FROM dbo.M AS m2;
SELECT *
FROM dbo.S AS s2;