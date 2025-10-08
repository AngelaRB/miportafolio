from flask import Flask, render_template, request, redirect, url_for, session
from consultas import insertar,consulta,consulta_unica
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__),'static','uploads')
UPLOAD_FOLDER='static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def nombre_imagen(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() 
        

@app.route('/') # habilidades con base de datos
def inicio():
    query = "SELECT * FROM habilidades"
    habilidadesbd = consulta(query)
    
    return render_template('index.html', index=True, habilidades=habilidadesbd)



@app.route('/actualizar_habilidades/<int:id>', methods=['POST', 'GET'])
def editar_hab(id):
    if request.method == 'POST':
        habilidad = request.form.get('habilidad')
        descripcion = request.form.get('descripcion')
        icono = request.form.get('icono')
        
        query = 'UPDATE habilidades SET habilidad = %s, descripcion = %s, icono = %s WHERE id = %s'
        
        parametros = (habilidad,descripcion,icono,id)
        
        habilidadesbd = insertar(query,parametros)
    
        return redirect(url_for('inicio'))

    query = 'SELECT * FROM habilidades WHERE id = %s'
    habilidadesbd = consulta_unica(query, (id,))
    return render_template('editar_habilidades.html', habilidad=habilidadesbd)

@app.route('/actualizar_habilidades_foto/<int:id>', methods=['POST', 'GET'])
def editar_hab_foto(id):
    if request.method == 'POST':
        icono = request.files['icono']
        
        if icono and icono.filename.endswith('.svg'):
            filename = secure_filename(icono.filename)
            icono.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            query = "UPDATE habilidades SET icono = %s WHERE id = %s"
            parametros=(filename,id)

            icono = insertar(query, parametros)
    
            return redirect(url_for("inicio")) 

    # Si es GET, traemos la imagen actual
    query = "SELECT id, icono FROM habilidades WHERE id = %s"
    icono = consulta_unica(query,(id,))
    
    return render_template("editar_habilidades_foto.html", habilidad=icono)

@app.route('/eliminar_hab/<int:id>', methods=['POST', 'GET'])
def eliminar_hab(id):
    query = 'DELETE FROM habilidades WHERE id = %s'
    parametros = (id,)
        
    habilidadesbd = insertar(query,parametros)
    
    return redirect(url_for('inicio'))

@app.route('/eliminar_pro/<int:id>', methods=['POST', 'GET'])
def eliminar_pro(id):
    query = 'DELETE FROM proyectos WHERE id = %s'
    parametros = (id,)
        
    projects = insertar(query,parametros)
    
    return redirect(url_for('proyectos'))

@app.route('/eliminar_datos_contacto/<int:id>', methods=['POST', 'GET'])
def eliminar_datoscon(id):
    query = 'DELETE FROM mensajes WHERE id = %s'
    parametros = (id,)
    
    mensajes = insertar(query,parametros)
    
    return redirect(url_for('tabla_contactos'))

@app.route('/eliminar_datos_footer/<int:id>', methods=['POST', 'GET'])
def eliminar_datosfot(id):
    query = 'DELETE FROM form_footer WHERE id = %s'
    parametros = (id,)
    
    mensajes = insertar(query,parametros)
    
    return redirect(url_for('tabla_footer'))

@app.route('/proyectos') # proyectos con base de datos
def proyectos():
    query = "SELECT * FROM proyectos"
    projects = consulta(query)
    return render_template("proyectos.html", proyectos=projects)

@app.route('/actualizar_proyectos/<int:id>', methods=['POST', 'GET'])
def editar_pro(id):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion') 
        imagen = request.form.get('imagen')
        link_git = request.form.get('link_git')
        link_proyecto = request.form.get('link_proyecto')
        
        query = 'UPDATE proyectos SET nombre = %s, descripcion = %s, imagen = %s, link_git = %s, link_proyecto = %s WHERE id = %s'
        
        parametros = (nombre, descripcion, imagen, link_git, link_proyecto, id)
        
        projects = insertar(query,parametros)
        
        return redirect(url_for('proyectos'))
    
    query = 'SELECT * FROM proyectos WHERE id = %s'
    projects = consulta_unica(query, (id,))   
    
    return render_template('editar_proyecto.html', proyecto=projects)


@app.route('/actualizar_proyecto_foto/<int:id>', methods=['POST', 'GET'])
def editar_pro_foto(id):
    if request.method == 'POST':
        imagen = request.files['imagen']
        
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            query = "UPDATE proyectos SET imagen= %s WHERE id = %s"
            parametros=(filename,id)

            projects = insertar(query, parametros)
    
            return redirect(url_for("proyectos")) 

    # Si es GET, traemos la imagen actual
    query = "SELECT id, imagen FROM proyectos WHERE id = %s"
    projects = consulta_unica(query,(id,))
    
    return render_template("editar_proyecto_foto.html", proyecto=projects)


