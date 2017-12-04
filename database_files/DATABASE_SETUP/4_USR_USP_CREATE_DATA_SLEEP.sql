--SET QUOTED_IDENTIFIER ON|OFF
--SET ANSI_NULLS ON|OFF
USE DiabeticLogger;
GO
IF OBJECT_ID('DiabeticLogger.dbo.USR_USP_CREATE_DATA_SLEEP') IS NOT NULL
    DROP PROC dbo.USR_USP_CREATE_DATA_SLEEP;
GO
CREATE PROCEDURE dbo.USR_USP_CREATE_DATA_SLEEP
AS
BEGIN

    INSERT INTO dbo.Sleep
    (
        Reading,
        RecordDate,
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
           ''
    FROM dbo.BloodGlucose AS yesterday
        INNER JOIN dbo.BloodGlucose AS tody
            ON tody.RecordDate = DATEADD(d, -1, yesterday.RecordDate)
    WHERE tody.Meal = CONCAT('BEFORE', ' ', 'BREAKFAST')
          AND yesterday.Meal = CONCAT('AFTER', ' ', 'DINNER')
          AND NOT EXISTS
    (
        SELECT 1
        FROM dbo.Sleep AS s2
        WHERE CAST(s2.RecordDate AS DATE) = CAST(tody.RecordDate AS DATE)
    );
END;



GO
