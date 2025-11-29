from flask import abort
from http import HTTPStatus
import requests
import base64
from dotenv import load_dotenv
import os
load_dotenv()


def get_cabeceros():
    return {
        "Content-Type":"application/json"
    }


def get_cabeceros_nuevo():
    return {
        "Content-Type":"application/json",
        "x-goog-api-key": f"{os.getenv('GEMINI_API_KEY')}"
    }


def get_consulta_simple_gemini(pregunta):
    payload = {
        'contents':[
            {
                'parts':[
                    {
                        'text': pregunta
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 500,
        }
    } 
    try:
        #gemini-2.0-flash
        #gemini-2.5-flash
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_simple_gemini_nuevo(pregunta):
    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': pregunta
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.7
        }
    } 
    try:
        #gemini-2.0-flash
        #gemini-2.5-flash
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)



def get_consulta_sql_gemini(texto):
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

    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.2,
            'maxOutputTokens': 500,
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_sql_gemini_nuevo(texto):
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

    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.2
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_gemini(texto, idioma_destino):
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

    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 500,
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_traduccion_gemini_nuevo(texto, idioma_destino):
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

    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.3,
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_analisis_sentimiento_gemini(texto):
    prompt = f"""
    Analiza el sentimiento del siguiente texto:
    {texto}
    Devuelve sólo: positivo, negativo o neutral.
    """
    
    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.2,
            'maxOutputTokens': 500,
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_analisis_sentimiento_gemini_nuevo(texto):
    prompt = f"""
    Analiza el sentimiento del siguiente texto:
    {texto}
    Devuelve sólo: positivo, negativo o neutral.
    """
    
    payload = {
        'contents':[
            {
                'role':'user',
                'parts':[
                    {
                        'text': prompt
                    }
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.2,
        }
    } 

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_chat_con_historial_gemini(mensajes_historial):
    contents = []

    for mensaje in mensajes_historial:
        role = "user" if mensaje["role"]=='user' else "model"
        contents.append(
            {
                'parts': [{'text': mensaje['content']}],
                'role': role
            }
        )
        
    payload = {
        'contents': contents,
        'generationConfig':{
            'temperature': 0.7,
            'maxOutputTokens': 1000,
            'topP': 0.8,
            'topK': 40
        }
    }
    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload,
            timeout=60
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #verificar si hay bloqueos de seguridad
        if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
            return "La conversación no puede continuar debido a restricciones de contenido"
        
        #extraer la respueta
        if 'candidates' in data and len(data['candidates'])>0:
            respuesta = data['candidates'][0]['content']['parts'][0]['text']
            return respuesta
        else:
            print("Error: Gemini no devolvió una respuesta válida")
            abort(HTTPStatus.NOT_FOUND)  

    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_chat_con_historial_gemini_nuevo(mensajes_historial):
    contents = []

    for mensaje in mensajes_historial:
        role = "user" if mensaje["role"]=='user' else "model"
        contents.append(
            {
                'parts': [{'text': mensaje['content']}],
                'role': role
            }
        )
        
    payload = {
        'contents': contents,
        'generationConfig':{
            'temperature': 0.7,
            'topP': 0.8,
            'topK': 40
        }
    }
    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload,
            timeout=60
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()
        #verificar si hay bloqueos de seguridad
        if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
            return "La conversación no puede continuar debido a restricciones de contenido"
        
        #extraer la respueta
        if 'candidates' in data and len(data['candidates'])>0:
            respuesta = data['candidates'][0]['content']['parts'][0]['text']
            return respuesta
        else:
            print("Error: Gemini no devolvió una respuesta válida")
            abort(HTTPStatus.NOT_FOUND)  

    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_imagen_gemini(pregunta, url_imagen):
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
        'contents': [
            {
                'role':'user',
                'parts': [
                    {
                        'text': prompt_optimizado
                    },
                    {
                        'inline_data':{
                            'mime_type': content_type,
                            'data': imagen_base64
                        }
                    }
                ]
            }
        ],
        'generationConfig':{
            'temperature': 0.7,
            'maxOutputTokens': 500,
        }
    }

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()


        #verificar si hay bloqueos de seguridad
        if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
            return "La conversación no puede continuar debido a restricciones de contenido"

        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_imagen_gemini_nuevo(pregunta, url_imagen):
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
    
    Pregunta espefícica: {pregunta}
    """
    payload = {
        'contents': [
            {
                'role':'user',
                'parts': [
                    {
                        'text': prompt_optimizado
                    },
                    {
                        'inline_data':{
                            'mime_type': content_type,
                            'data': imagen_base64
                        }
                    }
                ]
            }
        ],
        'generationConfig':{
            'temperature': 0.7,
        }
    }

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        response.raise_for_status() # Lanza una excepción si hay un error HTTP
        data = response.json()


        #verificar si hay bloqueos de seguridad
        if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
            return "La conversación no puede continuar debido a restricciones de contenido"

        #respuesta_ia = data['candidates'][0]['content']
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        print(e)
        abort(HTTPStatus.NOT_FOUND)


def transcribir_audio_gemini(audio_file_path):
    try:
        #verificar que el archivo existe
        if not os.path.exists(audio_file_path):
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"El archivo de audio no existe")
        
        #verificar tamaño del archivo
        file_size = os.path.getsize(audio_file_path) / (1024 * 1024)  # MB
        if file_size > 20:
            abort(HTTPStatus.BAD_REQUEST, description="El archivo es demasiado grande (máximo 20MB)")

        #determinar el formato del archivo
        file_extension = audio_file_path.lower().split('.')[-1]
        mime_types={
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'm4a': 'audio/mp4',
            'ogg': 'audio/ogg',
            'flac': 'audio/flac',
        }
        mime_type = mime_types.get(file_extension, 'audio/mpeg')

        #leer el archivo de audio y convertirlo a base64
        with open(audio_file_path, 'rb') as audio_file:
            audio_data= audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        #preparar el payload para gemini
        payload ={
            'contents':[
                {
                    'role':'user',
                    'parts':[
                        {
                            'text': "Transcribe este audio a texto exactamente como se escucha. Devuelve solo la transcripción sin comentarios adicionales, títulos o explicaciones"
                        },
                        {
                            'inline_data':{
                                'mime_type': mime_type,
                                'data': audio_base64
                            }
                        }
                    ]
                }
            ],
            'generationConfig':{
                'temperature': 0.1,
                'maxOutputTokens': 2000
            }
        }
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload
        )
        if response.status_code==200:
            data = response.json()

            #verificar si hay bloqueos de seguridad
            if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
                return "La conversación no puede continuar debido a restricciones de contenido"
            
            #extraer la respueta
            if 'candidates' in data and len(data['candidates'])>0:
                respuesta = data['candidates'][0]['content']['parts'][0]['text']
                return respuesta.strip()

        else:
            print(f"Gemini no devolvió una transcripció válida")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Gemini no devolvió una transcripció válida")

    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Error interno: {str(e)}")


def transcribir_audio_gemini_nuevo(audio_file_path):
    try:
        #verificar que el archivo existe
        if not os.path.exists(audio_file_path):
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"El archivo de audio no existe")
        
        #verificar tamaño del archivo
        file_size = os.path.getsize(audio_file_path) / (1024 * 1024)  # MB
        if file_size > 20:
            abort(HTTPStatus.BAD_REQUEST, description="El archivo es demasiado grande (máximo 20MB)")
            
        #determinar el formato del archivo
        file_extension = audio_file_path.lower().split('.')[-1]
        mime_types={
            'mp3': 'audio/mpeg',
            'wav': 'audio/wav',
            'm4a': 'audio/mp4',
            'ogg': 'audio/ogg',
            'flac': 'audio/flac',
        }
        mime_type = mime_types.get(file_extension, 'audio/mpeg')

        #leer el archivo de audio y convertirlo a base64
        with open(audio_file_path, 'rb') as audio_file:
            audio_data= audio_file.read()
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        #preparar el payload para gemini
        payload ={
            'contents':[
                {
                    'role':'user',
                    'parts':[
                        {
                            'text': "Transcribe este audio a texto exactamente como se escucha. Devuelve solo la transcripción sin comentarios adicionales, títulos o explicaciones"
                        },
                        {
                            'inline_data':{
                                'mime_type': mime_type,
                                'data': audio_base64
                            }
                        }
                    ]
                }
            ],
            'generationConfig':{
                'temperature': 0.1
            }
        }
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload
        )
        if response.status_code==200:
            data = response.json()

            #verificar si hay bloqueos de seguridad
            if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
                return "La conversación no puede continuar debido a restricciones de contenido"
            
            #extraer la respueta
            if 'candidates' in data and len(data['candidates'])>0:
                respuesta = data['candidates'][0]['content']['parts'][0]['text']
                return respuesta.strip()

        else:
            print(f"Gemini no devolvió una transcripció válida")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Gemini no devolvió una transcripción válida")

    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Error interno: {str(e)}")


def analizar_video_gemini(video_file_path, pregunta_personalizada=None):

    try:
        #verificar que el archivo existe
        if not os.path.exists(video_file_path):
            abort(HTTPStatus.BAD_REQUEST, description=f"El archivo de video no existe")
        
        
        #leer el archivo de audio y convertirlo a base64
        with open(video_file_path, 'rb') as video_file:
            video_data= video_file.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        #construir el prompt
        if pregunta_personalizada:
            prompt_text=pregunta_personalizada
        else:
            prompt_text="""
            Analiza este video y describe:
            1. Qué se ve en el video (escenas, personas, objetos, acciones)
            2. El contexto o situación
            3. Elementos importantes o destacados

            Sé descriptivo y objetivo
            """
        

        payload ={
            'contents':[
                {
                    'role':'user',
                    'parts':[
                        {
                            'text': prompt_text
                        },
                        {
                            'inline_data':{
                                'mime_type': 'video/mp4',
                                'data': video_base64
                            }
                        }
                    ]
                }
            ],
            'generationConfig':{
                'temperature': 0.2,
                'maxOutputTokens': 1000
            }
        }
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers=get_cabeceros(),
            json=payload,
            timeout= 120
        )
        if response.status_code==200:
            data = response.json()

            #verificar si hay bloqueos de seguridad
            if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
                return "La conversación no puede continuar debido a restricciones de contenido"
            
            #extraer la respueta
            if 'candidates' in data and len(data['candidates'])>0:
                respuesta = data['candidates'][0]['content']['parts'][0]['text']
                return respuesta.strip()

        else:
            print(f"Error al analizar el video: {response.status_code} - {response.text} ")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Gemini no devolvió un análisis válido")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Error interno: {str(e)}")


def analizar_video_gemini_nuevo(video_file_path, pregunta_personalizada=None):

    try:
        #verificar que el archivo existe
        if not os.path.exists(video_file_path):
            abort(HTTPStatus.BAD_REQUEST, description=f"El archivo de video no existe")
        
        
        #leer el archivo de audio y convertirlo a base64
        with open(video_file_path, 'rb') as video_file:
            video_data= video_file.read()
            video_base64 = base64.b64encode(video_data).decode('utf-8')
        
        #construir el prompt
        if pregunta_personalizada:
            prompt_text=pregunta_personalizada
        else:
            prompt_text="""
            Analiza este video y describe:
            1. Qué se ve en el video (escenas, personas, objetos, acciones)
            2. El contexto o situación
            3. Elementos importantes o destacados

            Sé descriptivo y objetivo
            """
        

        payload ={
            'contents':[
                {
                    'role':'user',
                    'parts':[
                        {
                            'text': prompt_text
                        },
                        {
                            'inline_data':{
                                'mime_type': 'video/mp4',
                                'data': video_base64
                            }
                        }
                    ]
                }
            ],
            'generationConfig':{
                'temperature': 0.2,
            }
        }
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers=get_cabeceros_nuevo(),
            json=payload,
            timeout= 120
        )
        if response.status_code==200:
            data = response.json()

            #verificar si hay bloqueos de seguridad
            if 'promptFeedback' in data and 'blockReason' in data['promptFeedback']:
                return "La conversación no puede continuar debido a restricciones de contenido"
            
            #extraer la respueta
            if 'candidates' in data and len(data['candidates'])>0:
                respuesta = data['candidates'][0]['content']['parts'][0]['text']
                return respuesta.strip()

        else:
            print(f"Error al analizar el video: {response.status_code} - {response.text} ")
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Gemini no devolvió un análisis válido")
    except Exception as e:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, description=f"Error interno: {str(e)}")