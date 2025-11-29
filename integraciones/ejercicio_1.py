from flask import abort
from http import HTTPStatus
import requests
import PyPDF2
from dotenv import load_dotenv
import os
load_dotenv()


def extraer_texto_pdf(ruta_pdf):
    texto = ""
    try:
        with open(ruta_pdf, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                texto += page.extract_text() + "\n"
        return texto
    except Exception as e:
        print(f"Error leyendo PDF {e}")
        return ""


def retornarContexto():
    return extraer_texto_pdf("static/pdf/manual_atencion_cliente.pdf")


def get_consulta_rag_mistral(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    """

    data = {
        "model": "mistral-small",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }
    response = requests.post(
        f"{os.getenv('MISTRAL_BASE_URL')}chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('MISTRAL_API_KEY')}"
        },
        json=data
    )
    if response.status_code==200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error al consulta la API de Mistral: {response.status_code} - {response.text}"
    

def get_consulta_rag_gemini(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    - No agregues explicaciones adicionales ni comentarios sobre el formato
    """

    payload ={
        'contents':[
            {
                'parts':[
                    {'text': prompt}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 500
        }
    }

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.0-flash:generateContent?key={os.getenv('GEMINI_API_KEY')}",
            headers={
                "Content-Type": "application/json",
            },
            json = payload
        )
        response.raise_for_status()
        data = response.json()
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        return f"Error al consulta Gemini API: {str(e)}"
    

def get_consulta_rag_gemini_nuevo(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    - No agregues explicaciones adicionales ni comentarios sobre el formato
    """

    payload ={
        'contents':[
            {
                'parts':[
                    {'text': prompt}
                ]
            }
        ],
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 500
        }
    }

    try:
        response = requests.post(
            f"{os.getenv('GEMINI_BASE_URL')}models/gemini-2.5-flash:generateContent",
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": f"{os.getenv('GEMINI_API_KEY')}"
            },
            json = payload
        )
        response.raise_for_status()
        data = response.json()
        respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
        return respuesta_ia
    except requests.exceptions.RequestException as e:
        return f"Error al consulta Gemini API: {str(e)}"


def get_consulta_rag_claude(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    - No agregues explicaciones adicionales ni comentarios sobre el formato
    """

    data = {
        "model": "claude-sonnet-4-5",
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        f"{os.getenv('CLAUDE_BASE_URL')}messages",
        headers={
            "anthropic-version":"2023-06-01",
            "Content-Type":"application/json",
            "x-api-key":f"{os.getenv("CLAUDE_API_KEY")}"
        },
        json = data,
        timeout=120
    )
    if response.status_code==200:
        return response.json()["content"][0]["text"]
    else:
        abort(HTTPStatus.NOT_FOUND)


def get_consulta_rag_deepseek(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    - No agregues explicaciones adicionales ni comentarios sobre el formato
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
    try:
        response = requests.post(
            f"{os.getenv('DEEPSEEK_API_URL')}chat/completions",
            headers={
                "Content-Type":"application/json",
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}"
            },
            json= data,
            timeout=120
        )
        if response.status_code ==200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error al consultar Deepseek API: {response.status_code}- {response.text}"
    except Exception as e:
        return f"Error de conexión con Deepseek: {str(e)}"


def get_consulta_rag_openai(pregunta, contexto_pdf):
    prompt=f"""
    Eres un asistente virtual de atención al cliente.
    Basa tu respuesta EXCLUSIVAMENTE en la siguiente información del manual:

    INFORMACIÓN DEL MANUAL DE ATENCIÓN AL CLIENTE:
    {contexto_pdf}

    PREGUNTA DEL CLIENTE:
    {pregunta}

    INSTRUCCIONES:
    - Response de manera clara y profesional usando ŚOLO la información del manual
    - Si la información no está en el manual, di "No encontré información específica sobre esto en el manual"
    - Mantén un tono amable y útil
    - Sé conciso (máximo 150 palabras)
    - Response en español
    - No agregues explicaciones adicionales ni comentarios sobre el formato
    """
    data = {
        "model": "gpt-4o",
        "messages":[
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 500
    }
    try:
        response = requests.post(
            f"{os.getenv('OPENAI_BASE_URL')}chat/completions",
            headers={
                "Content-Type":"application/json",
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
            },
            json= data,
            timeout=120
        )
        if response.status_code ==200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error al consultar OpenaAI API: {response.status_code}- {response.text}"
    except Exception as e:
        return f"Error de conexión con OpenaAI: {str(e)}"
