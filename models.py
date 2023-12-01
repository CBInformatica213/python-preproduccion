from run import db

"1.- TABLA DATOS_PERSONAS"
class DatosPersonas(db.Model):
    __tablename__ = 'datos_personas'

    id = db.Column(db.Integer, primary_key=True)
    rut_pers = db.Column(db.String(50))
    num_perm_edif = db.Column(db.String(200))
    fec_perm_edif = db.Column(db.String(200))
    num_recep = db.Column(db.String(200))
    fec_recep1 = db.Column(db.String(200))
    fec_recep_nom = db.Column(db.String(200))
    rsh = db.Column(db.String(200))
    pers_viv = db.Column(db.SmallInteger)
    # Otros campos...

"2.- TABLA EstructuraGrupos"
class Grupos(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    encargado = db.Column(db.String(50))
    fecha_llamado = db.Column(db.String(200))
    estado = db.Column(db.String(200))
    nombre_cto = db.Column(db.String(200))
    rut_cto = db.Column(db.String(200))
    rut_pj = db.Column(db.String(200))
    cod_cb = db.Column(db.String(200))
    cod_rukan = db.Column(db.Integer)
    nom_grupo = db.Column(db.String(200))
    comuna = db.Column(db.String(200))
    tipo_proy = db.Column(db.String(200))
    num_pers = db.Column(db.SmallInteger)
    # Otros campos...

"3.- TABLA Personas"
class Personas(db.Model):
    __tablename__ = 'Personas'

    #id = db.Column(db.Integer, primary_key=True)
    RUT = db.Column(db.String(20))
    Nombre = db.Column(db.String(50))
    A_Paterno = db.Column(db.String(20))
    A_Materno = db.Column(db.String(20))
    Nacionalidad = db.Column(db.String(20))
    Sexo = db.Column(db.String(20))
    Fecha_de_Nacimiento = db.Column(db.String(20))
    Edad = db.Column(db.String(3))
    Estado_civil = db.Column(db.String(20))
    Dirección = db.Column(db.String(50))
    Piso = db.Column(db.String(10))
    Num = db.Column(db.String(20))
    Block = db.Column(db.String(20))
    Villa = db.Column(db.String(30))
    COMUNA = db.Column(db.String(30))
    Fono = db.Column(db.String(20))
    Correo = db.Column(db.String(50))
    Vigencia_cedula = db.Column(db.String(20))
    Rut_Cony = db.Column(db.String(20))
    Estado = db.Column(db.String(20))
    Fecha_Act = db.Column(db.String(20))
    N_Depto = db.Column(db.String(10))

"4.- TABLA PJ"
class PJ(db.Model):
    __tablename__ = 'PJ'

    Cod_PJ = db.Column(db.String(30), primary_key=True)
    Rol_PJ = db.Column(db.String(20))
    Rut_PJ = db.Column(db.String(20))
    Nombre_PJ = db.Column(db.String(55))
    Dirección_1 = db.Column(db.String(255))
    Numero_1 = db.Column(db.Float)
    Block_1 = db.Column(db.String(20))
    Villa_1 = db.Column(db.String(30))
    N_Depto_1 = db.Column(db.Float)
    Dirección_2 = db.Column(db.String(255))
    Numero_2 = db.Column(db.String(20))
    Block_2 = db.Column(db.String(20))
    Villa_2 = db.Column(db.String(30))
    Comuna = db.Column(db.String(30))
    Serie = db.Column(db.Float)
    Fecha = db.Column(db.String(20))
    N_Depto_2 = db.Column(db.Float)

"5.- TABLA cod_rut"
class cod_rut(db.Model):
    __tablename__ = 'cod_rut'

"6.- Dir_Serie"
class Dir_Serie(db.Model):
    __tablename__ = 'Dir_Serie'

    id = db.Column(db.Integer, primary_key=True)
    Cod_PJ = db.Column(db.String(30))
    Serie_Vigente = db.Column(db.models.FloatField)
    Rut = db.Column(db.String(20))
    Cargo = db.Column(db.String(255))
    
   
