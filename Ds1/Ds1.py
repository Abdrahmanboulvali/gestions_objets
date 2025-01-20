from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'etud_sdid'
mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM etud,departement where etud.code_dep=departement.code_dep")
    data = cur.fetchall()
    cur.close()
    return render_template('liste_etud_sdid.html', etuds=data )

@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM departement")
    data = cur.fetchall()
    cur.close()
    return render_template('index_sdid.html' , departements=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":

        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        tel = request.form['tel']
        code_dep = request.form['code_dep']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO etud (nom, prenom, email, tel, code_dep ) "
                    "VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, tel, code_dep ) )
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<matricule>', methods = ['GET'])
def delete(matricule):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM etud WHERE matricule=%s", [matricule])
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update_rec/<matricule>', methods=['GET'])
def update_rec(matricule):
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT  * FROM departement")
    departements = cur1.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM etud WHERE matricule=%s", [matricule])
    etud = cur.fetchone()
    cur.close()
    return render_template('modifier_sdid.html', etud=etud, departements=departements)

@app.route('/update/', methods=['POST'])
def update():
    if request.method == 'POST':
        matricule = request.form['matricule']
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        tel = request.form['tel']
        code_dep = request.form['Departement']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE etud
            SET nom = %s,
                prenom = %s,
                email = %s,
                tel = %s,
                code_dep = %s
            WHERE matricule = %s
        """, (nom, prenom, email, tel, code_dep, matricule))
        mysql.connection.commit()
        return redirect(url_for('Index'))

app.run(debug=True)