from elasticsearch import Elasticsearch
from flask import Flask, request, session, redirect, url_for, render_template
from datetime import datetime, timedelta
from google.cloud import storage
from flask_socketio import SocketIO, emit
from pymongo import MongoClient

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'your-secret-key'

client = MongoClient("mongodb://localhost:27017/")
# Cambia esto por el nombre real de tu base de datos
db = client["nombre_de_tu_base_de_datos"]
colección = db["nombre_de_tu_colección"]
# app.register_blueprint(main)
socketio = SocketIO()
socketio.init_app(app)
USERNAME = 'Buscador'
PASSWORD = 'inpahu*'

text_pdf = ""

users = {}

ruta_credenciales = 'green-alchemy-301821-3680caf2273f.json'
client = storage.Client.from_service_account_json(ruta_credenciales)
api_key = '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'


def obtener_url_firma(bucket_nombre, ruta_archivo):
    bucket = client.get_bucket(bucket_nombre)
    blob = bucket.blob(ruta_archivo)
    tiempo_expiracion = datetime.utcnow() + timedelta(hours=1)
    url_firma = blob.generate_signed_url(expiration=tiempo_expiracion)
    return url_firma


@app.route('/')
def home():
    if 'username' in session:
        return render_template('menu.html')
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/buscar", methods=["POST"])
def buscar():
    palabra_clave = request.form.get("palabra_clave")
    es = Elasticsearch("http://10.20.135.13:9200/")
    # es = Elasticsearch("localhost:9200")
    resultados = es.search(index="licitaciones", body={
        # resultados = es.search(index="licitaciones_prueba", body={
        "size": 100,
        "query": {
            "match": {
                "Texto_PDF": palabra_clave
            }
        },
        "aggs": {
            "por_ruta": {
                "terms": {
                    "field": "Ruta"
                }
            }
        },
    })
    if resultados:
        for resultado in resultados['hits']['hits']:
            # texto_pdf=resultado['_source']['Texto_PDF']
            resultado['_source']['ver_pdf'] = resultado["_source"]["Ruta"].replace(
                "\\", "/").replace(
                "C:/Users/jkevi/Dropbox/Mi PC (LAPTOP-GPEOQ0JB)/Documents/CNC/buscador_licitaciones_new/", "Licitaciones/2023/")
    return render_template("resultados_licitaciones.html", resultados=resultados)


@app.route("/ver_pdf", methods=["POST"])
def ver_pdf():
    ruta_pdf = request.form.get("ruta_pdf")

    if ruta_pdf:
        url_pdf = obtener_url_firma("bucket-licitaciones", ruta_pdf)
    return redirect(url_pdf)


@app.route("/contratos")
def contratos():
    return render_template("contratos.html")


@app.route("/buscar_contratos", methods=["POST"])
def buscar_contratos():
    palabra_clave = request.form.get("palabra_clave_contratos")
    es = Elasticsearch("http://10.20.135.13:9200/")
    resultados = es.search(index="contratos", body={
        "size": 100,
        "query": {
            "match": {
                "Texto_PDF": palabra_clave
            }
        },
        "aggs": {
            "por_ruta": {
                "terms": {
                    "field": "Ruta"
                }
            }
        },
    })
    if resultados:
        for resultado in resultados['hits']['hits']:
            resultado['_source']['ver_pdf'] = resultado["_source"]["Ruta"].replace(
                "\\", "/").replace(
                "C:/Users/CNC_02/Documents/CNC/buscador_licitaciones_new/", "")
    return render_template("resultados_contratos.html", resultados=resultados)


@app.route("/certificaciones")
def certificaciones():
    return render_template("certificaciones.html")


@app.route("/buscar_certificaciones", methods=["POST"])
def buscar_certificaciones():
    palabra_clave = request.form.get("palabra_clave_certificaciones")
    es = Elasticsearch("http://10.20.135.13:9200/")
    resultados = es.search(index="certificaciones", body={
        "size": 100,
        "query": {
            "match": {
                "Texto_PDF": palabra_clave
            }
        },
        "aggs": {
            "por_ruta": {
                "terms": {
                    "field": "Ruta"
                }
            }
        },
    })
    if resultados:
        for resultado in resultados['hits']['hits']:
            resultado['_source']['ver_pdf'] = resultado["_source"]["Ruta"].replace(
                "\\", "/").replace(
                "C:/Users/CNC_02/Documents/CNC/buscador_licitaciones_new/", "")
    return render_template("resultados_certificaciones.html", resultados=resultados)


@app.route("/buscar_mongo", methods=["GET", "POST"])
def buscar_mongo():
    if request.method == "POST":
        palabra_clave = request.form.get("palabra_clave")
        # Aquí se esta buscando documentos por un campo específico que contenga la 'palabra_clave'
        resultados = colección.find(
            {"campo_de_búsqueda": {"$regex": palabra_clave, "$options": "i"}})
        return render_template("resultados_mongo.html", resultados=resultados)
    return render_template("buscar_mongo.html")
