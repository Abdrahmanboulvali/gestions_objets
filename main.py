import os
import random

from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL
from twilio.rest import Client
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

account_sid = "ACa95ab4e41f99b202e1b1f0819d9b3771"
auth_token = "0ef7113d41987ab32821a42c1e187bb4"
twilio_phone_number = "+15673443856"  # Corrected format


client = Client(account_sid, auth_token)

app.secret_key ="abderrahmane"
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

        return f"Le code de verification a été envoyé avec succès", 200
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
        email = session['email']
        adress = session['adress']

        if not code_otp or not tel:
            return "Veuillez saisir le code de vérification et le numéro de téléphone", 400
        else:
            if int(code_otp) == session['otp']:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO person_p_t (nom, prenom,genre, num_tel,mot_passe,mail, adress) "
                            "VALUES (%s, %s, %s, %s, %s, %s, %s)", (nom, prenom,genre, tel, password, email, adress))
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
        etat1 = 'active'
        etat2 = 'inactive'
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM objet_p_t where id_o = %s", (id_o,))
        etat = cur.fetchone()
        if etat[8] == etat2:
            cur.execute("""
                    UPDATE objet_p_t
                    SET etat = %s
                    WHERE id_o = %s
                """, (etat1, id_o))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Indexadmin'))
        else:
            cur.execute("""
                                UPDATE objet_p_t
                                SET etat = %s
                                WHERE id_o = %s
                            """, (etat2, id_o))
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

@app.route('/hutile')
def Indexutile():
    if 'user_id' in session:
        id_p = session['user_id']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p and objet_p_t.id_p = %s", (id_p,))
        data = cur.fetchall()
        cur.close()
        return render_template('objs_utl.html', objs_utl=data)
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
        session['email'] = request.form['email']
        session['adress'] = request.form['adress']

        # Check if the phone number already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT num_tel FROM person_p_t WHERE num_tel = %s", [session['tel']])
        N_tel = cur.fetchone()

        if N_tel:
            return "Vous avez déja une compte"  # Account already exists
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
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            file_path1 = None
            file_path2 = None
            file_path3 = None
            # Gérer le téléchargement de l'image si elle est fournie
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path1 = f"{UPLOAD_FOLDER}/{filename}"
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO objet_p_t.file_path = %s)",
                    (file_path1,))
                mysql.connection.commit()
                cur.close()
            elif file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path2 = f"{UPLOAD_FOLDER}/{filename}"
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO objet_p_t.file_path1 = %s",
                    (file_path2,))
                mysql.connection.commit()
                cur.close()
            elif file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path3 = f"{UPLOAD_FOLDER}/{filename}"
                cur = mysql.connection.cursor()
                cur.execute(
                    "INSERT INTO objet_p_t.file_path3 = (%s)",
                    (file_path3,))
                mysql.connection.commit()
                cur.close()

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO objet_p_t (type, statu, emplacement, destribition, date_p_t, id_p, etat)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (type, statu, place, destribition, date, id_p, etat))
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
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            # Gérer le téléchargement de l'image si elle est fournie
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path1 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path = %s
                            WHERE id_o = %s
                        """, (image_path1, id_o)),
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path2 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path1 = %s
                            WHERE id_o = %s
                        """, (image_path2, id_o)),
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path3 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path2 = %s
                            WHERE id_o = %s
                        """, (image_path3, id_o)),
            cur.execute("""
                        UPDATE objet_p_t
                        SET type = %s,
                            statu = %s,
                            emplacement = %s,
                            destribition = %s,
                            date_p_t = %s
                        WHERE id_o = %s
                    """, (type, statu, place, destribition, date, id_o))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Index'))

        cur.execute(
            "SELECT id_o, type, destribition, emplacement, date_p_t, file_path,file_path1, file_path2, statu FROM objet_p_t WHERE id_o = %s",
            (id_o,))
        objet = cur.fetchone()
        cur.close()

        return render_template('modifier.html', objet=objet)
    return redirect(url_for('hom'))

@app.route('/updateutl/<int:id_o>', methods=['GET', 'POST'])
def updateutl(id_o):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        if request.method == 'POST':
            type = request.form['type']
            statu = request.form['statu']
            place = request.form['place']
            destribition = request.form['destribition']
            date = request.form['date']
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            # Gérer le téléchargement de l'image si elle est fournie
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path1 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path = %s
                            WHERE id_o = %s
                        """, (image_path1, id_o)),
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path2 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path1 = %s
                            WHERE id_o = %s
                        """, (image_path2, id_o)),
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path3 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                            UPDATE objet_p_t
                            SET file_path2 = %s
                            WHERE id_o = %s
                        """, (image_path3, id_o)),
            cur.execute("""
                        UPDATE objet_p_t
                        SET type = %s,
                            statu = %s,
                            emplacement = %s,
                            destribition = %s,
                            date_p_t = %s
                        WHERE id_o = %s
                    """, (type, statu, place, destribition, date, id_o))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Indexutile'))

        cur.execute(
            "SELECT id_o, type, destribition, emplacement, date_p_t, file_path, file_path1, file_path2, statu FROM objet_p_t WHERE id_o = %s",
            (id_o,))
        objet = cur.fetchone()
        cur.close()

        return render_template('modifier_utl.html', objet=objet)
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
            file1 = request.files['file1']
            file2 = request.files['file2']
            file3 = request.files['file3']
            # Gérer le téléchargement de l'image si elle est fournie
            if file1 and allowed_file(file1.filename):
                filename = secure_filename(file1.filename)
                file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path1 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                        UPDATE objet_p_t
                        SET file_path = %s
                        WHERE id_o = %s
                    """, (image_path1, id_o)),
            if file2 and allowed_file(file2.filename):
                filename = secure_filename(file2.filename)
                file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path2 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                        UPDATE objet_p_t
                        SET file_path1 = %s
                        WHERE id_o = %s
                    """, (image_path2, id_o)),
            if file3 and allowed_file(file3.filename):
                filename = secure_filename(file3.filename)
                file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path3 = f"{UPLOAD_FOLDER}/{filename}"
                # Mettre à jour avec une nouvelle image
                cur.execute("""
                        UPDATE objet_p_t
                        SET file_path2 = %s
                        WHERE id_o = %s
                    """, (image_path3, id_o)),
            cur.execute("""
                        UPDATE objet_p_t
                        SET type = %s,
                            statu = %s,
                            emplacement = %s,
                            destribition = %s,
                            date_p_t = %s
                        WHERE id_o = %s
                    """, (type, statu, place, destribition, date, id_o))

            mysql.connection.commit()
            cur.close()
            return redirect(url_for('Indexadmin'))

        # Récupérer les données actuelles de l'item
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM objet_p_t WHERE id_o = %s",
            (id_o,))
        objetadmin = cur.fetchone()
        cur.close()

        return render_template('modifier_admin.html', objetadmin=objetadmin)

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

