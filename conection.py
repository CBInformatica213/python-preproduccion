import pyodbc

cnxn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server}; Server=tcp:casablanca.database.windows.net,1433;Database=DB_CB;Uid={adm4@psatcb.onmicrosoft.com}; Pwd={Brss213.--};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryPassword')
cursor = cnxn.cursor()
cursor.execute("SELECT * FROM Personas")
rows = cursor.fetchall()
for row in rows:
    print(row)
print("cnxn")