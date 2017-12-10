driver = 'DRIVER={ODBC Driver 13 for SQL Server};'
server = 'SERVER=vampires.database.windows.net;'
port = 'PORT=1433;'
database = 'DATABASE=DiabeticLogger;'
username = 'UID=miguel;'
password = 'PWD=Hola123.;'

connection_string = driver + port + server + port + database + username + password

print(connection_string)