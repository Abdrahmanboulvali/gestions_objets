from tkinter.constants import INSERT

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_objs_p_t'
mysql = MySQL(app)

@app.route('/')
def hom():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t ")
    data = cur.fetchall()
    cur.close()
    return render_template('login.html' , persons_p=data)

@app.route('/inserteee', methods = ['POST'])
def inserteee():
    if request.method == "POST":

        n_tel = request.form['tel']
        password = request.form['password']
        cur = mysql.connection.cursor()
        verify = "SELECT * FROM person_p_t WHERE person_p_t.num_tel = %s and person_p_t.mode_passe = %s"
        cur.execute(verify, (n_tel, password))
        result = cur.fetchall()
        cur.close()
        if result:
            return redirect(url_for('Index'))
        else:

            return redirect(url_for('hom'))

@app.route('/h')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p")
    data = cur.fetchall()
    cur.close()
    return render_template('list_objets.html', objets_p=data )

@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t")
    data = cur.fetchall()
    cur.close()
    return render_template('sign.html' , persons=data)
@app.route('/homee')
def homee():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM objet_p_t")
    data = cur.fetchall()
    cur.close()
    return render_template('objet.html' , objets=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":

        nom = request.form['nome']
        prenom = request.form['prenome']
        tel = request.form['tel']
        password = request.form['password']
        session
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO person_p_t (nom, prenom, num_tel,mode_passe) "
                    "VALUES (%s, %s, %s, %s)", (nom, prenom, tel,password))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/inserte', methods = ['POST'])
def inserte():
    if request.method == "POST":

        type = request.form['type']
        statu = request.form['statu']
        photo = request.form['photo']
        place = request.form['place']
        destribition = request.form['destribition']
        date =request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO objet_p_t (type, statu,photo,emplacement,destribition,date_p_t)"
                    "VALUES (%s, %s, %s, %s, %s, %s)", (type, statu,photo,place,destribition,date))
        mysql.connection.commit()
        return redirect(url_for('Index'))

app.run(debug=True)