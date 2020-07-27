from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_mysqldb import MySQLdb
import os

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


@app.route('/Sesion',  methods=['POST'])
def Sesion():

    return render_template('InicioDeSesion.html')


@app.route('/Index')
def Index():
    return render_template('Index.html')


@app.route('/add_contact', methods=['POST'])
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

