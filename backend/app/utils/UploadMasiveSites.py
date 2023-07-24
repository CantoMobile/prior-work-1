import json
import os

from flask import jsonify
from app.services.site_service import create_masive_sites


def upload_masive_sites(archive):
    print(archive)
    print("STARTING")
    list_sites = leer_archivo_json(archive)
    response = create_masive_sites(list_sites)
    print(response)
    # if os.path.exists(archive):
    #     os.remove(archive)
    #     print(f"Archivo '{archive}' eliminado.")
    return jsonify({"response": "ejecutado"})

def leer_archivo_json(nombre_archivo):
    print(nombre_archivo)
    lista_diccionarios = []
    with open(nombre_archivo, 'r') as archivo:
        contenido = archivo.read()
        try:
            json_lista = json.loads(contenido)
            lista_diccionarios.extend(json_lista)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
    return lista_diccionarios


