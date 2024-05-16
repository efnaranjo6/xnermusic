from flask import Flask, render_template, request, redirect, url_for, session, jsonify,make_response,send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import  datetime
import soundfile as sf
#from spleeter.separator import Separator
import os
import sys
import logging
import librosa
import numpy as np
app = Flask(__name__,template_folder='templates')
db_config = {
    'user': 'my_user',
    'password': 'my_password',
    'host': 'p_a-dbs-1',
    'port': '5432',
    'database': 'my_database'
}

# Crea la cadena de conexión
db_url = f'postgresql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['APP_UPLOAD_FOLDER'] = 'musica_no_procesada'
db = SQLAlchemy(app)


@app.route("/")
def hello_world():

    return  render_template('index.html')
@app.route("/login",methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            query= text("SELECT * from login where  correo=:correo AND password=:password")
            resultados = db.session.execute(query.params(correo=username, password=password)).fetchall()
            if resultados:
                return render_template('dashboard.html', datadsh=resultados)
            else :
                return render_template('login.html')
@app.route("/subir",methods=['GET', 'POST'])
def subida_archivos():
    if request.method == 'GET':
        query= text("SELECT * from document")
        resultados = db.session.execute(query).fetchall()
        return render_template('subr_archivo.html',data=resultados)
    elif request.method == 'POST':
        archivo = request.files['file']
        now = datetime.now()
        fecha_actual = now.strftime("%Y-%m-%d")
        hora_actual = now.strftime("%H:%M:%S")
        concathora=fecha_actual+'-'+hora_actual
        archivo.save(os.path.join(app.config['APP_UPLOAD_FOLDER'],  concathora+".wav"))
        uri=app.config['APP_UPLOAD_FOLDER']+"/"+concathora+".wav"
        db.session.execute(text("INSERT INTO document (uri, nombre) VALUES (:uri,:nombre)"),{"uri":uri, "nombre":archivo.filename})
        db.session.commit()
        return render_template('subr_archivo.html') 
@app.route("/procesamiento",methods=['GET', 'POST'])
def procesar():
    if request.method == 'GET':
        query= text("SELECT * from document")
        resultados = db.session.execute(query).fetchall()
        return render_template('procesamiento.html', data=resultados)
    elif request.method == 'POST':
        uri=''
        id_pista = request.form['id_pista']
        tipo = request.form['tipo_procesamiento']
        query= text("SELECT * from document where  id=:id_pista")
        resultados = db.session.execute(query.params(id_pista=id_pista)).fetchall()
        for row in resultados:
           uri= row.uri
        y, sr = librosa.load(uri)   
        S = np.abs(librosa.stft(y))
        harmonic, percussive = librosa.effects.hpss(y)
        sf.write(app.config['APP_UPLOAD_FOLDER']+"/"+'harmonic.wav', harmonic, sr)
        sf.write(app.config['APP_UPLOAD_FOLDER']+"/"+'percussive.wav', percussive, sr)
        return render_template('procesamiento.html')
    #send_file(uri, as_attachment=True)
        
     
if __name__ == '__main__':
 

    app.run(debug=True, host='0.0.0.0')