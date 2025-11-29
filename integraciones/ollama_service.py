from flask import abort
from http import HTTPStatus
import json
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def get_cabeceros_ollama_service():
    return {
        "Content-Type":"application/json",
    }


def get_consulta_simple_ollama_service(prompt, model="tinyllama"):
    data = {
        "model": model,
        "messages": [{"role":"user", "content": prompt}],
        "stream": True
    }
    try:
        response = requests.post(
            f"{os.getenv('OLLAMA_BASE_URL')}api/chat",
            json= data,
            stream= True,
            timeout= 60,
            headers=get_cabeceros_ollama_service()
        )
        if response.status_code==200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_data= json.loads(line)
                    if 'message' in line_data and 'content' in line_data['message']:
                        chunk = line_data['message']['content']
                        full_response += chunk
                    if line_data.get('done', False):
                        break
            return full_response
        else:
            abort(HTTPStatus.NOT_FOUND)
    except Exception as e:
        #print(f"Error: {e}")
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_sql_ollama_service(texto, model="tinyllama"):
    schema="""
        Tabla: users
        Columnas:
        - id (int)
        - name (string)
        - email (string)
        - state_id (int)
        - created_at (datetime)
    """
    prompt = f"""
    Eres un experto en bases de datos PostgreSQL. Tu tarea es convertir este texto en un consulta SQL válida:
    Texto: "{texto}"
    Esquema de la tabla:
    {schema}
    Reglas de formato:
    - Nunca uses * en las consultas SQL.
    - Siempre ordena los datos por el id de forma descendente
    - Sólo devuelve la consulta SQL, sin explicaciones ni comentarios, ni anotaciones Markdown, ni al inicio ni al final
    - no user ``` ni al inicio ni al final de tu respuesta
    """

    data = {
        "model": model,
        "messages": [
            {"role":"user", "content": prompt}
            ],
        "stream": False
    }
    try:
        response = requests.post(
            f"{os.getenv('OLLAMA_BASE_URL')}api/chat",
            json= data,
            timeout= 60,
            headers=get_cabeceros_ollama_service()
        )
        if response.status_code==200:
            consulta_sql = response.json()["message"]["content"]
            return consulta_sql
        else:
            #print(f"Error: {e}")
            abort(HTTPStatus.NOT_FOUND)
    except Exception as e:
        print(f"Error: {e}")
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_ollama_service(texto, idioma_destino, model="tinyllama"):
    prompt = f"""
    Traduce el siguiente texto al {idioma_destino}:
    {texto}
    Reglas:
    - Mantén el tono y estilo del texto original.
    - Solo devuelve la traducción, sin explicaciones adicionales, ni al inicio ni al final.
    - No muestres ninguna nota ni al final ni al inicio, sólo devuelve la traducción, de ningún tipo.
    - No muestres tampoco indicaciones referentes al tipo de caracteres usados, ni tampoco ninguna advertencia.
    """

    data = {
        "model": model,
        "messages": [
            {"role":"user", "content": prompt}
            ],
        "stream": False
    }
    try:
        response = requests.post(
            f"{os.getenv('OLLAMA_BASE_URL')}api/chat",
            json= data,
            timeout= 180,
            headers=get_cabeceros_ollama_service()
        )
        if response.status_code==200:
            return response.json()["message"]["content"]
        else:
            #print(f"Error: {e}")
            abort(HTTPStatus.NOT_FOUND)
    except Exception as e:
        print(f"Error: {e}")
        abort(HTTPStatus.NOT_FOUND)

