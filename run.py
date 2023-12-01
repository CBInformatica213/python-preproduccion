from flask import Flask, render_template, flash, request, redirect, session, url_for, make_response, jsonify, json, send_from_directory
import pyodbc
from urllib.parse import quote
from functools import wraps
from unidecode import unidecode

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'Brss213.--'
app.config['SESSION_PERMANENT'] = False

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

#cache = Cache(app, config={'CACHE_TYPE': 'simple'})

password = 'Brss213.--'
encoded_password = quote(password)
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

#@app.route('/set_session')
#def set_session():
#    session['username'] = 'PePe'
#    return 'Session data set.'


@app.route('/get_session')
def get_session():
    username = session.get('username', 'Guest')
    return f'Hola, {username}!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('index.html')

@app.after_request
def after_request(response):
    return response

def proteger_ruta(func):
    @wraps(func)
    def decorador(*args, **kwargs):
        current_route = request.endpoint
        if current_route == 'index' and ('user' in session and session['user']):
            return func(*args, **kwargs)
        if 'user' not in session or not session['user']:
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decorador

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Rut = request.form['Rut']
        clave = request.form['clave']
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE Rut = ? AND clave = ? UNION SELECT * FROM accounts WHERE Rut = ? AND clave = ?", (Rut, clave, Rut, clave))
        user = cursor.fetchone()
        if user and len(user) > 1:
            session['user'] = user[1]  # Acceso por índice para el campo 'Rut'
            session['nombre'] = user[2]  # Acceso por índice para el campo 'Nombre'
            flash(f"Bienvenido, {Rut}", 'success')
            nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
            rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión
            cursor.close()
            return render_template('home.html', nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)
        else:
            flash("Rut o clave incorrectos", 'error')
        cursor.close()

    if 'user' in session and session['user']:
        return redirect(url_for('home'))

    return render_template("index.html")

from datetime import timedelta

@app.route('/logout', methods=['GET', 'POST'])
def logout():
     # Borra la sesión y restablece el tiempo de espera de sesión a 1 minuto
    session.clear()
        
    return redirect(url_for('index'))

#@app.route('/home')
#@proteger_ruta
#def home():
#    cursor = cnxn.cursor()
#    cursor.execute("SELECT * FROM Personas")
#    personas = cursor.fetchall()
#    cursor.close()
#    nombre_usuario = session.get('nombre', 'Desconocido')
#    rut_usuario = session.get('user', 'Desconocido')
#    return render_template('home.html', personas=personas, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)



@app.route('/home')
@proteger_ruta
def home():
        cursor = cnxn.cursor()

        # Consulta para obtener todos los datos de la tabla Personas
        cursor.execute("SELECT * FROM Personas")
        personas = cursor.fetchall()

        # Consulta para obtener todos los datos de la tabla EstructuraGrupos
        cursor.execute("SELECT * FROM EstructuraGrupos")
        grupo = cursor.fetchall()

        cursor.close()

        nombre_usuario = session.get('nombre', 'Desconocido')
        rut_usuario = session.get('user', 'Desconocido')

        return render_template('home.html', personas=personas, grupo=grupo, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)
    

#________________________________________________________________________________________

@app.route('/mostrar_nombre_grupo')
def mostrar_nombre_grupo():
    rut_buscado = request.args.get('rut')
    if not rut_buscado:
        return jsonify({'nombre_grupo': 'No hay datos proporcionados'})
    # Aquí va tu lógica para buscar el grupo
    consulta_sql = """
    SELECT EstructuraGrupos.NOMBRE
    FROM Personas
    INNER JOIN GrupoPersona ON Personas.RUT = GrupoPersona.Rut
    INNER JOIN EstructuraGrupos ON GrupoPersona.COD_CB = EstructuraGrupos.COD_CB
    WHERE Personas.RUT = ?
    """
    cursor = cnxn.cursor()
    cursor.execute(consulta_sql, [rut_buscado])
    resultado = cursor.fetchone()
    cursor.close()
    if resultado:
        nombre_grupo = resultado[0]
    else:
        nombre_grupo = 'No esta asociado a un grupo'
    return jsonify({'nombre_grupo': nombre_grupo})

#@app.route('/personas')
#@proteger_ruta
#def personas():
#    cursor = cnxn.cursor()
#    cursor.execute("SELECT * FROM Personas")
#    personas = cursor.fetchall()
#    nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
#    rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión
#    cursor.close()
#    return render_template('personas.html', personas=personas, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)


@app.route('/datos_sociales/<rut>')
def datos_sociales(rut):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM PERSONA_DATOS WHERE RUT = ?", (rut,))
    datos_sociales = cursor.fetchall()
    cursor.close()
    return render_template('datos_sociales.html', datos_sociales=datos_sociales)

@app.route('/editar_datos/<rut>', methods=['GET', 'POST'])
@proteger_ruta
def editar_datos(rut):
    cursor = cnxn.cursor()
    if request.method == 'POST':
        # Obtén todos los campos del formulario
        fecha_digita = request.form.get('Fecha_Digita')
        cta_ahorro = request.form.get('Cta_ahorro')
        a_nombre = request.form.get('A_Nombre')
        banco = request.form.get('Banco')
        aho_post = request.form.get('Aho_Post')
        aho_banco = request.form.get('Aho_Banco')
        aho_digi = request.form.get('Aho-Digi')
        rsh = request.form.get('RSH')
        personas_en_vivienda_rsh = request.form.get('Personas_en_vivienda_RSH')
        n_viviendas = request.form.get('N_viviendas')
        observaciones = request.form.get('Observaciones')
        estado = request.form.get('ESTADO')
        n_post = request.form.get('N_Post')
        monoparental = request.form.get('MONOPARENTAL')
        categoria = request.form.get('Categoría')
        discapacidad = request.form.get('DISCAPACIDAD')
        n_discapacitados = request.form.get('N_DISCAPACITADOS')
        victima_prision_politica = request.form.get('VICTIMA_PRISIÓN_POLÍTICA')
        nueva_postulacion = request.form.get('NUEVA_POSTULACIÓN')
        hacinamiento = request.form.get('HACINAMIENTO')
        rol = request.form.get('ROL')
        tasacion = request.form.get('TASACION')
        fec_dom = request.form.get('Fec_DOM')
        antiguedad = request.form.get('Antigüedad')
        fojas = request.form.get('FOJAS')
        numero = request.form.get('NUMERO')
        ano = request.form.get('AÑO')
        tipo_postulacion = request.form.get('TIPO_POSTULACION')
        antiguedad_vivienda = request.form.get('ANTIGUEDAD_VIVIENDA')
        accesibilidad = request.form.get('ACCESIBILIDAD')
        observacion = request.form.get('OBSERVACION')
        n_depto = request.form.get('N_DEPTO')
        
        try:
            # Actualiza todos los campos en la base de datos
            cursor.execute("""
                UPDATE PERSONA_DATOS
                SET [Fecha_Digita]=?, [Cta_ahorro]=?, [A NOMBRE]=?, [Banco]=?, [Aho_Post]=?, [Aho_Banco]=?, [Aho Digi]=?, [RSH]=?, [Personas en vivienda RSH]=?, [N_viviendas]=?, [Observaciones]=?, [ESTADO]=?, [N_Post]=?, [MONOPARENTAL]=?, [Categoría]=?, [DISCAPACIDAD]=?, [N_DISCAPACITADOS]=?, [VICTIMA PRISIÓN POLÍTICA]=?, [NUEVA POSTULACIÓN]=?, [HACINAMIENTO]=?, [ROL]=?, [TASACION]=?, [Fec_DOM]=?, [Antigüedad]=?, [FOJAS]=?, [NUMERO]=?, [AÑO]=?, [TIPO POSTULACION]=?, [ANTIGUEDAD VIVIENDA]=?, [ACCESIBILIDAD]=?, [OBSERVACION]=?, [N_DEPTO]=?
                WHERE [RUT]=?
            """, (fecha_digita, cta_ahorro, a_nombre, banco, aho_post, aho_banco, aho_digi, rsh, personas_en_vivienda_rsh, n_viviendas, observaciones, estado, n_post, monoparental, categoria, discapacidad, n_discapacitados, victima_prision_politica, nueva_postulacion, hacinamiento, rol, tasacion, fec_dom, antiguedad, fojas, numero, ano, tipo_postulacion, antiguedad_vivienda, accesibilidad, observacion, n_depto, rut))
            cnxn.commit()  # Guarda los cambios en la base de datos
            flash("Datos actualizados correctamente", 'success')
            cursor.close()
            return redirect(url_for('editar_datos', rut=rut))
        except Exception as e:
            flash("Error al actualizar los datos: " + str(e), 'error')

    cursor.execute("SELECT * FROM PERSONA_DATOS WHERE RUT = ?", (rut,))
    datos_sociales = cursor.fetchall()
    cursor.close()

    if datos_sociales:
        return render_template('datos_sociales.html', datos_sociales=datos_sociales)

    else:
        flash("RUT no encontrado", 'error')
        return redirect(url_for('personas'))

   

