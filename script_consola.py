import pyodbc
from urllib.parse import quote

password = 'Brss213.--'
encoded_password = quote(password)
# Conexión a SQL Server
cnxn = pyodbc.connect(
    f'Driver={{ODBC Driver 18 for SQL Server}};'
    f'Server=tcp:casablanca.database.windows.net,1433;'
    f'Database=DB_CB;'
    f'Uid=adm4@psatcb.onmicrosoft.com;'
    f'Pwd={encoded_password};'
    f'Encrypt=yes;'
    f'TrustServerCertificate=no;'
    f'Connection Timeout=30;'
    f'Authentication=ActiveDirectoryPassword'
)
cursor = cnxn.cursor()

def obtener_primer_registro_pj():
    cursor.execute("SELECT TOP 1 * FROM PJ")
    primer_registro_pj = cursor.fetchone()
    return primer_registro_pj

def obtener_personas_asociadas(cod_pj):
    cursor.execute("SELECT p.* FROM Personas p INNER JOIN Dir_Serie ds ON p.RUT = ds.Rut WHERE ds.Cod_PJ = ?", (cod_pj,))
    personas_asociadas = cursor.fetchall()
    return personas_asociadas

primer_registro_pj = obtener_primer_registro_pj()
if primer_registro_pj:
    print("Primer registro de PJ:")
    print(primer_registro_pj)

    cod_pj = primer_registro_pj.Cod_PJ
    personas_asociadas = obtener_personas_asociadas(cod_pj)
    if personas_asociadas:
        print("Personas asociadas:")
        for persona in personas_asociadas:
            print(persona)
    else:
        print("No hay personas asociadas a este registro de PJ.")
else:
    print("No hay registros en la tabla PJ.")
