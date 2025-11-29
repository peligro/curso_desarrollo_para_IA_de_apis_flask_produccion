from flask import abort
from http import HTTPStatus
import requests
import base64
from dotenv import load_dotenv
import os
load_dotenv()

from utilidades.utilidades import descargar_imagen_con_curl
from aws.aws import get_conection

import time

def get_cabeceros_openai():
    return {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }


def get_consulta_simple_openai(prompt):
    data = {
        "model": "gpt-4o-mini",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
        headers=get_cabeceros_openai(),
        json=data
    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_sql_openai(texto):
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
        "model": "gpt-4o-mini",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2
    }
    response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
        headers=get_cabeceros_openai(),
        json=data
    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_openai(texto, idioma_destino):
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
        "model": "gpt-4o",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
        headers=get_cabeceros_openai(),
        json=data
    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_analisis_sentimiento_openai(texto):
    prompt = f"""
    Analiza el sentimiento del siguiente texto:
    {texto}
    Devuelve sólo: positivo, negativo o neutral.
    """

    data = {
        "model": "gpt-4o-mini",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2
    }
    response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
        headers=get_cabeceros_openai(),
        json=data
    )
    if response.status_code==200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_chat_con_historial_openai(mensajes_historial):
    data={
        "model": "gpt-4o",
        "messages": mensajes_historial,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    try:
        response = requests.post(
        f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
        headers=get_cabeceros_openai(),
        json=data,
        timeout=60
        )
        if response.status_code==200:
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        else:
            print(f"Error en OpenAI API: {response.status_code} - {response.text}")
            abort(HTTPStatus.NOT_FOUND)
    except Exception as e:
        print(f"Error en conexión con OpenAI: {e}")


def get_consulta_imagen_openai(pregunta, url_imagen):
    try:
        response_imagen = requests.get(url_imagen)
        response_imagen.raise_for_status()

        imagen_base64 = base64.b64encode(response_imagen.content).decode('utf-8')
        content_type = response_imagen.headers.get('content-type', 'image/jpeg')

    except requests.exceptions.RequestException as e:
        abort(HTTPStatus.BAD_REQUEST, description=f"Error al descargar la imagen: {str(e)}")

    prompt_optimizado = f"""
    Analiza esta imagen de manera objetiva y descriptiva.
    Enfócate en:
    - Elementos visuales observables
    - personas, cómo estás vestidas, qué están haciendo

    Evita cualquier interpretación médica, emocional o personal
    
    Pregunta específico: {pregunta}
    """

    payload = {
        "model": "gpt-4o",
        "messages":[
            {
                "role": "user",
                "content":[
                    {
                        "type": "text", "text": prompt_optimizado
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64, {imagen_base64}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    try:
        response = requests.post(
            f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
            headers=get_cabeceros_openai(),
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return f"Error al analizar la imagen: {data['error']['message']}"
        
        respuesta_ia = data["choices"][0]["message"]["content"]
        return respuesta_ia

    except requests.exceptions.RequestException as e:
        abort(HTTPStatus.NOT_FOUND)


def transcribir_audio_openai(audio_file_path):
    try:
        #verificar que el archivo existe
        if not os.path.exists(audio_file_path):
            abort(HTTPStatus.BAD_REQUEST, description=f"El archivo de audio no existe")

        with open(audio_file_path, 'rb') as audio_file:
            files ={
                'file': (os.path.basename(audio_file_path ), audio_file, 'audio/mpeg'),
                'model': (None, 'whisper-1'),
                'response_format': (None, 'text'),
                'language': (None, 'es')
            }
            response = requests.post(
                f"{os.getenv('OPENAI_BASE_URL')}audio/transcriptions",
                headers= {
                    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
                },
                files= files
            )
            if response.status_code ==200:
                return response.text
            else:
                abort(HTTPStatus.BAD_REQUEST, description=f"Error en la transcripción {response.status_code} - {response.text}")


    except Exception as e:
        abort(HTTPStatus.BAD_REQUEST, description=f"Error: {str(e)}")

    
def generar_imagem_dall_e_3(prompt):
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1
    }
    try:
        #generar la imagen
        response = requests.post(
            f"{os.getenv('OPENAI_BASE_URL')}images/generations",
            headers=get_cabeceros_openai(),
            json=data
        )
        if response.status_code!=200:
            abort(HTTPStatus.BAD_REQUEST, description=f"Error al generar la imagen: {response.text}")

        response_json = response.json()
        imagen_url = response_json["data"][0]["url"]
        #descargar la imagen usando pycurl
        imagen_content = descargar_imagen_con_curl(imagen_url)
        #subir a s3
        s3_client = get_conection()
        #bucket_name = os.getenv('AWS_BUCKET')
        s3_key = f"dalle_{int(time.time())}.png"
        """
        s3_client.put_object(
            Bucket=os.getenv('AWS_BUCKET'),
            Key = s3_key,
            Body = imagen_content
            ContentType ='image/png'
        )
        """
        s3_client.put_object(
            Bucket=os.getenv('AWS_BUCKET'),
            Key=s3_key,
            Body=imagen_content,
            ContentType='image/png'
        )
        return f"{s3_key}"

    except Exception as e:
        print(f"Error={str(e)}")
        abort(HTTPStatus.NOT_FOUND)