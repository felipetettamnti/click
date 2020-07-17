from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config ['MYSQL_HOST'] = 'localhost'
app.config ['MYSQL_USER'] = 'root'
app.config ['MYSQL_PASSWORD'] = ''
app.config ['MYSQL_DB'] = 'registro'
mysql = MySQL(app)


# setting 
app.secret_key = 'mysecretkey'


@app.route('/')
def Index():
    return render_template('Index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
     Nombre = request.form ['Nombre']
     Email = request.form ['Email']
     Contraseña = request.form ['Contraseña']
     ConfirmarContraseña = request.form ['ConfirmarContraseña']
     cur = mysql.connection.cursor()
     cur.execute('INSERT INTO datos(Nombre, Email, Contraseña, ConfirmarContraseña) VALUES (%s, %s, %s, %s)', 
     (Nombre,Email,Contraseña,ConfirmarContraseña))
     mysql.connection.commit()
     flash('Contact Added successfully')
     
     return redirect(url_for('Index'))
    
    

@app.route('/edit' )
def edit_contact():
    return 'edit contact'

@app.route('/delete')
def delete_contact():
    return 'delete contact'

if __name__  ==  '__main__':
    app.run(port = 3000, debug = True)

