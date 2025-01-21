import os
import random

from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
from twilio.rest import Client
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

#this is a comment 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_objs_p_t'
UPLOAD_FOLDER = 'static/uploads'

mysql = MySQL(app)

# Configuration pour le téléchargement des fichiers
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def envoyer_otp():
    num_tel = session.get('tel')
    if not num_tel:
        return "Entrez votre numéro de téléphone SVP", 400

    if not num_tel.startswith('+'):
        num_tel = f"+222{num_tel}"

    if not num_tel[1:].isdigit():
        return "Le numéro de téléphone doit inclure l'indicatif du pays (ex: +222) et être valide", 400

    otp = random.randint(100000, 999999)
    session['otp'] = otp

    try:
        message = client.messages.create(
            body=f"Votre code de verification est : {otp}",
            from_=twilio_phone_number,
            to=num_tel
        )

        return f"Le code de verification a été envoyé avec succès: {otp}", 200
    except Exception as e:
        return f"Echec de l'envoi du code de vérification : {str(e)}", 500


@app.route('/verification_otp', methods=['POST'])
def verification_otp():
    if request.method == 'POST':
        nom = session['nome']
        prenom = session['prenome']
        tel = session['tel']
        genre = session['genre']
        password = session['password']
        code_otp = request.form['otp']

        if not code_otp or not tel:
            return "Veuillez saisir le code de vérification et le numéro de téléphone", 400
        else:
            if int(code_otp) == session['otp']:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO person_p_t (nom, prenom,genre, num_tel,mot_passe) "
                            "VALUES (%s, %s, %s, %s, %s)", (nom, prenom,genre, tel, password))
                mysql.connection.commit()
                return redirect(url_for('hom'))
            else:
                return "Code de verification invalide", 400

# Fonction pour vérifier les extensions de fichier
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
            return redirect(url_for('Index'))
        else:
            if n_tel == '37614881' and password == '23605':
                session['admin'] = '23605'
                return redirect(url_for('Indexadmin'))
            else:
                return 'Numéro du téléphone ou le mot de passe est incorret !'

@app.route('/logoutadmin')
def logoutadmin():
    session.pop('admin', None)
    return redirect(url_for('hom'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('hom'))


@app.route('/upadmin/<int:id_o>')
def upadmin(id_o):
    if 'admin' in session:
        etat = 'active'
        cur = mysql.connection.cursor()
        cur.execute("""
                UPDATE objet_p_t
                SET etat = %s
                WHERE id_o = %s
            """, (etat, id_o))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Indexadmin'))
    return redirect(url_for('hom'))

@app.route('/h', methods = ['POST', 'GET'])
def Index():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p and objet_p_t.etat = 'active' ")
        objets_p3 = cur.fetchall()
        cur.close()
        return render_template('tables.html', objets_p3=objets_p3)

    return redirect(url_for('hom'))

@app.route('/h3')
def Index3():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p and objet_p_t.etat = 'active' ")
        data = cur.fetchall()
        cur.close()
        return render_template('tables.html', objets_p=data)
    return redirect(url_for('hom'))


@app.route('/hadmin')
def Indexadmin():
    if 'admin' in session:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p")
        data = cur.fetchall()
        cur.close()
        return render_template('all_pub.html', objets_admin=data)
    return redirect(url_for('hom'))
@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM person_p_t")
    data = cur.fetchall()
    cur.close()
    return render_template('register.html' , persons=data)

@app.route('/profile')
def profile():
    if 'user_id' in session:
        id_p = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM person_p_t where id_p = %s", [id_p])
        data = cur.fetchone()
        cur.close()
        return render_template('Profile.html' , person=data)
    return redirect(url_for('hom'))


@app.route('/homee')
def homee():
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM objet_p_t")
        data = cur.fetchall()
        cur.close()
        return render_template('objet.html' , objets=data)
    return redirect(url_for('hom'))


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        # Capture form data and store it in session
        session['nome'] = request.form['nome']
        session['prenome'] = request.form['prenome']
        session['genre'] = request.form.get('gender')
        session['tel'] = request.form['tel']
        session['password'] = request.form['password']

        # Check if the phone number already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_tel FROM person_p_t WHERE num_tel = %s", [session['tel']])
        N_tel = cur.fetchone()

        if N_tel:
            return "لديك حساب بالفعل، يمكنك تسجيل الدخول"  # Account already exists
        else:
            # Call the envoyer_otp function to send OTP
            otp_response, status_code = envoyer_otp()
            return render_template('otp.html', message=otp_response)





@app.route('/inserte', methods=['POST'])
def inserte():
    if 'user_id' in session:
        global filename
        if request.method == "POST":
            type = request.form['type']
            statu = request.form['statu']
            place = request.form['place']
            destribition = request.form['destribition']
            date = request.form['date']
            etat = request.form['etat']
            id_p = session['user_id']
            file = request.files['file']
            file_path = None
            if file and file.filename != '':
                # Sécuriser le nom de fichier et l'enregistrer
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_path = f"{UPLOAD_FOLDER}/{filename}"

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO objet_p_t (type, statu, file_path, emplacement, destribition, date_p_t, id_p, etat)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (type, statu, file_path, place, destribition, date, id_p, etat))
            mysql.connection.commit()
            cur.close()

            return redirect(url_for('Index'))
        return redirect(url_for('hom'))