#__________________________________________________________________________________________

# Configurar cabecera para evitar caché en todas las respuestas
#@app.after_request
#def add_header(response):
#    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
#    response.headers['Pragma'] = 'no-cache'
#    response.headers['Expires'] = '-1'
#    return response

#@app.after_request
#def add_no_cache_header(response):
#    if response.status_code == 302:  # Redirection response
#        response.headers['Cache-Control'] = 'no-store, must-revalidate'
#    return response

#@app.route('/static/<path:filename>')
#def serve_static(filename):
#    response = send_from_directory('static', filename)
#    response.headers['Cache-Control'] = 'max-age=86400'  # Cache for 1 day
#    return response

# Nueva ruta para la tabla de directiva
@app.route('/directiva', defaults={'index': 0})
@app.route('/directiva/<int:index>')
@proteger_ruta
def directiva(index):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM PJ")
    data = cursor.fetchall()
    total_registros = len(data)
    primer_registro = None  # Inicializar como None
    nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
    rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión
    if total_registros == 0:
        cursor.close()
        return render_template('directiva.html', data=None, index=0, primer_registro=None, personas_asociadas=None)

    if 0 <= index < total_registros:
        primer_registro = data[index]
        # Obtener los datos de Personas asociados al Cod_PJ del primer registro de PJ
        cursor.execute("SELECT * FROM Personas INNER JOIN Dir_Serie ON Personas.RUT = Dir_Serie.Rut WHERE Dir_Serie.Cod_PJ = ?", primer_registro.Cod_PJ)
        personas_asociadas = cursor.fetchall()
        # Obtener el campo "Cargo" asociado al "Rut"
        cursor.execute("SELECT Cargo FROM Dir_Serie WHERE Rut = ?", (rut_usuario,))
        cargo_usuario = cursor.fetchone()
        cursor.close()
    else:
        cursor.close()
        return redirect(url_for('directiva', index=0, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario))

    return render_template('directiva.html', data=data, index=index, primer_registro=primer_registro, personas_asociadas=personas_asociadas, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario, cargo_usuario=cargo_usuario)

@app.route('/detalle_pj/<Cod_PJ>')
@proteger_ruta
def detalle_pj(Cod_PJ):
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM PJ WHERE Cod_PJ = ?", Cod_PJ)
    registro_actual = cursor.fetchone()
    campos_mostrar = ['Cod_PJ', 'Rol_PJ', 'Rut_PJ', 'Nombre', 'Dirección_1', 'Numero_1', 'Block_1',
                      'Villa_1', 'N_Depto_1', 'Dirección_2', 'Numero_2', 'Block_2', 'Villa_2',
                      'Comuna', 'Serie', 'Fecha', 'N_Depto_2']  
    cursor.close()  
    return render_template('detalle_pj.html' ,registro_actual=registro_actual, campos_mostrar=campos_mostrar)

@app.route('/agregar_pj', methods=['GET', 'POST'])
@proteger_ruta
def agregar_pj():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        Cod_PJ = request.form.get('Cod_PJ')
        Rol_PJ = request.form.get('Rol_PJ')
        Rut_PJ = request.form.get('Rut_PJ')
        Nombre = request.form.get('Nombre')
        Direccion_1 = request.form.get('Dirección_1')
        Numero_1 = request.form.get('Número_1')
        Block_1 = request.form.get('Block_1')
        Villa_1 = request.form.get('Villa_1')
        N_Depto_1 = request.form.get('N_Depto_1')
        Direccion_2 = request.form.get('Dirección_2')
        Numero_2 = request.form.get('Número_2')
        Block_2 = request.form.get('Block_2')
        Villa_2 = request.form.get('Villa_2')
        Comuna = request.form.get('Comuna')
        Serie = request.form.get('Serie')
        Fecha = request.form.get('Fecha')
        N_Depto_2 = request.form.get('N_Depto_2')
        
        try:
            # Ejecutar la consulta SQL para insertar un nuevo registro en la tabla PJ
            cursor.execute("INSERT INTO PJ (Cod_PJ, Rol_PJ, Rut_PJ, Nombre, Dirección_1, Numero_1, Block_1, Villa_1, N_Depto_1, Dirección_2, Numero_2, Block_2, Villa_2, Comuna, Serie, Fecha, N_Depto_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
               Cod_PJ, Rol_PJ, Rut_PJ, Nombre, Direccion_1, Numero_1, Block_1, Villa_1, N_Depto_1, Direccion_2, Numero_2, Block_2, Villa_2, Comuna, Serie, Fecha, N_Depto_2)
            # Confirmar los cambios en la base de datos
            cnxn.commit()
            cursor.close()
            # Mostrar la plantilla de éxito
            return render_template('guardado_exitoso_pj.html')
        except Exception as e:
            # En caso de error, puedes mostrar un mensaje de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error_al_guardar_pj.html', error_message=str(e))

    # Renderizar la página para agregar una nueva persona (formulario de ingreso)
    return render_template('agregar_pj.html')

@app.route('/editar_PJ/<Cod_PJ>', methods=['POST'])
@proteger_ruta
def editar_PJ(Cod_PJ):
    cursor = cnxn.cursor()
    datos = request.form
    query = '''UPDATE [dbo].[PJ]
               SET Rol_PJ = ?, Rut_PJ = ?, Nombre = ?, Dirección_1 = ?, Numero_1 = ?, Block_1 = ?, Villa_1 = ?, N_Depto_1 = ?, Dirección_2 = ?, Numero_2 = ?, Block_2 = ?, Villa_2 = ?, Comuna = ?, Serie = ?, Fecha = ?, N_Depto_2 = ?
               WHERE Cod_PJ = ?'''
    cursor.execute(query, (datos['Rol_PJ'], datos['Rut_PJ'], datos['Nombre'], datos['Dirección_1'], datos['Numero_1'], datos['Block_1'], datos['Villa_1'], datos['N_Depto_1'], datos['Dirección_2'], datos['Numero_2'], datos['Block_2'], datos['Villa_2'], datos['Comuna'], datos['Serie'], datos['Fecha'], datos['N_Depto_2'], Cod_PJ))
    cnxn.commit()
    cursor.close()
    flash('Registro actualizado con éxito', 'success')
    return redirect('/directiva')
    

