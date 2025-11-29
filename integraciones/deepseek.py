from flask import abort
from http import HTTPStatus
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def get_cabeceros_deepseek():
    return {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
    }


def get_consulta_simple_deepseek(prompt):
    data = {
        "model": "deepseek-chat",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    response = requests.post(
        f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
        headers= get_cabeceros_deepseek(),
        json= data
    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_sql_deepseek(texto):
    schema ="""
    Tabla: users
    Columnas:
    - id (int)
    - name (string)
    - email (string)
    - state_id (int)
    - created_at (datetime)
    """

    prompt = f"""
    Eres un experto en bases de datos PostgreSQL. Tu tarea es convertir este texto en una consulta SQL válida:
    Texto: {texto}
    Esquema de la tabla:
    {schema}
    Reglas de formato:
    - Nunca uses * en las consultas SQL.
    - Siempre ordena los datos por el id de forma descendente
    - Sólo devuelve la consulta SQL, sin expliaciones ni comentarios, ni al inicio ni al final.
    - no envuelvas la consulta en ```sql ```
    """

    data = {
        "model": "deepseek-chat",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }
    response = requests.post(
        f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
        headers= get_cabeceros_deepseek(),
        json= data
    )
    if response.status_code==200:
        consulta_sql = response.json()["choices"][0]["message"]["content"]
        return consulta_sql
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_deepseek(texto, idioma_destino):
    prompt = f"""
    Eres un experto en idiomas y traducción de textos.
    Traduce el siguiente texto al {idioma_destino}:
    {texto}
    Reglas:
    - Mantén el tono y estilo del texto original.
    - Sólo devuelve la traducción, sin explicaciones adicionales, ni al inicio ni al final.
    - no muestras ninguna nota ni al final ni al inicio, sólo devuelve la traducción, de ningún tipo.
    - no muestres tampoco indicadores referentes al tipo de caracteres usados, ni tampoco ninguna advertencia
    """
    
    data = {
        "model": "deepseek-chat",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    response = requests.post(
        f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
        headers= get_cabeceros_deepseek(),
        json= data
    )
    if response.status_code==200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_analisis_sentimiento_deepseek(texto):
    prompt = f"""
    Analiza el sentimiento del siguiente texto:
    {texto}
    Devuelve sólo: positivo, negativo o neutral.
    """
    
    data = {
        "model": "deepseek-chat",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 500
    }
    response = requests.post(
        f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
        headers= get_cabeceros_deepseek(),
        json= data
    )
    if response.status_code==200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_chat_con_historial_deepseek(mensajes_historial):

    data={
        "model": "deepseek-chat",
        "messages": mensajes_historial,
        "temperature": 0.7,
        "max_tokens": 2000,
        "stream": False
    }

    try:
        response = requests.post(
        f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
        headers= get_cabeceros_deepseek(),
        json= data,
        timeout=60
        )
        if response.status_code==200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"Error en Deepseek API: {response.status_code} - {response.text}")
            abort(HTTPStatus.NOT_FOUND)
    except Exception as e:
        print(f"Error de conexión con Deepseek: {e}")
        abort(HTTPStatus.NOT_FOUND)