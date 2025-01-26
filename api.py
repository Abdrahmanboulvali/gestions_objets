import base64
import os
import uuid

from flask import Flask, request, jsonify, url_for, session
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis des origines externes (nécessaire pour Flutter)

# Configuration de la base de données
app.secret_key = "abderrahmane"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_objs_p_t'

# Configuration pour le dossier d'upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

# Fonction pour vérifier si un fichier est autorisé
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Api : Obtenir tous les items
@app.route('/api/objet_p_t', methods=['GET'])
def get_objets():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM objet_p_t, person_p_t where person_p_t.id_p=objet_p_t.id_p")
    objects = cur.fetchall()
    cur.close()

    results = [
        {
            'id_o': row[0],
            'type': row[1],
            'statu': row[2],
            'destribition': row[5],
            'emplacement': row[3],
            'date': row[4],
            'nom': row[12],
            'prenome': row[13],
            'id_p': row[6],
            'etat':row[8],
            'num_tel': row[14],
            'image1': url_for('static', filename=row[7].replace('static/', ''), _external=True) if row[7] else None,
            'image2': url_for('static', filename=row[9].replace('static/', ''), _external=True) if row[9] else None,
            'image3': url_for('static', filename=row[10].replace('static/', ''), _external=True) if row[10] else None
        }
        for row in objects
    ]

    return jsonify(results)

@app.route('/api/login', methods = ['POST'])
def inserteee():
    try:
        data2 = request.get_json()
        if not data2 or 'num_tel' not in data2 or 'mot_passe' not in data2:
            return jsonify({'error': 'Champs obligatoires manquants'}), 400
        else:
            n_tel = data2['num_tel']
            password = data2['mot_passe']
            cur = mysql.connection.cursor()
            verify = "SELECT * FROM person_p_t WHERE num_tel = %s and mot_passe = %s"
            cur.execute(verify, (n_tel, password))
            result = cur.fetchone()
            cur.close()
            if result:
                return jsonify(result), 201
            else:
                if n_tel == "37614881" and password == "23605":
                    return '', 200
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500

# Api : Créer un nouvel item avec une image
@app.route('/api/create', methods=['POST'])
def api_create():
    try:
        # Vérifier si tous les champs requis sont présents
        data = request.get_json()
        if not data or 'statu' not in data or 'destribition' not in data or 'image' not in data:
            return jsonify({'error': 'Champs obligatoires manquants'}), 400

        type = data['type']
        statu = data['statu']
        destribition = data['destribition']
        emplacement = data['emplacement']
        date = data['date']
        etat = data['etat']
        id_p = data['identifiant']
        image_base64 = data['image']

        # Décoder l'image Base64

        try:
            image_data = base64.b64decode(image_base64)
        except Exception as e:
            return jsonify({'error': 'Image invalide ou non décodable'}), 400

        # Vérifier si le dossier d'upload existe, sinon le créer
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Générer un nom de fichier unique pour l'image
        unique_filename = f"{uuid.uuid4().hex}.jpg"  # Par défaut, l'image est enregistrée au format JPG
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename).replace("\\", "/")

        # Enregistrer l'image
        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)

        # Chemin relatif pour la base de données
        relative_image_path = os.path.join('uploads', unique_filename).replace("\\", "/")

        # Insérer les données dans la base
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO objet_p_t (type, statu, file_path, emplacement, destribition, date_p_t, id_p, etat)"
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (type, statu, relative_image_path, emplacement, destribition, date, id_p, etat)
        )
        mysql.connection.commit()
        return '', 201

    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500

# Api : Mettre à jour un item
@app.route('/api/update/<int:id_o>', methods=['PUT'])
def update_objet(id_o):
    global relative_image_path
    try:
        # Lire les données JSON envoyées par le client
        data4 = request.get_json()

        # Vérifier si les champs requis sont présents
        if not data4 or 'statu' not in data4 or 'destribition' not in data4:
            return jsonify({'error': 'Champs obligatoires manquants'}), 400

        type = data4['type']
        statu = data4['statu']
        destribition = data4['destribition']
        emplacement = data4['emplacement']
        date = data4['date']
        image_path = None

        # Gérer l'image encodée en Base64 si présente
        if 'image' in data4:
            try:
                # Décoder l'image Base64
                image_data = base64.b64decode(data4['image'])
                unique_filename = f"{uuid.uuid4().hex}.jpg"  # Nom unique avec extension JPG
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename).replace("\\", "/")

                # Enregistrer l'image
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])

                with open(image_path, 'wb') as image_file:
                    image_file.write(image_data)

                # Chemin relatif pour la base de données
                relative_image_path = os.path.join('uploads', unique_filename).replace("\\", "/")
            except Exception as e:
                return jsonify({'error': 'Erreur lors du traitement de l\'image'}), 400

        # Mise à jour dans la base de données
        cur = mysql.connection.cursor()
        if image_path:
            cur.execute("""
                    UPDATE objet_p_t
                    SET file_path = %s
                    WHERE id_o = %s
                """, (relative_image_path, id_o)
            )
        cur.execute("""
                            UPDATE objet_p_t
                            SET type = %s,
                                statu = %s,
                                emplacement = %s,
                                destribition = %s,
                                date_p_t = %s
                            WHERE id_o = %s
                        """, (type, statu, emplacement, destribition, date, id_o)
                    )
        mysql.connection.commit()

        return '', 200

    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500




# API : Supprimer un item
@app.route('/api/delete/<int:id_o>', methods=['DELETE'])
def api_delete(id_o):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM objet_p_t WHERE id_o = %s", (id_o,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'objet deleted successfully'}), 200
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/create_account', methods = ['POST'])
def insert():
    try:
        data1 = request.get_json()
        print(data1)
        if not data1 or 'nom' not in data1 or 'prenom' not in data1 or 'num_tel' not in data1 or 'mot_passe' not in data1 :
            return jsonify({'error': 'Champs obligatoires manquants'}), 400
        else:
            nom = data1['nom']
            prenom = data1['prenom']
            tel = data1['num_tel']
            genre = data1['genre']
            password = data1['mot_passe']
            cur = mysql.connection.cursor()
            cur.execute("SELECT num_tel FROM person_p_t WHERE num_tel = %s", [tel])
            N_tel = cur.fetchone()
            if N_tel:
                return "لديك حساب بالفعل، يمكنك تسجيل الدخول"
            else:
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO person_p_t (nom, prenom, genre, num_tel,mot_passe) "
                            "VALUES (%s, %s, %s, %s, %s)", (nom, prenom,genre, tel, password))
                mysql.connection.commit()
            return '', 201
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({'error': str(e)}), 500




if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=5001, debug=True)