@app.route('/acerca')
def nosotros():
    query = 'SELECT cargo,biografia,profesional,hobbies, foto from sobremi'
    me = consulta(query)
    return render_template("acerca.html", acerca=True, yo=me)

@app.route('/actualizar_sobremi', methods=['POST', 'GET'])
def editar_sobremi():
    if request.method == 'POST':
        cargo = request.form.get('cargo')
        biografia = request.form.get('biografia')
        profesional = request.form.get('profesional')
        hobbies = request.form.get('hobbies')
        
        query = 'UPDATE sobremi SET cargo = %s, biografia = %s, profesional = %s, hobbies = %s WHERE id = 1'
        parametros = (cargo,biografia,profesional,hobbies)
        sobremi = insertar(query,parametros)
        return redirect(url_for('nosotros'))
    
    query = 'SELECT * FROM sobremi WHERE id = 1'
    sobremi = consulta_unica(query)
    return render_template('editar_sobremi.html', mi=sobremi)
        

@app.route('/actualizar_foto', methods=['POST', 'GET'])
def editar_foto():
    if request.method == 'POST':
        imagen = request.files['imagen']
        
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            query = "UPDATE sobremi SET foto = %s"
            parametros=(filename,)

            insertar(query, parametros)
            return redirect(url_for("nosotros")) 

    # Si es GET, traemos la imagen actual
    imagen = consulta_unica("SELECT foto FROM sobremi WHERE id = 1")
    return render_template("editar_foto.html")

@app.route("/", methods=["GET", "POST"])
def form_wp():
    correo = request.form.get('correo')
    nombre = request.form.get('nombre')
    
    query = 'INSERT INTO form_footer (nombre,correo) VALUES(%s,%s)'
    parametros = (nombre,correo)
    footer = insertar(query,parametros)
    
    
    return redirect(url_for('tabla_footer'))

@app.route('/contacto')
def contacto():
    return render_template("contacto.html", contacto=True)

@app.route('/contactar', methods=['POST'])
def procesar_contacto():
    nombre = request.form.get('nombre')
    celular = request.form.get('celular')
    correo = request.form.get('correo')
    mensaje = request.form.get('mensaje')
    query = ("INSERT INTO mensajes (nombre, celular, correo, mensaje) VALUES(%s,%s,%s,%s)")
    parametros = (nombre,celular,correo,mensaje)
    respuesta = insertar(query,parametros)
    print(respuesta)
    
    return redirect(url_for('tabla_contactos'))

@app.route('/tabla_contactos')
def tabla_contactos():
    query = 'SELECT * FROM mensajes'
    mensajes = consulta(query)
    return render_template('db_contacto.html', mensajes=mensajes)

@app.route('/tabla_footer')
def tabla_footer():
    query = 'SELECT * FROM form_footer'
    footer = consulta(query)
    return render_template('db_footer.html', footer=footer)

@app.route('/panel')
def panel():
    return render_template('panel.html')  

@app.route('/ingresar_proyectos', methods=['POST', 'GET'])
def ingresar_proyectos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        link_git = request.form.get('link_git')
        link_proyecto = request.form.get('link_proyecto')
        imagen = request.files['imagen']
        
        if imagen and imagen.filename != "":
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        query = ("INSERT INTO proyectos (nombre, descripcion, imagen, link_git, link_proyecto) VALUES(%s,%s,%s,%s,%s)")
        parametros = (nombre,descripcion,filename,link_git,link_proyecto)
        
        projects = insertar(query,parametros)
        
        return redirect(url_for('proyectos'))
    
    return render_template('ingresar_proyectos.html')


@app.route('/ingresar_habilidades', methods=['GET', 'POST'])
def ingresar_habilidades():
    if request.method == 'POST':
        habilidad = request.form.get('habilidad')
        descripcion = request.form.get('descripcion')
        icono = request.files['icono']
        
        
        if icono and icono.filename.endswith('.svg'):
            filename = secure_filename(icono.filename)
            icono.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        query = ('INSERT INTO habilidades (habilidad,descripcion,icono) VALUES(%s,%s,%s)')
        parametros = (habilidad,descripcion,filename)
        habilidadesbd = insertar(query,parametros)
        
        return redirect(url_for('inicio'))
    
    return render_template('ingresar_habilidades.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    mensaje = ''
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        query = 'SELECT * FROM usuarios WHERE usuario = %s and password = %s'
        parametros = (usuario,password)
        user = consulta_unica(query,parametros)
        
        if usuario == 'angela' and password == "bb00":
            session['usuario'] = user['id']
            session['usuario'] = user['usuario']
            return redirect(url_for('panel'))
        else:
            mensaje = 'Usuario o contraseña incorrectos'
            return render_template('login.html', mensaje=mensaje,login=login)
    
    return render_template('login.html', login=True)

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("inicio"))

app.run(debug=True)