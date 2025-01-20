from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory
from flask_mysqldb import MySQL
import os

from werkzeug.http import parse_if_range_header
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "abderrahmane"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_objs_p_t'
UPLOADS_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = 'static/uploads'
mysql = MySQL(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/H')
def homm():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t ")
    data = cur.fetchall()
    cur.close()
    return render_template('pages.html' , persons_ps=data)

@app.route('/')
def hom():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t ")
    data = cur.fetchall()
    cur.close()
    return render_template('login1.html' , persons_p=data)

@app.route('/charts')
def hommm():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t ")
    data = cur.fetchall()
    cur.close()
    return render_template('charts.html' , persons_pss=data)

@app.route('/inserteee', methods = ['POST'])
def inserteee():
    if request.method == "POST":

        n_tel = request.form['tel']
        password = request.form['password']
        cur = mysql.connection.cursor()
        verify = "SELECT * FROM person_p_t WHERE num_tel = %s and mot_passe = %s"
        cur.execute(verify, (n_tel, password))
        result = cur.fetchone()
        cur.close()
        if result:
            session['user_id'] = result[0]
            return redirect(url_for('homm'))
        else:
            return 'رقم الهاتف أو كلمة المرور غير صحيحة، رجاءا أعد المحاولة'



@app.route('/h')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p and objet_p_t.etat = 'active' ")
    data = cur.fetchall()
    cur.close()
    return render_template('tables.html', objets_p=data )

@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t")
    data = cur.fetchall()
    cur.close()
    return render_template('register.html' , persons=data)
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
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_tel FROM person_p_t WHERE num_tel = %s", [tel])
        N_tel = cur.fetchone()
        if N_tel:
            return "لديك حساب بالفعل، يمكنك تسجيل الدخول"
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO person_p_t (nom, prenom, num_tel,mode_passe) "
                        "VALUES (%s, %s, %s, %s, %s)", (nom, prenom, tel, password))
            mysql.connection.commit()
            return redirect(url_for('hom'))




@app.route('/inserte', methods=['POST'])
def inserte():
    global filename
    if request.method == "POST":
        type = request.form['type']
        statu = request.form['statu']
        place = request.form['place']
        destribition = request.form['destribition']
        date = request.form['date']
        id_p = session['user_id']
        file = request.files['file']
        etat = request.form['etat']
        file_path = None
        if file and file.filename != '':
            # Sécuriser le nom de fichier et l'enregistrer
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = f"{UPLOADS_FOLDER}/{filename}"

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO objet_p_t (type, statu, file_path, emplacement, destribition, date_p_t, id_p, etat)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (type, statu, file_path, place, destribition, date, id_p, etat))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('Index'))

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/delete/<id_o>', methods = ['GET'])
def delete(id_o):
    id_p = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_p FROM objet_p_t WHERE id_o=%s", ([id_o]))
    result = cur.fetchone()
    if result[0] != id_p:
        return "Vous n'avez pas le droit de suprimer cet article"
    else:
        cur.execute("DELETE FROM objet_p_t WHERE id_o=%s", ([id_o]))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update_rec/<id_o>', methods=['GET'])
def update_rec(id_o):
    id_p = session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_p FROM objet_p_t WHERE id_o=%s", ([id_o]))
    result = cur.fetchone()
    if result[0] != id_p:
        return "Vous n'avez pas le droit de modifier cet article"
    else:
        cur.execute("SELECT  * FROM objet_p_t WHERE id_o=%s", [id_o])
        objet = cur.fetchone()
        cur.close()
    return render_template('modifier.html', objet=objet)

@app.route('/update/', methods=['POST'])
def update():
    if request.method == 'POST':
        id_o = request.form["id_o"]
        type = request.form['type']
        statu = request.form['statu']
        file = request.files['file']
        place = request.form['place']
        destribition = request.form['destribition']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE objet_p_t
                    SET type = %s,
                        statu = %s,
                        file_path = %s,
                        emplacement = %s,
                        destribition = %s,
                        date_p_t = %s
                    WHERE id_o = %s
                """, (type, statu, file, place, destribition, date, id_o))
        mysql.connection.commit()
        return redirect(url_for('Index'))


app.run(debug=True)