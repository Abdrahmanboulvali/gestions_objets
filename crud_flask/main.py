from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bd_emp'
mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM employee,service where employee.service=service.id")
    data = cur.fetchall()
    cur.close()
    return render_template('liste_emp.html', emps=data )

@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM service")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html' , services=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":

        nom = request.form['nom']
        date_naiss = request.form['date_naiss']
        mail = request.form['mail']
        genre = request.form['genre']
        service = request.form['service']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee (nom, date_naiss, mail,genre,service) "
                    "VALUES (%s, %s, %s, %s, %s)", (nom, date_naiss, mail,genre,service) )
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<id_emp>', methods = ['GET'])
def delete(id_emp):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employee WHERE id_emp=%s", [id_emp])
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update_rec/<id_emp>', methods=['GET'])
def update_rec(id_emp):
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT  * FROM service")
    services = cur1.fetchall()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM employee WHERE id_emp=%s", [id_emp])
    emp = cur.fetchone()
    cur.close()
    return render_template('modifier.html', emp=emp, services=services)

@app.route('/update/', methods=['POST'])
def update():
    if request.method == 'POST':
        id_emp = request.form['id_emp']
        nom = request.form['nom']
        date_naiss = request.form['date_naiss']
        mail = request.form['mail']
        genre = request.form['genre']
        service = request.form['service']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE employee
            SET nom = %s,
                date_naiss = %s,
                mail = %s,
                genre = %s,
                service = %s
            WHERE id_emp = %s
        """, (nom, date_naiss, mail,genre,service,id_emp))
        mysql.connection.commit()
        return redirect(url_for('Index'))


app.run(debug=True)