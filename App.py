# app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flaskext.mysql import MySQL 
import pymysql
import re

app = Flask(__name__, template_folder='templates')


app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# configuracion para la conexion a msql
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'registro'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def home1():
    return render_template('Pagina_principal.html')


# http://localhost:5000/pythonlogin/ - esta es la pagina para iniciar sesion


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login2():

 # conexion a msql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es el login
    msg = ''

    if request.method == 'POST' and 'Email' in request.form and 'Contraseña' in request.form:

        Email = request.form['Email']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos2 WHERE Email = %s AND Contraseña = %s', (Email, Contraseña))

        datos2 = cursor.fetchone()

    if request.method == 'POST' and 'Email' in request.form and 'Contraseña' in request.form:

        Email = request.form['Email']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos WHERE Email = %s AND Contraseña = %s', (Email, Contraseña))

        datos = cursor.fetchone()

    # If si la cuenta exisite, te manda a home, que es la pagina que veria el usuario al ingresar, en la misma estan los datos de su cuenta
        if datos2:

            session['loggedin'] = True
            session['id'] = datos2['id']
            session['Email'] = datos2['Email']

            return redirect(url_for('profile22'))
        else:
            # esto es un mensaje por si la cagas y escribiste mal
            msg = 'Usuario o contraseña'

        if datos:

            session['loggedin'] = True
            session['id'] = datos['id']
            session['Email'] = datos['Email']

            return redirect(url_for('profile11'))
        else:
            # esto es un mensaje por si la cagas y escribiste mal
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


# http://localhost:5000/register - Esto es el registro a la pagina


@app.route('/register', methods=['GET', 'POST'])
def register():
 # Conexion a mysql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es la conexion a mysql para el registro
    msg = ''

    if request.method == 'POST' and 'Nombre' in request.form and 'Contraseña' in request.form and 'Email' in request.form:

        Nombre = request.form['Nombre']
        Email = request.form['Email']
        Contraseña = request.form['Contraseña']
        ConfirmarContraseña = request.form['ConfirmarContraseña']

        cursor.execute('SELECT * FROM datos WHERE Nombre = %s', (Nombre))
        account = cursor.fetchone()
        # esto es por si la cuenta que queres registrar ya existe
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Email incorrecto!'
        elif not re.match(r'[A-Za-z0-9]+', Nombre):
            msg = 'El nombre solo debe contener caracteres y numeros!'
        elif not Nombre or not Contraseña or not Email:
            msg = 'Por favor llene el formulario!'

        else:
            # ahora si la cuenta no existe te deja registrar por este codigo
            cursor.execute('INSERT INTO datos VALUES (NULL, %s, %s, %s, %s)',
                           (Nombre, Email, Contraseña, ConfirmarContraseña))
            conn.commit()

            msg = 'Has sido registrado con exito, ahora solo debes iniciar sesion!'
            return render_template('index.html')
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


################################################################################

@app.route('/register2', methods=['GET', 'POST'])
def register2():
 # Conexion a mysql
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # esto es la conexion a mysql para el registro

    if request.method == 'POST' and 'Nombredellocal' in request.form and 'Direccion' in request.form and 'Email' in request.form and 'Contraseña' in request.form:

        Nombredellocal = request.form['Nombredellocal']
        Direccion = request.form['Direccion']
        Email = request.form['Email']
        Contraseña = request.form['Contraseña']

        cursor.execute(
            'SELECT * FROM datos2 WHERE Nombredellocal = %s', (Nombredellocal))
        account = cursor.fetchone()
        # esto es por si la cuenta que queres registrar ya existe
        if account:
            msg = 'La cuenta ya existe!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = 'Email incorrecto!'
        elif not re.match(r'[A-Za-z0-9]+', Nombredellocal):
            msg = 'El nombre solo debe contener caracteres y numeros!'
        elif not Nombredellocal or not Contraseña or not Email:
            msg = 'Por favor llene el formulario!'

        else:
            # ahora si la cuenta no existe te deja registrar por este codigo
            cursor.execute('INSERT INTO datos2 VALUES (NULL, %s, %s, %s, %s)',
                           (Nombredellocal, Direccion, Email, Contraseña))
            conn.commit()

            msg = 'Has sido registrado con exito, ahora solo debes iniciar sesion!'
            return render_template('index.html')
    elif request.method == 'POST':

        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)


# http://localhost:5000/home - Esta es la pagina a la que accede el usuario al ingresar es home.html, es solo una interfaz para tener un recibimiento y de ahi podes elejir que hacer


@app.route('/home')
def home():

    if 'loggedin' in session:

        return render_template('home.html', Email=session['Email'])

    if 'loggedin' in session:

        return render_template('home.html', Correo=session['Correo'])

    return redirect(url_for('login'))

# http://localhost:5000/logout - esta es la pagina para salir de la sesion


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('Nombre', None)
    # Redirect to login page
    return redirect(url_for('login2'))

# http://localhost:5000/profile - aca van a estar todas las caracteristicas de la cuenta


@app.route('/profile11')
def profile11():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM datos WHERE id = %s', [session['id']])
        datos = cursor.fetchone()

        return render_template('profile1.html', datos=datos)
    # esto es por is el usuario nopuede ingresar, lo redirecciona
    return redirect(url_for('login2'))

# http://localhost:5000/profile - aca van a estar todas las caracteristicas de la cuenta


@app.route('/profile22')
def profile22():

    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if 'loggedin' in session:

        cursor.execute('SELECT * FROM datos2 WHERE id = %s', [session['id']])
        datos2 = cursor.fetchone()

        return render_template('profile2.html', datos2=datos2)
    # esto es por is el usuario nopuede ingresar, lo redirecciona
    return redirect(url_for('login2'))


@app.route('/inventario')
def inventario():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM inventario')
    data = cursor.fetchall()
    cursor.close()
    return render_template('inventario.html', contacts = data)


@app.route('/add_producto', methods=['POST'])
def add_producto():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST' and 'Producto' in request.form and 'Marca' in request.form and 'Cantidad' in request.form and 'Precio' in request.form:

        Producto = request.form['Producto']
        Marca = request.form['Marca']
        Cantidad = request.form['Cantidad']
        Precio = request.form['Precio']

        cursor.execute('INSERT INTO inventario (Producto, Marca, Cantidad, Precio) VALUES (%s, %s, %s, %s)',
                       (Producto, Marca, Cantidad, Precio))
        conn.commit()
        flash('Producto agregado con exito')
        return redirect(url_for('inventario'))


if __name__ == '__main__':
    app.run(debug=True)
