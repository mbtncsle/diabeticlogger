-- ======================================================================================
-- Create SQL Login template for Azure SQL Database and Azure SQL Data Warehouse Database
-- ======================================================================================

CREATE LOGIN heroku WITH PASSWORD = 'Vampires6!'
GO

Use DiabeticLogger;
GO

IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'heroku')
BEGIN
    CREATE USER [heroku] FOR LOGIN [heroku]
    EXEC sp_addrolemember N'db_owner', N'heroku'
END;
GO