from flask import abort
from http import HTTPStatus
import requests
import base64
from dotenv import load_dotenv
import os
load_dotenv()


def get_cabeceros():
    return {
        "anthropic-version":"2023-06-01",
        "Content-Type":"application/json",
        "x-api-key":f"{os.getenv("CLAUDE_API_KEY")}"
    }


def get_consulta_simple_claude(prompt):
    data = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 100,
        "messages": [
            {
                "role":"user",
                "content": prompt
            }
        ]
    }
    response = requests.post(
        f"{os.getenv("CLAUDE_BASE_URL")}messages",
        headers= get_cabeceros(),
        json= data

    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_sql_claude(texto):
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
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [
            {
                "role":"user",
                "content": prompt
            }
        ]
    }
    response = requests.post(
        f"{os.getenv("CLAUDE_BASE_URL")}messages",
        headers= get_cabeceros(),
        json= data

    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_claude(texto, idioma_destino):
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
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [
            {
                "role":"user",
                "content": prompt
            }
        ]
    }
    response = requests.post(
        f"{os.getenv("CLAUDE_BASE_URL")}messages",
        headers= get_cabeceros(),
        json= data

    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_analisis_sentimiento_claude(texto):
    
    prompt = f"""
    Analiza el sentimiento del siguiente texto:
    {texto}
    Devuelve sólo: positivo, negativo o neutral.
    """

    data = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [
            {
                "role":"user",
                "content": prompt
            }
        ]
    }
    response = requests.post(
        f"{os.getenv("CLAUDE_BASE_URL")}messages",
        headers= get_cabeceros(),
        json= data

    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_chat_con_historial_claude(mensajes_historial):

    messages = [] # [{"role":"user", "content": "pregunta"}, {"role":"asistant", "content": "respuesta"}]

    for mensaje  in mensajes_historial:
        role = mensaje['role']
        content = mensaje['content']

        messages.append({
            "role": role,
            "content": content
        })
    
    
    data = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": 0.3
    }
    response = requests.post(
        f"{os.getenv("CLAUDE_BASE_URL")}messages",
        headers= get_cabeceros(),
        json= data,
        timeout=60

    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)