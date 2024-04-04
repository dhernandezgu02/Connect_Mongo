from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["proyecto_pia"]

collection = db["documentos_inpahu"]

documento_inicial = {"nombre": "Documento de prueba",
                     "contenido": "Este es un documento de prueba en la colección documentos_inpahu."}
collection.insert_one(documento_inicial)

print("Base de datos y colección creadas exitosamente.")
