from array import array
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from flask import Flask, render_template, request, redirect, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pickle
import os
from flask_serialize import FlaskSerialize
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

load_dotenv()

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
CORS(app)



app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

fs_mixin = FlaskSerialize(db)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

class DataPrediksi(fs_mixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)
    jenis_kelamin = db.Column(db.String(100), nullable=False)
    tempat_lahir = db.Column(db.String(100), nullable=False)
    pendidikan = db.Column(db.String(100), nullable=False)
    no_hp = db.Column(db.Integer, nullable=False)
    jabatan = db.Column(db.String(20), nullable=False)
    penempatan = db.Column(db.String(20), nullable=False)
    lama_kerja = db.Column(db.String(20), nullable=False)
    kehadiran = db.Column(db.Integer, nullable=False)
    sikap = db.Column(db.Integer, nullable=False)
    tanggung_jawab = db.Column(db.Integer, nullable=False)
    pencapaian = db.Column(db.Integer, nullable=False)
    keputusan = db.Column(db.String(100), nullable=False)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "admin":
        return jsonify({"msg": "Anda gak bisa login karena salah gaes"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/", methods=["GET"])
def home():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "dataset.json")
    data = json.load(open(json_url))
    return render_template('read.html', data=data)

@app.route("/predict", methods=["GET"])
def predict_home():
    return render_template('index.html')
    
@app.route("/item/<item_id>", methods=["GET"])
@app.route("/items")
@jwt_required()
def table(item_id = None):
   return DataPrediksi.fs_get_delete_put_post(item_id)


@app.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    data = request.get_json()

    fitur = np.array([
        int(data["kehadiran"]),
        int(data["sikap"]),
        int(data["tanggung_jawab"]),
        int(data["pencapaian"])
    ])

    numpyArray = [np.array(fitur)]

    bener = np.array(numpyArray)

    prediction = model.predict(bener)

    formated_predict = f"{prediction}".replace("[", "").replace("]", "").replace("'", "")

    populate_data = DataPrediksi(
        nama=data["nama"],
        jenis_kelamin=data["jenis_kelamin"],
        tempat_lahir=data["tempat_lahir"],
        pendidikan=data["pendidikan"],
        no_hp=data["no_hp"],
        jabatan=data["jabatan"],
        penempatan=data["penempatan"],
        lama_kerja=data["lama_kerja"],
        kehadiran=data["kehadiran"],
        sikap=data["sikap"],
        tanggung_jawab=data["tanggung_jawab"],
        pencapaian=data["pencapaian"],
        keputusan=formated_predict
    )

    db.session.add(populate_data)
    db.session.commit()

    return {
        "keputusan": formated_predict
    }

if __name__ == "__main__":
    app.run(debug=True)