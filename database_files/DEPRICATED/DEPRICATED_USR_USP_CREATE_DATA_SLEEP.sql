--SET QUOTED_IDENTIFIER ON|OFF
--SET ANSI_NULLS ON|OFF
USE DiabeticLogger;
GO
IF OBJECT_ID('DiabeticLogger.dbo.USR_USP_CREATE_DATA_SLEEP') IS NOT NULL
    DROP TABLE dbo.USR_USP_CREATE_DATA_SLEEP;
GO
CREATE PROCEDURE dbo.USR_USP_CREATE_DATA_SLEEP
AS
BEGIN

    INSERT INTO dbo.S
    (
        Reading,
        RecordDate,
        RecordDateTime,
        Notes
    )
    SELECT Reading = CASE
                         WHEN tody.Reading - yesterday.Reading = 0 THEN
                             6.0
                         WHEN tody.Reading - yesterday.Reading < 0 THEN
                             8.0
                         WHEN tody.Reading - yesterday.Reading > 0 THEN
                             4.0
                     END,
           tody.RecordDate,
           tody.RecordDateTime,
           ''
    FROM dbo.BG AS yesterday
        INNER JOIN dbo.BG AS tody
            ON tody.RecordDate = DATEADD(d, -1, yesterday.RecordDate)
    WHERE tody.Meal = 'Breakfast'
          AND tody.Mark = 'Before'
          AND yesterday.Meal = 'DINNER'
          AND yesterday.Mark = 'AFTER'
          AND NOT EXISTS
    (
        SELECT 1 FROM dbo.S AS s2 WHERE s2.RecordDate = tody.RecordDate
    );
END;



GO