@app.route('/deleteutl/<int:id_o>', methods=['GET'])
def deleteutl(id_o):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM objet_p_t WHERE id_o=%s", ([id_o]))
        mysql.connection.commit()
        return redirect(url_for('Indexutile'))
    return redirect(url_for('hom'))


@app.route('/updateprofil/<int:id_p>', methods=['GET', 'POST'])
def updateprofil(id_p):
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        message = None

        if request.method == 'POST':
            nom = request.form['nom']
            prenom = request.form['prenom']
            num_tel = request.form['num_tel']
            email = request.form['email']
            adresse = request.form['adresse']
            password = request.form['password']

            cur.execute("SELECT * FROM person_p_t WHERE id_p = %s", [id_p])
            person = cur.fetchone()

            if person and password and password == person[4]:
                cur.execute("""
                        UPDATE person_p_t
                        SET nom = %s,
                            prenom = %s,
                            num_tel = %s,
                            mail = %s,
                            adress = %s
                        WHERE id_p = %s
                    """, (nom, prenom, num_tel, email, adresse, id_p))

                mysql.connection.commit()
                cur.close()
                return redirect(url_for('profile'))
            else:
                message = "Mot de passe incorrect !"

        cur.execute("SELECT * FROM person_p_t WHERE id_p = %s", (id_p,))
        person = cur.fetchone()
        cur.close()

        return render_template('modifier_profil.html', person=person, message=message)
    return redirect(url_for('hom'))


@app.route('/change-password/<int:id_p>', methods=['GET', 'POST'])
def change_password(id_p):
    if 'user_id' in session:
        if request.method == 'POST':
            current_password = request.form['currentPassword']
            new_password = request.form['newPassword']
            confirm_new_password = request.form['confirmNewPassword']

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM person_p_t WHERE id_p = %s", ([id_p]))
            person = cur.fetchone()

            if person and person[4] == current_password:
                if new_password == confirm_new_password:
                    cur.execute("UPDATE person_p_t SET mot_passe = %s WHERE id_p = %s", (new_password, id_p))
                    mysql.connection.commit()
                    cur.close()
                    return redirect(url_for('hom'))
                else:
                    message = "كلمة المرور الجديدة لا تطابق التأكيد!"
            else:
                message = "كلمة المرور الحالية غير صحيحة!"
            cur.close()
        else:
            message = None

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM person_p_t WHERE id_p = %s", (id_p,))
        person = cur.fetchone()
        cur.close()

        return render_template('change_password.html', person=person, message=message)

    return redirect(url_for('hom'))


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