@app.route('/eliminar_pj/<Cod_PJ>', methods=['GET', 'POST'])
@proteger_ruta
def eliminar_pj(Cod_PJ):
    cursor = cnxn.cursor()
    if request.method == 'POST':
        try:
            # Ejecutar consulta SQL para eliminar el registro de PJ
            cursor.execute("DELETE FROM PJ WHERE Cod_PJ = ?", Cod_PJ)
            cnxn.commit()
            flash(f'Registro con Código PJ {Cod_PJ} eliminado exitosamente.', 'success')
            cursor.close()
            return redirect('/directiva')
        except Exception as e:
            cursor.close()
            return f"Ocurrió un error: {str(e)}"

    # Si la solicitud es GET, mostrar una página de confirmación
    cursor.execute("SELECT * FROM PJ WHERE Cod_PJ = ?", Cod_PJ)
    registro_actual = cursor.fetchone()
    return render_template('eliminar_pj.html', registro_actual=registro_actual)


@app.route('/informe_social')
@proteger_ruta
def informe_social():
    cursor = cnxn.cursor()
    rut_usuario = session.get('user', 'Desconocido')
    try:
        # Fetch unique 'Tipo_Proy' values from the database
        cursor = cnxn.cursor()
        cursor.execute("""SELECT
                    EG.COD_CB,
                    EG.COD_RUKAN,
                    EG.NOMBRE AS Grupo_Nombre,
                    EG.COMUNA AS Grupo_Comuna,
                    EG.COD_PJ AS Grupo_Cod_PJ,
                    EG.Tipo_Proy,
                    EG.Año_Llamado,
                    PJ.[Rol_PJ] AS Rol_PJ_Dir_Serie,
                    P.RUT AS Rut_Personas,
                    P.Nombre AS Nombre_Personas,
                    P.[A_Paterno] AS A_Paterno_Personas,
                    P.[A_Materno] AS A_Materno_Personas,
                    P.Dirección AS Dirección_Personas,
                    P.Num AS Num_Direccion,
                    P.Piso AS Piso_Personas,
                    P.Block AS Block_Personas,
                    P.COMUNA AS Comuna_Personas,
                    P.Fono AS Fono_Personas,
                    P.[Estado] AS Estado_Personas
                    FROM EstructuraGrupos EG
                    LEFT JOIN PJ ON EG.COD_PJ = PJ.Cod_PJ
                    LEFT JOIN GrupoPersona GP ON EG.COD_CB = GP.COD_CB
                    LEFT JOIN PERSONA_DATOS DP ON GP.Rut = DP.RUT
                    LEFT JOIN Personas P ON GP.Rut = P.RUT;""")
        consulta = cursor.fetchall()

        cursor.execute("""SELECT EG.COMUNA AS COMUNA,
                    COUNT(GP.Rut) AS Cantidad_Personas
                    FROM EstructuraGrupos EG
                    LEFT JOIN GrupoPersona GP ON EG.COD_CB = GP.COD_CB
                    GROUP BY EG.COMUNA;""")
        comunas = cursor.fetchall()
        comunas_limpias = [unidecode(comuna[0]) for comuna in comunas]

        cursor.execute("""select distinct Tipo_Proy from EstructuraGrupos""")
        Tipo_Proyecto = cursor.fetchall()
        Tipo_Proyecto_limpio = [unidecode(str(Tipo_Proyecto[0])) for Tipo_Proyecto in Tipo_Proyecto] 

        cursor.execute("""SELECT DISTINCT EG.COMUNA AS COMUNA,
        COUNT(GP.Rut) AS Cantidad_Personas
        FROM EstructuraGrupos EG
        LEFT JOIN GrupoPersona GP ON EG.COD_CB = GP.COD_CB
        GROUP BY EG.COMUNA;""")
        cont_comuna = cursor.fetchall()

        cursor.execute("""SELECT DISTINCT EG.Tipo_Proy AS Tipo_Proyecto,
                COUNT(GP.Rut) AS Cantidad_Personas
                FROM EstructuraGrupos EG
                LEFT JOIN GrupoPersona GP ON EG.COD_CB = GP.COD_CB
                GROUP BY EG.Tipo_Proy;
                """, )
        tipoProy = cursor.fetchall()


        cursor.close()
        return render_template('informe_social.html',consulta=consulta , rut_usuario=rut_usuario , comunas_limpias = comunas_limpias, Tipo_Proyecto_limpio= Tipo_Proyecto_limpio , cont_comuna=cont_comuna, tipoProy=tipoProy )


    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500


    #finally:
    #    if cursor is not None:
    #        cursor.close()

#________________________________________________________________________________________

@app.errorhandler(500)
@proteger_ruta
def internal_server_error(e):
    return "Ocurrió un error interno en el servidor. Por favor, inténtalo nuevamente más tarde.", 500

campo_traduccion = {
    'Cod_PJ': 'Código PJ',
    'Rol_PJ': 'Rol PJ',
    # Agrega más campos aquí
}

@app.route('/pj', defaults={'index': 0})    
@app.route('/pj/<int:index>')
@proteger_ruta
def pj(index): 
    cursor = cnxn.cursor()
    cursor.execute("SELECT * FROM PJ")
    data = cursor.fetchall()
    total_registros = len(data)
    if total_registros == 0:
        cursor.close()
        return render_template('directiva.html', data=None, index=0, primer_registro=None, personas_asociadas=None)
    
    # Verificar si el índice está dentro de los límites
    if 0 <= index < total_registros:
        registro_actual = data[index]
        cursor.close()
    else:
        cursor.close()
        return redirect(url_for('pj', index=0))

    # Renderizar el formulario PJ y pasar los datos necesarios
    return render_template('PJ.html', registro_actual=registro_actual, total_registros=total_registros, index=index)


@app.route('/static/js/session_timeout.js')
def static_js_session_timeout():
    try:
        with open('static/js/session_timeout.js', 'r') as file:
            content = file.read()
        return content, 200, {'Content-Type': 'application/javascript'}
    except Exception as e:
        # Manejar errores adecuadamente
        return str(e), 500

# ...

@app.route('/search_directiva', methods=['POST'])
@proteger_ruta
def search_directiva():
    cursor = cnxn.cursor()
    search_term = request.form['search_term']
    cursor.execute("SELECT * FROM PJ WHERE Nombre LIKE ?", (f"%{search_term}%",))
    result = cursor.fetchall()
    if result:
        primer_registro = result[0]
        # Obtener los datos de Personas asociados al Cod_PJ del primer registro de PJ
        cursor.execute("SELECT * FROM Personas INNER JOIN Dir_Serie ON Personas.RUT = Dir_Serie.Rut WHERE Dir_Serie.Cod_PJ = ?", primer_registro.Cod_PJ)
        personas_asociadas = cursor.fetchall()
        cursor.close()
        return render_template('directiva.html', data=result, index=0, primer_registro=primer_registro, personas_asociadas=personas_asociadas)
    else:
        # No se encontraron resultados, limpiamos la variable de personas asociadas y renderizamos la plantilla con el primer_registro en None
        cursor.close()
        return render_template('directiva.html', data=result, index=0, primer_registro=None, personas_asociadas=None, message="No se encontraron resultados")



@app.route('/search', methods=['POST'])
def search():
    try:
        cursor = cnxn.cursor()
        term = request.form.get('term', '').lower()  # Convertir a minúsculas
        
        # Ejecuta la consulta SQL (ajusta la consulta según tus necesidades)
        cursor.execute("SELECT * FROM Personas WHERE LOWER(rut) LIKE ? OR LOWER(nombre) LIKE ?", ('%' + term + '%', '%' + term + '%'))

        # Obtiene todos los resultados
        results = cursor.fetchall()

        # Puedes formatear los resultados según sea necesario
        formatted_results = [dict(zip([column[0] for column in cursor.description], row)) for row in results]

        # Retorna los resultados como JSON
        return jsonify(formatted_results)

    except Exception as e:
        # Maneja las excepciones adecuadamente en un entorno de producción
        return jsonify({'error': str(e)})
    