# Route : Mettre à jour un item
@app.route('/update/<int:id_o>', methods=['GET', 'POST'])
def update(id_o):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            type = request.form['type']
            statu = request.form['statu']
            place = request.form['place']
            destribition = request.form['destribition']
            date = request.form['date']
            file = request.files['file']
            # Gérer le téléchargement de l'image si elle est fournie
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                        UPDATE objet_p_t
                        SET type = %s,
                            statu = %s,
                            file_path = %s,
                            emplacement = %s,
                            destribition = %s,
                            date_p_t = %s
                        WHERE id_o = %s
                    """, (type, statu, image_path, place, destribition, date, id_o))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Index'))

        cur.execute(
            "SELECT id_o, type, destribition, emplacement, date_p_t, file_path, statu FROM objet_p_t WHERE id_o = %s",
            (id_o,))
        objet = cur.fetchone()
        cur.close()

        return render_template('modifier.html', objet=objet)
    return redirect(url_for('hom'))

@app.route('/updateadmin/<int:id_o>', methods=['GET', 'POST'])
def updateadmin(id_o):
    if 'admin' in session:
        cur = mysql.connection.cursor()

        if request.method == 'POST':
            type = request.form['type']
            statu = request.form['statu']
            place = request.form['place']
            destribition = request.form['destribition']
            date = request.form['date']
            file = request.files['file']
            # Gérer le téléchargement de l'image si elle est fournie
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                        UPDATE objet_p_t
                        SET type = %s,
                            statu = %s,
                            file_path = %s,
                            emplacement = %s,
                            destribition = %s,
                            date_p_t = %s
                        WHERE id_o = %s
                    """, (type, statu, image_path, place, destribition, date, id_o))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Indexadmin'))

        # Récupérer les données actuelles de l'item
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT id_o, type, destribition, emplacement, date_p_t, file_path, statu FROM objet_p_t WHERE id_o = %s",
            (id_o,))
        objet = cur.fetchone()
        cur.close()

        return render_template('modifier.html', objet=objet)

    return redirect(url_for('hom'))

# Route : Supprimer un item
@app.route('/deleteadmin/<int:id_o>', methods=['GET'])
def deleteadmin(id_o):
    if 'admin' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM objet_p_t WHERE id_o=%s", ([id_o]))
        mysql.connection.commit()
        return redirect(url_for('Indexadmin'))
    return redirect(url_for('hom'))

@app.route('/delete/<int:id_o>', methods=['GET'])
def delete(id_o):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM objet_p_t WHERE id_o=%s", ([id_o]))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    return redirect(url_for('hom'))

@app.route('/updateprofil/<int:id_p>', methods=['GET', 'POST'])
def updateprofil(id_p):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        num_tel = request.form['num_tel']
        email = request.form['email']
        adresse = request.form['adresse']
        password = request.form['password']

        cur.execute("SELECT mot_passe FROM person_p_t WHERE id_p = %s", (session['user_id'],))
        mot_passe = cur.fetchone()

        if mot_passe and mot_passe[0] == password:
            cur.execute("""
                    UPDATE person_p_t
                    SET nom = %s,
                        prenom = %s,
                        num_tel = %s
                    WHERE id_p = %s
                    """, (nom, prenom, num_tel, id_p))
            if email and adresse:
                cur.execute("""
                            UPDATE person_p_t
                            SET mail = %s,
                                adresse = %s
                            WHERE id_p = %s
                            """, (email, adresse, id_p))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('profile'))

    cur.execute("SELECT * FROM person_p_t WHERE id_p = %s", (session['user_id'],))
    person = cur.fetchone()
    cur.close()
    return render_template('modifier_profil.html', person=person)


@app.route('/charts')
def hommm():
    if 'admin' in session:
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT  COUNT(*) FROM person_p_t where genre = 'Homme'")
        data1 = cur1.fetchone()
        cur1.close()

        cur2 = mysql.connection.cursor()
        cur2.execute("SELECT  COUNT(*) FROM person_p_t where genre = 'Femme'")
        data2 = cur2.fetchone()
        cur2.close()

        cur3 = mysql.connection.cursor()
        cur3.execute("SELECT  COUNT(*) FROM objet_p_t where etat = 'active'")
        data3 = cur3.fetchone()
        cur3.close()

        cur4 = mysql.connection.cursor()
        cur4.execute("SELECT  COUNT(*) FROM objet_p_t where etat = 'inactive'")
        data4 = cur4.fetchone()
        cur4.close()

        cur7 = mysql.connection.cursor()
        cur7.execute("SELECT  COUNT(*) FROM objet_p_t where statu = 'perdu'")
        data7 = cur7.fetchone()
        cur7.close()

        cur8 = mysql.connection.cursor()
        cur8.execute("SELECT  COUNT(*) FROM objet_p_t where statu = 'trouvé'")
        data8 = cur8.fetchone()
        cur8.close()

        cur5 = mysql.connection.cursor()
        cur5.execute("SELECT  COUNT(*) FROM person_p_t")
        data5 = cur5.fetchone()
        cur5.close()

        cur6 = mysql.connection.cursor()
        cur6.execute("SELECT  COUNT(*) FROM objet_p_t")
        data6 = cur6.fetchone()
        cur6.close()


        return render_template('charts.html' , Utilisateurs=data5, Hommes=data1, Femmes=data2, objets=data6, actives=data3, inactives=data4, perdus=data7, trouvés=data8)
    return redirect(url_for('hom'))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
