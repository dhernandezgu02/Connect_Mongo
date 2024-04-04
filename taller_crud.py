from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["universidad"]
collection = db["profesor"]


def insertar_documento():
    nombre = input("Ingrese el nombre: ")
    edad = input("Ingrese la edad: ")
    ciudad = input("Ingrese la ciudad: ")
    documento = {"nombre": nombre, "edad": edad, "ciudad": ciudad}
    collection.insert_one(documento)
    print("Documento insertado exitosamente.")


def buscar_documento():
    nombre = input("Ingrese el nombre para buscar: ")
    resultado = collection.find_one({"nombre": nombre})
    if resultado:
        print("Documento encontrado:", resultado)
    else:
        print("Documento no encontrado.")


def actualizar_documento():
    nombre = input("Ingrese el nombre del documento a actualizar: ")
    nuevo_nombre = input("Ingrese el nuevo nombre: ")
    nueva_edad = input("Ingrese la nueva edad: ")
    nueva_ciudad = input("Ingrese la nueva ciudad: ")
    nuevo_valor = {"$set": {"nombre": nuevo_nombre,
                            "edad": nueva_edad, "ciudad": nueva_ciudad}}
    resultado = collection.update_one({"nombre": nombre}, nuevo_valor)
    if resultado.modified_count:
        print("Documento actualizado exitosamente.")
    else:
        print("No se encontró ningún documento para actualizar.")


def eliminar_documento():
    nombre = input("Ingrese el nombre del documento a eliminar: ")
    resultado = collection.delete_one({"nombre": nombre})
    if resultado.deleted_count:
        print("Documento eliminado exitosamente.")
    else:
        print("No se encontró ningún documento para eliminar.")


while True:
    print("\nSeleccione una opción:")
    print("1. Insertar documento")
    print("2. Buscar documento")
    print("3. Actualizar documento")
    print("4. Eliminar documento")
    print("5. Salir")

    opcion = input("Ingrese el número de opción: ")

    if opcion == "1":
        insertar_documento()
    elif opcion == "2":
        buscar_documento()
    elif opcion == "3":
        actualizar_documento()
    elif opcion == "4":
        eliminar_documento()
    elif opcion == "5":
        break
    else:
        print("Opción no válida. Por favor, ingrese un número del 1 al 5.")
