from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_mysqldb import MySQL
import pymysql


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registro'
mysql = MySQL(app)


# setting
app.secret_key = 'mysecretkey'


@app.route('/')
def home():
    return render_template('texto.html')



@app.route('/Sesion')
def login():
    return render_template('InicioDeSesion.html')


@app.route('/Sesion', methods=['POST', 'GET'])
def Authenticate():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'Email' in request.form and 'Contraseña' in request.form:
        # Create variables for easy access
        username = request.form['Email']
        password = request.form['Contraseña']
        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM datos WHERE Email = %s AND Contraseña = %s', (Email, Contraseña))
        # Fetch one record and return result
        datos = cursor.fetchone()

        if datos:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = datos['id']
            session['Email'] = datos['Email']
            # Redirect to home page
            # return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)


@app.route('/add_contact')
def Index():
    return render_template('Index.html')

# Esto es el registro


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Email = request.form['Email']
        Contraseña = request.form['Contraseña']
        ConfirmarContraseña = request.form['ConfirmarContraseña']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO datos(Nombre, Email, Contraseña, ConfirmarContraseña) VALUES (%s, %s, %s, %s)',
                    (Nombre, Email, Contraseña, ConfirmarContraseña))
        mysql.connection.commit()
        return render_template('Gracias.html')

# Registro de los locales


@app.route('/add_contact2', methods=['POST'])
def add_contact2():
    if request.method == 'POST':
        Nombredellocal = request.form['Nombredellocal']
        Direccion = request.form['Direccion']
        Correo = request.form['Correo']
        Contraseña = request.form['Contraseña']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO datos2(Nombredellocal, Direccion, Correo, Contraseña) VALUES (%s, %s, %s, %s)",
                    (Nombredellocal, Direccion, Correo, Contraseña))
        mysql.connection.commit()
        return render_template('texto.html')


@app.route('/edit')
def edit_contact():
    return 'edit contact'


@app.route('/delete')
def delete_contact():
    return 'delete contact'


if __name__ == '__main__':
    app.run(port=3000, debug=True)
