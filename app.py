from flask import Flask, flash, redirect, render_template, url_for
from flask_bootstrap import Bootstrap #pip install Flask Bootstrap ---> BT 3
from flaskext.mysql import MySQL #pip install flask mysql
from flask_modals.modal import render_template_modal #pip install Flask-Modals
from static.admin.form import Formulario

app = Flask(__name__)
bootstrap = Bootstrap(app)  #se crea una instancia de Bootstrap
mysql = MySQL() # crea una instancia de la clase MySQL para mi Base de Datos

#Configurando la BBDD
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'db_python_crud'
app.config['MYSQL_DATABASE_Host'] = 'localhost'
app.config['SECRET_KEY'] = 'secret'
mysql.init_app(app) #con esto se vincula mi BBDD con de mi app

def connection():
    conn = mysql.connect()
    cursor = conn.cursor()
    return conn,cursor

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    conn,cursor = connection()
    cursor.execute('SELECT personas.id, nombre, apellido, ciudad, provincia FROM personas INNER JOIN locaciones WHERE personas.id_locacion = locaciones.id ORDER BY apellido')
    data = cursor.fetchall()
    conn.close()

    return render_template('display.html', db_list = data)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    formulario = Formulario()
    get_locaciones(formulario)

    if formulario.validate_on_submit():
        nom = formulario.nombre.data
        ape = formulario.apellido.data
        id_loc = formulario.locacion.data
        conn, cursor = connection()
        sql = 'INSERT INTO personas(nombre, apellido, id_locacion) VALUES (%s, %s, %s)'
        values = (nom, ape, id_loc)
        cursor.execute(sql, values)
        conn.commit()
        conn.close() 
        flash('Registro agregado con éxito')
        return redirect(url_for('display'))
    return render_template('add.html', formulario = formulario)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    formulario = Formulario()
    get_locaciones(formulario)

    if formulario.validate_on_submit():
        nom = formulario.nombre.data
        ape = formulario.apellido.data
        id_loc = formulario.locacion.data
        conn, cursor = connection()
        sql = 'UPDATE personas SET nombre = %s, apellido = %s, id_locacion = %s WHERE id = %s'
        value = (nom, ape, id_loc, id)
        cursor.execute(sql, value)
        conn.commit()
        conn.close()
        flash('Se actualizó el usuario con éxito')
        return redirect( url_for('display') )
    
    #MOSTRAR DATOS DEL REGISTRO A MODIFICAR
    conn, cursor = connection()
    sql = 'SELECT * FROM personas WHERE id = %s'
    cursor.execute(sql, id)
    data = cursor.fetchall()
    data = data[0]
    conn.close()
    formulario.nombre.data = data[1]
    formulario.apellido.data = data[2]
    formulario.locacion.data = data[3]
    return render_template('edit.html', person = data, formulario = formulario)

@app.route('/delete/<int:id>')
def delete(id):
    conn, cursor = connection()
    sql = 'DELETE FROM personas WHERE id = %s'
    cursor.execute(sql, id)
    conn.commit() #cuando realizo una modificación en la BBDD necesito hacer un commit para aplicar los cambios
    conn.close()
    flash('Registro eliminado')
    return redirect(url_for('display'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error = error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error = error)

def get_locaciones(formulario):
    locaciones = []
    conn, cursor = connection()
    cursor.execute('SELECT DISTINCT * FROM locaciones')
    locs = cursor.fetchall()
    for l in locs:
        locaciones.append(l)
    conn.close()
    
    opciones = [(l[0], l[1] + ", " + l[2]) for l in locaciones]
    opciones.sort(key = lambda x : x[1])
    formulario.locacion.choices = opciones

if __name__ == '__main__':
    app.run(debug=True)