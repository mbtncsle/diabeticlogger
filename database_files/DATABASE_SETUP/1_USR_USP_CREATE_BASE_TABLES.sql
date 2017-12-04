IF OBJECT_ID('diabeticlogger.dbo.USR_USP_CREATE_BASE_TABLES') IS NOT NULL
    DROP PROC USR_USP_CREATE_BASE_TABLES;
GO
CREATE PROC USR_USP_CREATE_BASE_TABLES
AS
BEGIN
    
    IF OBJECT_ID('diabeticlogger.dbo.[BG]') IS NOT NULL
        DROP TABLE diabeticlogger.dbo.[BG];

    CREATE TABLE diabeticlogger.[dbo].[BG]
    (
        [BloodGlucoseId] [INT] NOT NULL IDENTITY(1, 1),
        [Mark] [NVARCHAR](20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
        [Meal] [NVARCHAR](20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
        [Reading] [INT] NOT NULL,
        [RecordDate] [DATE] NOT NULL,
        [RecordDateTime] [DATETIME] NOT NULL,
        [Notes] [NVARCHAR](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
    ) ON [PRIMARY];

    ALTER TABLE [dbo].[BG]
    ADD CONSTRAINT [PK__BG__D56DFCB397FC2C5C]
        PRIMARY KEY CLUSTERED ([BloodGlucoseId]) ON [PRIMARY];

   
    IF OBJECT_ID('diabeticlogger.dbo.[M]') IS NOT NULL
        DROP TABLE [M];

    CREATE TABLE [dbo].[M]
    (
        [MealId] [INT] NOT NULL IDENTITY(1, 1),
        [Meal] [NVARCHAR](20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
        [TotalCarbs] [INT] NOT NULL,
        [RecordDate] [DATE] NOT NULL,
        [RecordDateTime] [DATETIME] NOT NULL,
        [Notes] [NVARCHAR](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
    ) ON [PRIMARY];

    ALTER TABLE [dbo].[M]
    ADD CONSTRAINT [PK__M__D56DFCB397FC2C5C]
        PRIMARY KEY CLUSTERED ([MealId]) ON [PRIMARY];


    IF OBJECT_ID('diabeticlogger.dbo.[S]') IS NOT NULL
        DROP TABLE [S];
    CREATE TABLE [dbo].[S]
    (
        [SleepId] [INT] NOT NULL IDENTITY(1, 1),
        [Reading] [FLOAT] NOT NULL,
        [RecordDate] [DATE] NOT NULL,
        [RecordDateTime] [DATETIME] NOT NULL,
        [Notes] [NVARCHAR](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
    ) ON [PRIMARY];
    ALTER TABLE [dbo].[S]
    ADD CONSTRAINT [PK__S__54B08AE9918526E8]
        PRIMARY KEY CLUSTERED ([SleepId]) ON [PRIMARY];


    IF OBJECT_ID('diabeticlogger.dbo.[W]') IS NOT NULL
        DROP TABLE [W];
    CREATE TABLE [dbo].[W]
    (
        [StepsId] [INT] NOT NULL IDENTITY(1, 1),
        [Reading] [FLOAT] NOT NULL,
        [RecordDate] [DATE] NOT NULL,
        [RecordDateTime] [DATETIME] NOT NULL,
        [Notes] [NVARCHAR](255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL
    ) ON [PRIMARY];
    ALTER TABLE [dbo].[W]
    ADD CONSTRAINT [PK__W__54B08AE9918526E8]
        PRIMARY KEY CLUSTERED ([StepsId]) ON [PRIMARY];


END
;
GO
EXEC dbo.USR_USP_CREATE_BASE_TABLES