@app.route('/searchRukan', methods=['POST'])
def searchRukan():
    try:
        cursor = cnxn.cursor()
        term = request.form.get('term', '').lower()  # Convertir a minúsculas
        
        # Ejecuta la consulta SQL (ajusta la consulta según tus necesidades)
        cursor.execute("SELECT * FROM EstructuraGrupos WHERE LOWER(NOMBRE) LIKE ? OR LOWER(COD_RUKAN) LIKE ?", ('%' + term + '%', '%' + term + '%'))
        # Obtiene todos los resultados
        results = cursor.fetchall()

        # Puedes formatear los resultados según sea necesario
        formatted_results = [dict(zip([column[0] for column in cursor.description], row)) for row in results]

        # Retorna los resultados como JSON
        return jsonify(formatted_results)

    except Exception as e:
        # Maneja las excepciones adecuadamente en un entorno de producción
        return jsonify({'error': str(e)})
    

# Ruta para editar una persona
@app.route('/editar_persona/<string:rut>', methods=['GET', 'POST'])
@proteger_ruta
def editar_persona(rut):
    cursor = cnxn.cursor()
    # Obtener los datos de la persona con el RUT proporcionado
    cursor.execute("SELECT * FROM Personas WHERE RUT = ?", rut)
    persona = cursor.fetchone()

    if request.method == 'POST':
        # Obtener los nuevos datos del formulario de edición
        nombre = request.form['nombre']
        a_paterno = request.form['a_paterno']
        a_materno = request.form['a_materno']
        nacionalidad = request.form['nacionalidad']
        sexo = request.form['sexo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        estado_civil = request.form['estado_civil']
        direccion = request.form['direccion']
        piso = request.form['piso']
        num = request.form['num']
        block = request.form['block']
        villa = request.form['villa']
        comuna = request.form['comuna']
        fono = request.form['fono']
        correo = request.form['correo']
        vigencia_cedula = request.form['vigencia_cedula']
        rut_cony = request.form['rut_cony']
        estado = request.form['estado']
        fecha_act = request.form['fecha_act']
        n_depto = request.form['n_depto']

        try:
            # Ejecutar la consulta SQL para actualizar los datos de la persona en la tabla de Personas
            cursor.execute("UPDATE Personas SET Nombre = ?, A_Paterno = ?, A_Materno = ?, Nacionalidad = ?, Sexo = ?, Fecha_de_Nacimiento = ?, Edad = ?, Estado_civil = ?, Dirección = ?, Piso = ?, Num = ?, Block = ?, Villa = ?, COMUNA = ?, Fono = ?, Correo = ?, Vigencia_cedula = ?, Rut_Cony = ?, Estado = ?, Fecha_Act = ?, N_Depto = ? WHERE RUT = ?",
                           nombre, a_paterno, a_materno, nacionalidad, sexo, fecha_nacimiento, edad, estado_civil, direccion, piso, num, block, villa, comuna, fono, correo, vigencia_cedula, rut_cony, estado, fecha_act, n_depto, rut)

            # Confirmar los cambios en la base de datos
            cnxn.commit()
            cursor.close()
            # Redirigir a la página personas.html para que se actualice la lista
            return redirect(url_for('personas'))
        except Exception as e:
            # En caso de error, puedes mostrar un mensaje de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error.html', error_message=str(e))

    # Si es un método GET, renderizar la página de edición con los datos de la persona
    return render_template('editar_persona.html', persona=persona)

# Ruta para eliminar una persona
@app.route('/eliminar_persona/<string:rut>')
@proteger_ruta
def eliminar_persona(rut):
    cursor = cnxn.cursor()
    try:
         # 1. Elimina el registro de la persona de la tabla 'Personas'
        cursor.execute("DELETE FROM Personas WHERE RUT = ?", rut)

        # 2. Elimina los registros asociados de la tabla 'PERSONA_DATOS' 
        cursor.execute("DELETE FROM PERSONA_DATOS WHERE RUT = ?", rut)

        # Confirma los cambios en la base de datos
        cnxn.commit()
        cursor.close()
        # Redirigir a la página personas.html para que se actualice la lista
        return redirect(url_for('personas'))
    except Exception as e:
        # En caso de error, puedes mostrar un mensaje de error o realizar alguna acción adicional
        cursor.close()
        return render_template('error.html', error_message=str(e))

# Ruta para agregar una nueva persona
@app.route('/agregar_persona', methods=['GET', 'POST'])
@proteger_ruta
def agregar_persona():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        rut = request.form['rut']
        nombre = request.form['nombre']
        a_paterno = request.form['a_paterno']
        a_materno = request.form['a_materno']
        nacionalidad = request.form['nacionalidad']
        sexo = request.form['sexo']
        fecha_nacimiento = request.form['fecha_nacimiento']
        edad = request.form['edad']
        estado_civil = request.form['estado_civil']
        direccion = request.form['direccion']
        piso = request.form['piso']
        num = request.form['num']
        block = request.form['block']
        villa = request.form['villa']
        comuna = request.form['comuna']
        fono = request.form['fono']
        correo = request.form['correo']
        vigencia_cedula = request.form['vigencia_cedula']
        rut_cony = request.form['rut_cony']
        estado = request.form['estado']
        fecha_act = request.form['fecha_act']
        n_depto = request.form['n_depto']
        # Obtener el valor del campo "rut_persona_datos" del formulario
        rut_persona_datos = request.form['rut']

        try:
            # Ejecutar la consulta SQL para insertar la nueva persona en la tabla de Personas
            cursor.execute(
                "INSERT INTO Personas (RUT, Nombre, A_Paterno, A_Materno, Nacionalidad, Sexo, Fecha_de_Nacimiento, Edad, Estado_civil, Dirección, Piso, Num, Block, Villa, COMUNA, Fono, Correo, Vigencia_cedula, Rut_Cony, Estado, Fecha_Act, N_Depto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                rut, nombre, a_paterno, a_materno, nacionalidad, sexo, fecha_nacimiento, edad, estado_civil, direccion, piso, num, block, villa, comuna, fono, correo, vigencia_cedula, rut_cony, estado, fecha_act, n_depto)
            # Ejecutar la consulta SQL para insertar el "rut" en la tabla de Persona_Datos
            cursor.execute(
                "INSERT INTO Persona_Datos (RUT) VALUES (?)",
                rut_persona_datos)
            # Confirmar los cambios en la base de datos
            cnxn.commit()
            cursor.close()
            # Mostrar la plantilla de éxito
            return render_template('exito_guardar_persona.html')
        except Exception as e:
            # En caso de error, puedes mostrar un mensaje de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error_guardar_persona.html', error_message=str(e))

    # Renderizar la página para agregar una nueva persona (formulario de ingreso)
    return render_template('agregar_persona.html')



# ...

# Ruta para ver el detalle de una persona
@app.route('/ver_detalle/<string:rut>')
@proteger_ruta
def ver_detalle(rut):
    cursor = cnxn.cursor()
    # Obtener los datos de la persona con el RUT proporcionado
    cursor.execute("SELECT * FROM Personas WHERE RUT = ?", rut)
    persona = cursor.fetchone()
    cursor.close()
    # Renderizar la plantilla ver_detalle.html con los datos de la persona
    return render_template('ver_detalle.html', persona=persona)

# ...
@app.route('/error401')
@proteger_ruta
def error401():
    return render_template('error401.html')

# Ruta para ver el detalle de un grupo
@app.route('/estructura_grupos/<string:COD_CB>', methods=['GET', 'POST'])
@proteger_ruta
def ver_detalle_grupo(COD_CB):
    cursor = cnxn.cursor()
    #cursor = None  # Initialize the cursor variable outside the try block
    mensaje_exito = None  # Inicializa el mensaje de éxito como nulo
    rut_usuario = session.get('user', 'Desconocido')

    try:
        if request.method == 'POST':
            # Aquí manejas la lógica para guardar los cambios en el grupo.
            # Puedes realizar las operaciones de base de datos necesarias aquí.
            
            # Después de guardar los cambios con éxito, establece el mensaje de éxito.
            mensaje_exito = "Cambios guardados con éxito."

        # Implementar la lógica para obtener los detalles del grupo con el 'COD_CB' proporcionado
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM EstructuraGrupos WHERE COD_CB = ?", COD_CB)
        grupo = cursor.fetchone()
        cursor.close()
        # Check if the group is not found
        if grupo is None:
            return render_template('error.html', error_message="Grupo no encontrado")

        return render_template('estructura_grupos.html', grupo=grupo, mensaje_exito=mensaje_exito , rut_usuario=rut_usuario)

    except Exception as e:
        # En caso de algún error, imprimirlo para depuración.
        print("Error:", e)
        return render_template('error.html', error_message="Error al obtener los detalles del grupo")

    finally:
        # Close the cursor in the finally block to ensure it's closed even if there's an exception
        if cursor is not None:
            cursor.close()
        # Do not close the connection here to keep it open for other requests


@app.route('/formulario/<string:COD_CB>', methods=['GET', 'POST'])
@proteger_ruta
def formulario(COD_CB):
    cursor = cnxn.cursor()
    #cursor = None  # Initialize the cursor variable outside the try block
    mensaje_exito = None  # Inicializa el mensaje de éxito como nulo
    rut_usuario = session.get('user', 'Desconocido')

    try:
        if request.method == 'POST':
            # Aquí manejas la lógica para guardar los cambios en el grupo.
            # Puedes realizar las operaciones de base de datos necesarias aquí.
            
            # Después de guardar los cambios con éxito, establece el mensaje de éxito.
            mensaje_exito = "Cambios guardados con éxito."

        # Implementar la lógica para obtener los detalles del grupo con el 'COD_CB' proporcionado
        cursor = cnxn.cursor()
        cursor.execute("SELECT * FROM EstructuraGrupos WHERE COD_CB = ?", COD_CB)
        grupo = cursor.fetchone()
        cursor.close()
        # Check if the group is not found
        if grupo is None:
            return render_template('error.html', error_message="Grupo no encontrado")

        return render_template('formulario.html', grupo=grupo, mensaje_exito=mensaje_exito , rut_usuario=rut_usuario)

    except Exception as e:
        # En caso de algún error, imprimirlo para depuración.
        print("Error:", e)
        return render_template('error.html', error_message="Error al obtener los detalles del grupo")

    finally:
        # Close the cursor in the finally block to ensure it's closed even if there's an exception
        if cursor is not None:
            cursor.close()
        # Do not close the connection here to keep it open for other requests

@app.route('/ver_detalle_grupos/<string:COD_CB>')
@proteger_ruta
def ver_detalle_grupos(COD_CB):
    cursor = cnxn.cursor()
    rut_usuario = session.get('user', 'Desconocido')
    #cursor = None
    try:
        cursor = cnxn.cursor()
        # Consulta para obtener información de la tabla "EstructuraGrupos"
        cursor.execute("SELECT COD_CB, COD_RUKAN, NOMBRE, COMUNA, Tipo_Proy FROM EstructuraGrupos WHERE COD_CB = ?", COD_CB)
        gruposcarlos = cursor.fetchall()
        # Consulta para obtener información de la tabla "GrupoPersona" y "Personas"
        cursor.execute("SELECT g.Rut, g.Estado, p.Nombre, p.A_Paterno, p.A_Materno, p.Dirección, p.Num, p.Piso, p.Block, p.Villa, p.COMUNA, p.Fono " +  
                       "FROM Personas AS p " + 
                       "JOIN GrupoPersona AS g ON g.Rut = p.Rut " +
                       "WHERE g.COD_CB = ?", COD_CB)
        dataGrupoPersona = cursor.fetchall()
        cursor.close()       
        return render_template('ver_detalle_grupos.html', gruposcarlos=gruposcarlos, dataGrupoPersona=dataGrupoPersona, COD_CB=COD_CB , rut_usuario=rut_usuario)

    except Exception as e:
        print("Error:", e)
        return jsonify(error=str(e)), 500
    finally:
        if cursor is not None:
            cursor.close()

# Vista que maneja la inserción de datos en la tabla GrupoPersona
@app.route('/añadir_persona_grupo', methods=['GET', 'POST'])
@proteger_ruta
def añadir_persona_grupo():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        COD_CB = request.form.get('COD_CB')
        Rut = request.form.get('Rut')
        Estado = request.form.get('Estado')  # Recupera el valor del campo oculto "Estado"
        # Añade aquí la lógica para guardar los datos en la tabla GrupoPersona y Persona
        # Puedes usar una consulta SQL de inserción para cada tabla

        try:
            # Ejecutar la consulta SQL para insertar los datos en la tabla GrupoPersona
            cursor.execute("INSERT INTO GrupoPersona (COD_CB, Rut, Estado) VALUES (?, ?, ?)",
                           (COD_CB, Rut, Estado))
            cnxn.commit()  # Confirmar los cambios en la base de datos

            # Añade aquí la lógica para guardar los datos en la tabla Persona
            # Usa una consulta similar para insertar los datos en la tabla Persona
            cursor.close()
            # Redirigir a una página de éxito o a la página deseada después de guardar los datos
            return redirect(url_for('guardado_exitoso_personarupo'))
        except Exception as e:
            cursor.close()
            return jsonify(error=str(e)), 500

    # Obtener los parámetros de la URL
    COD_CB = request.args.get('COD_CB')
    NOMBRE = request.args.get('NOMBRE')
    Tipo_Proy = request.args.get('Tipo_Proy')

    # Obtener los datos de Personas para mostrar en la tabla
    cursor.execute("SELECT * FROM Personas")
    personas = cursor.fetchall()
    cursor.close()
    return render_template('añadir_persona_grupo.html', personas=personas, COD_CB=COD_CB, NOMBRE=NOMBRE, Tipo_Proy=Tipo_Proy)

@app.route('/guardar_cambios', methods=['POST'])
def guardar_cambios():
    cursor = cnxn.cursor()
    try:
        Rut = request.form.get('Rut')
        Estado = request.form.get('Estado')
        Nombre = request.form.get('Nombre')
        ApellidoP = request.form.get('ApellidoP')
        ApellidoM = request.form.get('ApellidoM')
        Direccion = request.form.get('Direccion')
        Numero = request.form.get('Numero')
        Piso = request.form.get('Piso')
        Block = request.form.get('Block')
        Villa = request.form.get('Villa')
        Telefono = request.form.get('Telefono')

        # Agrega declaraciones de impresión para verificar los datos que se están procesando
        print("Rut:", Rut)
        print("Estado:", Estado)
        print("Nombre:", Nombre)
        print("ApellidoP:", ApellidoP)
        print("ApellidoM:", ApellidoM)
        print("Direccion:", Direccion)
        print("Numero:", Numero)
        print("Piso:", Piso)
        print("Block:", Block)
        print("Villa:", Villa)
        print("Telefono:", Telefono)

        # ...

        # Agrega más declaraciones de impresión para verificar el flujo de ejecución
        cursor.execute("UPDATE GrupoPersona SET Estado = ? WHERE Rut = ?", (Estado, Rut))
        cnxn.commit()
        print("Actualizado GrupoPersona")

        cursor.execute("UPDATE Personas SET Nombre = ?, A_Paterno = ?, A_Materno = ?, Dirección = ?, Num = ?, Piso = ?, Block = ?, Villa = ?, Fono = ? WHERE Rut = ?", 
                      (Nombre, ApellidoP, ApellidoM, Direccion, Numero, Piso, Block, Villa, Telefono, Rut))
        cnxn.commit()
        print("Actualizado Personas")
        cursor.close()
        return jsonify({"message": "Cambios guardados con éxito"})
    except Exception as e:
        print("Error:", str(e))
        cursor.close()
        return jsonify({"error": str(e)}), 500



@app.route('/eliminar_persona_grupo', methods=['POST']) # type: ignore
@proteger_ruta
def eliminar_persona_grupo():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        COD_CB = request.form.get('COD_CB')
        Rut = request.form.get('Rut')
        Estado = request.form.get('Estado')

        try:
            # Ejecuta una consulta SQL para eliminar el registro en la tabla GrupoPersona
            cursor.execute("DELETE FROM GrupoPersona WHERE COD_CB = ? AND Rut = ? AND Estado = ?", (COD_CB, Rut, Estado))
            cnxn.commit()
            print("Registro eliminado con éxito")
            cursor.close()
            # Redirige nuevamente a la misma página con los parámetros para cargar el mismo registro
            return redirect(url_for('ver_detalle_grupos', COD_CB=COD_CB))  # Reemplaza 'nombre_de_tu_vista' con el nombre de tu vista

        except Exception as e:
            print(f"Error al eliminar el registro: {str(e)}")
            cursor.close()
            return jsonify({"error": str(e)}), 500



@app.route('/grupo_tabla', methods=['GET'])
@proteger_ruta
def grupo_tabla():
    cursor = cnxn.cursor()
    try:
        # Fetch unique 'Tipo_Proy' values from the database
        cursor = cnxn.cursor()
        cursor.execute("SELECT DISTINCT Tipo_Proy FROM EstructuraGrupos")
        tipos_proy = [tipo[0] for tipo in cursor.fetchall()]  # Convert the result to a list

        # Get the selected 'Tipo_Proy' filter from the URL query parameters
        filtro = request.args.get('filtro', '')


        # Get the current page number from the URL query parameters
        page = int(request.args.get('page', 1))

        # Define the number of records to show per page
        records_per_page = 10

        if filtro:
            # If a filter is selected, fetch the filtered groups
            cursor.execute("SELECT COD_CB, COD_RUKAN, NOMBRE, COMUNA, Tipo_Proy FROM EstructuraGrupos WHERE Tipo_Proy = ?", filtro)
            
        else:
            # If no filter is selected, fetch all groups
            cursor.execute("SELECT COD_CB, COD_RUKAN, NOMBRE, COMUNA, Tipo_Proy FROM EstructuraGrupos")

        grupos = cursor.fetchall()
        
        nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
        rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión

        cursor.execute("SELECT Estado, COUNT(*) as Cantidad_de_Personas FROM GrupoPersona GROUP BY Estado")
        estado = cursor.fetchall()

        formatted_estado = ', '.join(f"{valor} ({estado})" for valor, estado in estado)


        grupo_actual = {
            'NOMBRE': 'Nombre del Grupo Actual'
        }
        cursor.close()
        return render_template('grupo_tabla.html', grupos=grupos, tipos_proy=tipos_proy, filtro=filtro, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario , formatted_estado=formatted_estado)


    except Exception as e:
        print("Error:", e)
        return render_template('error.html', error_message="Error al cargar la tabla de grupos")

    #finally:
    #    if cursor is not None:
    #        cursor.close()


@app.route('/eliminar_grupo/<cod_cb>', methods=['DELETE'])
@proteger_ruta
def eliminar_grupo(cod_cb):
    cursor = cnxn.cursor()
    try:
        # Aquí debes ejecutar la consulta SQL para eliminar el grupo en la base de datos
        # Por ejemplo:
        cursor.execute("DELETE FROM EstructuraGrupos WHERE COD_CB = ?", cod_cb)
        cnxn.commit()  # Importante: Confirmar la transacción
        cursor.close()
        return jsonify({'success': True})
    except Exception as e:
        print(str(e))
        cursor.close()
        return jsonify({'success': False})


# ..
@app.route('/agregar_grupo', methods=['GET', 'POST'])
@proteger_ruta
def agregar_grupo():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        # Obtener los datos ingresados en el formulario
        cod_rukan = request.form['cod_rukan']
        nombre = request.form['nombre']
        comuna = request.form['comuna']
        tipo_proy = request.form['tipo_proy']

        try:
            # Ejecutar la consulta SQL para insertar el nuevo grupo en la tabla EstructuraGrupos
            cursor.execute("INSERT INTO EstructuraGrupos (COD_RUKAN, NOMBRE, COMUNA, Tipo_Proy) VALUES (?, ?, ?, ?)",
                           cod_rukan, nombre, comuna, tipo_proy)
            cnxn.commit()  # Confirmar los cambios en la base de datos
            cursor.close()
            # Redirigir a la página de grupos después de agregar exitosamente
            return redirect(url_for('exito_grupo'))
        except Exception as e:
            # En caso de error, puedes mostrar una página de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error_grupo.html', error_message=str(e))

    # Si es un método GET, simplemente mostrar el formulario para agregar un nuevo grupo
    return render_template('agregar_grupo.html')

@app.route('/añadir_a_directiva', methods=['GET', 'POST'])
@proteger_ruta
def añadir_a_directiva():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        cod_pj = request.form.get('Cod_PJ')
        Serie_Vigente = request.form['Serie_Vigente']
        cargo = request.form['Cargo']
        Rut = request.form['Rut']
        try:
            # Ejecutar la consulta SQL para insertar los datos en la tabla Dir_Serie
            cursor.execute("INSERT INTO dir_serie (Cod_PJ, Serie_Vigente, Rut, Cargo) VALUES (?, ?, ?, ?)",
                           cod_pj, Serie_Vigente, Rut, cargo)
            cnxn.commit()  # Confirmar los cambios en la base de datos
            cursor.close()
            # Redirigir a una página de éxito o a la página deseada después de guardar los datos
            return redirect(url_for('guardado_exitosamente'))
        except Exception as e:
            # En caso de error, puedes mostrar una página de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error_guardado.html', error_message=str(e))

    # Obtener los datos de Personas para mostrar en la tabla
    cursor.execute("SELECT * FROM Personas")
    personas = cursor.fetchall()

    # Obtener los parámetros de consulta de la URL
    cod_pj = request.args.get('Cod_PJ')
    nombre = request.args.get('nombre')
    serie = request.args.get('serie')
    cursor.close()
    return render_template('añadir_a_directiva.html', personas=personas, cod_pj=cod_pj, nombre=nombre, serie=serie)


@app.route('/guardado_exitosamente')
@proteger_ruta
def guardado_exitosamente():
    return render_template('guardado_exitosamente.html')

@app.route('/exito_grupo')
@proteger_ruta
def exito_grupo():
    return render_template('exito_grupo.html')

@app.route('/guardado_exitoso_pj.html')
@proteger_ruta
def guardado_exitoso_pj():
    return render_template('guardado_exitoso_pj.html')

@app.route('/guardado_exitoso_personarupo')
@proteger_ruta
def guardado_exitoso_personarupo():
    return render_template('guardado_exitoso_personarupo.html')

@app.route('/error_grupo')
@proteger_ruta
def error_grupo():
    return render_template('error_grupo.html')

@app.route('/error_al_guardar_pj.html')
@proteger_ruta
def error_al_guardar_pj():
    return render_template('error_al_guardar_pj.html')

@app.route('/eepp_egis', methods=['GET'])
@proteger_ruta
def eepp_egis():
    cursor = cnxn.cursor()
    # Obtener el parámetro cod_rukan desde la URL
    cod_rukan = request.args.get('cod_rukan', '')  # Si no se proporciona el parámetro, establecerlo como cadena vacía

    # Obtener los datos de la tabla EP_Const que coincidan con el campo COD_RUKAN
    cursor.execute("SELECT *, [Est Pago] as Est_Pago FROM EP_Const WHERE CODIGO_RUKAN = ?", cod_rukan)
    ep_const_data = cursor.fetchall()

    # Obtener los datos de la tabla EP_Serviu que coincidan con el campo COD_RUKAN
    cursor.execute("SELECT * FROM EP_Serviu WHERE CODIGO_RUKAN = ?", cod_rukan)
    ep_serviu_data = cursor.fetchall()
    cursor.close()
    return render_template('eepp_egis.html', ep_const_data=ep_const_data, ep_serviu_data=ep_serviu_data)

@app.route('/eliminar_persona_asociada/<int:id>', methods=['GET', 'POST'])
@proteger_ruta
def eliminar_persona_asociada(id):
    cursor = cnxn.cursor()
    if request.method == 'POST':
        try:
            # Obtener el RUT de la persona asociada al id proporcionado
            cursor.execute("SELECT Rut FROM Dir_Serie WHERE Id = ?", id)
            rut = cursor.fetchone()
            # Ejecutar la consulta SQL para eliminar la persona asociada de la tabla Dir_Serie
            cursor.execute("DELETE FROM Dir_Serie WHERE Id = ?", id)
            cnxn.commit()  # Confirmar los cambios en la base de datos
            cursor.close()
            # Redirigir a una página de éxito o a la página deseada después de eliminar la persona
            return redirect(url_for('directiva', index=0))
        except Exception as e:
            # En caso de error, puedes mostrar una página de error o realizar alguna acción adicional
            cursor.close()
            return render_template('error.html', error_message=str(e))
    # Obtener los datos de Personas asociados al id proporcionado
    cursor.execute("SELECT * FROM Personas INNER JOIN Dir_Serie ON Personas.RUT = Dir_Serie.Rut WHERE Dir_Serie.Id = ?", id)
    persona_asociada = cursor.fetchone()
    # Renderizar la plantilla eliminar_persona_asociada.html con los datos de la persona asociada
    return render_template('eliminar_persona_asociada.html', persona_asociada=persona_asociada)

# Ejecutar la consulta SQL para eliminar la persona asociada de la tabla Dir_Serie


def conectar_bd():
    # Conexión a SQL Server
    password = 'Brss213.--'
    encoded_password = quote(password)
    conn_str = (
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
    conn = pyodbc.connect(conn_str)
    return conn


@app.route('/guardar_eepp_egis', methods=['POST'])
@proteger_ruta
def guardar_eepp_egis():
    cursor = cnxn.cursor()
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario para EP_Const
            id_const = request.form.getlist('Id[]')
            codigo_rukan_const = request.form.getlist('CODIGO_RUKAN[]')
            nombre_const = request.form.getlist('Nombre[]')
            f_confec_const = request.form.getlist('F_Confec[]')
            f_envio_const = request.form.getlist('F_Envio[]')
            f_recep_const = request.form.getlist('F_Recep[]')
            est_pago_const = request.form.getlist('Est_Pago[]')
            monto_uf_const = request.form.getlist('Monto UF[]')
            fecha_pago_const = request.form.getlist('Fecha Pago[]')
            monto_pagdo_const = request.form.getlist('Monto Pagdo[]')
            estado_const = request.form.getlist('Estado[]')
            observacion_const = request.form.getlist('Observacion[]')
            # Obtener datos del formulario para EP_Serviu
            id_serviu = request.form.getlist('Id2[]')
            codigo_rukan_serviu = request.form.getlist('CODIGO_RUKAN[]')
            n_op_serviu = request.form.getlist('N_OP[]')
            fecha_ingrso_serviu = request.form.getlist('Fecha_Ingreso[]')
            rut_paguese_a_serviu = request.form.getlist('Rut_Paguese_a[]')
            a_pagar_serviu = request.form.getlist('A_Pagar[]')
            total_pesos_serviu = request.form.getlist('Total_Pesos[]')
            n_egreso_serviu = request.form.getlist('N_Egreso[]')
            fecha_egreso_serviu = request.form.getlist('Fecha_Egreso[]')
            retiro_cheque_serviu = request.form.getlist('Retiro_Cheque[]')
            # Actualizar registros en la tabla EP_Const
            for i in range(len(id_const)):
                cursor.execute("UPDATE EP_Const SET CODIGO_RUKAN=?, Nombre=?, F_Confec=?, F_Envio=?, F_Recep=?, [Est Pago]=?, [Monto UF]=?, [Fecha Pago]=?, [Monto Pagdo]=?, Estado=?, Observacion=? WHERE ID=?", (codigo_rukan_const[i], nombre_const[i], f_confec_const[i], f_envio_const[i], f_recep_const[i], est_pago_const[i], monto_uf_const[i], fecha_pago_const[i], monto_pagdo_const[i], estado_const[i], observacion_const[i], id_const[i]))
            # Actualizar registros en la tabla EP_Servi
            for i in range(len(id_serviu)):
                cursor.execute("UPDATE EP_Serviu SET CODIGO_RUKAN=?, N_OP=?, Fecha_Ingreso=?, Rut_Paguese_a=?, A_Pagar=?, Total_Pesos=?, N_Egreso=?, Fecha_Egreso=?, Retiro_Cheque=? WHERE ID=?", (codigo_rukan_serviu[i], n_op_serviu[i], fecha_ingrso_serviu[i], rut_paguese_a_serviu[i], a_pagar_serviu[i], total_pesos_serviu[i], n_egreso_serviu[i], fecha_egreso_serviu[i], retiro_cheque_serviu[i], id_serviu[i]))
            # Confirmar los cambios en la base de datos
            cnxn.commit()
            flash("Cambios guardados exitosamente", 'success')
            cursor.close()
        except Exception as e:
            print("Error al insertar datos:", e)
            flash("Error al insertar datos en la base de datos.", 'error')
            cursor.close()
    # Redirige al usuario a la página actual para refrescar
    return redirect(request.referrer)

# Ruta para guardar o actualizar un grupo

@app.route('/guardar_grupo', methods=['POST'])
@proteger_ruta
def guardar_grupo():
    # Resto del código para procesar y guardar los datos
    def insertar_datos_en_bd(data):
        cursor = cnxn.cursor()
        conn = conectar_bd()
        cursor = conn.cursor()

        campos_requeridos = ['COD_CB', 'COD_RUKAN']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return jsonify({"success": False, "message": f"El campo '{campo}' es requerido y no puede estar vacío."}), 400

        update_query = """
            UPDATE EstructuraGrupos
            SET 
                COD_RUKAN = ?,
                NOMBRE = ?,
                COMUNA = ?,
                COD_PJ = ?,
                Tipo_Proy = ?,
                N_Llamado = ?,
                Año_Llamado = ?,
                F_Llamado = ?,
                N_Resolucion = ?,
                F_resolucion = ?,
                N_Sel = ?,
                N_Post = ?,
                N_Hab = ?,
                F_inic_Sub = ?,
                F_finSubs = ?,
                OBSERV = ?,
                Rut_constr = ?,
                N_Renun = ?,
                Fec_Sol_Prorr = ?,
                Res_Prorr = ?,
                TOTAL_AT = ?,
                T_Pagado_E = ?,
                Saldo_Eg = ?,
                Cobro_Eg = ?,
                OBS_E = ?,
                EST_cobro_Eg = ?,
                T_Subs_C = ?,
                T_Ahorro = ?,
                T_Pagado_C = ?,
                Saldo = ?,
                En_Cobro = ?,
                OBS_C = ?,
                ESTADO_cobro = ?,
                A_FAV_EG = ?,
                T_Egis = ?,
                M_Boleta = ?,
                Num_B_CF = ?,
                BG_CF = ?,
                FOLIO_Egis = ?,
                F_Venc_Egis = ?,
                Inst_egis = ?,
                Est_BG_Eg = ?,
                Est_S_BG_Eg = ?,
                OBS_BG_eg = ?,
                A_FAV_CtRa = ?,
                T_ctra = ?,
                M_Boleta_ctra = ?,
                N_B_CF_Ctra = ?,
                BG_CF_Ctra = ?,
                FOLIO_ctra = ?,
                F_VENC_Ctra = ?,
                Inst_Ctra = ?,
                Est_BG_Ctra = ?,
                Est_S_BG_Ctra = ?,
                OBS_BG_Ctra = ?,
                Fec_Ing_Inf = ?,
                Fecha_Rec_Inf = ?,
                Ord_Cert = ?,
                Fec_Ord = ?,
                OBS_CERT = ?,
                Estado_Cert = ?,
                Monto_Ahr = ?,
                Solic_AHorro = ?,
                Fec_sol_Cobro = ?,
                Fec_Entr_Cobro = ?,
                Fec_Entrega_Ahorro = ?,
                Fec_Retiro_Ahorro = ?,
                Fec_Ing_a_Banco = ?,
                Fec_Dep_en_banco = ?,
                Pers_retiro = ?,
                JO = ?,
                Administ = ?,
                Fec_Inic_Prg = ?,
                Fec_Ter_Prg = ?,
                Fec_Inic_R = ?,
                FEC_Ter_R = ?,
                Fec_Ent_Terr = ?,
                Sup_Serviu = ?,
                ITO_Int = ?,
                EST_Obra = ?,
                Por_AVANCE = ?,
                MONTO_CTTO = ?,
                MONTO_SUBSIDIO = ?,
                MONTO_AHORRO = ?,
                Viv_SA = ?,
                VIV_ABT = ?,
                VIV_INSP = ?,
                VIV_TER = ?,
                VIV_APAGO = ?,
                VIV_EnCOBRO = ?,
                VIV_PGD = ?,
                Fec_ing_Perm = ?,
                Fec_Botadero = ?,
                Fec_Aprob = ?,
                Transporte = ?,
                T_MO = ?
            WHERE COD_CB = ?
        """

        try:
        # Ejecutar la consulta con los datos del diccionario
            cursor.execute(update_query, (
                data['COD_RUKAN'], data['NOMBRE'], data['COMUNA'], data['COD_PJ'], data['Tipo_Proy'], data['N_Llamado'], data['Año_Llamado'],
                data['F_Llamado'], data['N_Resolucion'], data['F_resolucion'], data['N_Sel'], data['N_Post'], data['N_Hab'],
                data['F_inic_Sub'], data['F_finSubs'], data['OBSERV'], data['Rut_constr'], data['N_Renun'], data['Fec_Sol_Prorr'],
                data['Res_Prorr'], data['TOTAL_AT'], data['T_Pagado_E'], data['Saldo_Eg'], data['Cobro_Eg'], data['OBS_E'],
                data['EST_cobro_Eg'], data['T_Subs_C'], data['T_Ahorro'], data['T_Pagado_C'], data['Saldo'], data['En_Cobro'],
                data['OBS_C'], data['ESTADO_cobro'], data['A_FAV_EG'], data['T_Egis'], data['M_Boleta'], data['Num_B_CF'], data['BG_CF'],
                data['FOLIO_Egis'], data['F_Venc_Egis'], data['Inst_egis'], data['Est_BG_Eg'], data['Est_S_BG_Eg'], data['OBS_BG_eg'],
                data['A_FAV_CtRa'], data['T_ctra'], data['M_Boleta_ctra'], data['N_B_CF_Ctra'], data['BG_CF_Ctra'], data['FOLIO_ctra'],
                data['F_VENC_Ctra'], data['Inst_Ctra'], data['Est_BG_Ctra'], data['Est_S_BG_Ctra'], data['OBS_BG_Ctra'], data['Fec_Ing_Inf'],
                data['Fecha_Rec_Inf'], data['Ord_Cert'], data['Fec_Ord'], data['OBS_CERT'], data['Estado_Cert'], data['Monto_Ahr'],
                data['Solic_AHorro'], data['Fec_sol_Cobro'], data['Fec_Entr_Cobro'], data['Fec_Entrega_Ahorro'], data['Fec_Retiro_Ahorro'],
                data['Fec_Ing_a_Banco'], data['Fec_Dep_en_banco'], data['Pers_retiro'], data['JO'], data['Administ'], data['Fec_Inic_Prg'],
                data['Fec_Ter_Prg'], data['Fec_Inic_R'], data['FEC_Ter_R'], data['Fec_Ent_Terr'], data['Sup_Serviu'], data['ITO_Int'],
                data['EST_Obra'], data['Por_AVANCE'], data['MONTO_CTTO'], data['MONTO_SUBSIDIO'], data['MONTO_AHORRO'], data['Viv_SA'],
                data['VIV_ABT'], data['VIV_INSP'], data['VIV_TER'], data['VIV_APAGO'], data['VIV_EnCOBRO'], data['VIV_PGD'],
                data['Fec_ing_Perm'], data['Fec_Botadero'], data['Fec_Aprob'], data['Transporte'], data['T_MO'], data['COD_CB']
            ))
            print('data') 
        # Guardar los cambios en la base de datos
            conn.commit()
            cursor.close()
            conn.close()

            return jsonify({"success": True, "message": "Datos insertados correctamente."}), 200
        except Exception as e:
            print("Error al insertar datos:", e)  # Agregar esta línea para imprimir el error en el servidor
            cursor.close()
            return jsonify({"success": False, "message": str(e)}), 500
    
    data = request.form.to_dict()
    return insertar_datos_en_bd(data)

#________________________________________________________________________________________

# ______Listado de EEPP Serviu_____

def EEPPServiuc():
    cursor = cnxn.cursor()
    # Define la consulta SQL
    query = """
    SELECT 
      EP.*, 
      EG.NOMBRE
    FROM 
      EP_Serviu EP
    LEFT JOIN 
      EstructuraGrupos EG ON EP.CODIGO_RUKAN = EG.COD_RUKAN;
    """
    
    # Ejecuta la consulta
    cursor.execute(query)
    
    # Extrae los datos
    data = cursor.fetchall()
    
    # Consigue los nombres de las columnas
    column_names = [column[0] for column in cursor.description]
    
    # Transforma los datos en una lista de diccionarios
    result = [dict(zip(column_names, row)) for row in data]
    cursor.close()
    return result


@app.route('/EEPPServiu')
@proteger_ruta
def EEPPServiu():
    cursor = cnxn.cursor()
    nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
    rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión
    EEPPServiu_data = EEPPServiuc()  # Llamada a la función que obtiene los datos
    cursor.close()
    return render_template('lista_EEPP_Serviu.html', EEPPServiu=EEPPServiu_data, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)


#________________________________________________________________________________________

#________Listado EEPP Constructora___________

def EEPPConstc():
    cursor = cnxn.cursor()
    # Define la consulta SQL
    query = """
    SELECT 
      EP.*, 
      EG.NOMBRE
    FROM 
      EP_Const EP
    LEFT JOIN 
      EstructuraGrupos EG ON EP.CODIGO_RUKAN = EG.COD_RUKAN;
    """
    
    # Ejecuta la consulta
    cursor.execute(query)
    
    # Extrae los datos
    data = cursor.fetchall()
    
    # Consigue los nombres de las columnas
    column_names = [column[0] for column in cursor.description]
    
    # Transforma los datos en una lista de diccionarios
    result = [dict(zip(column_names, row)) for row in data]
    cursor.close()
    return result


@app.route('/EEPPConst')
@proteger_ruta
def EEPPConst():
    cursor = cnxn.cursor()
    nombre_usuario = session.get('nombre', 'Desconocido')  # Obteniendo el nombre del usuario de la sesión
    rut_usuario = session.get('user', 'Desconocido')  # Obteniendo el Rut del usuario de la sesión
    EEPPConst_data = EEPPConstc()  # Llamada a la función que obtiene los datos
    cursor.close()
    return render_template('lista_EEPP_Constructora.html', EEPPConst=EEPPConst_data, nombre_usuario=nombre_usuario, rut_usuario=rut_usuario)



#________________________________________________________________________________________

@app.route('/guardado_exitoso', methods=['GET'])
@proteger_ruta
def guardado_exitoso():
    return render_template('guardado_exitosamente.html')

if __name__ == '__main__':
    app.run(debug=True)

