from flask import abort
from http import HTTPStatus
import requests
from dotenv import load_dotenv
import os
load_dotenv()
import time


def get_cabeceros_perplexity():
    return {
        "Content-Type":"application/json",
        "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}"
    }


def get_busqueda_basica_perplexity(pregunta):
    data = {
        "model":"sonar",
        "messages":[
            {
                "role": "user",
                "content": pregunta
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.2,
        "return_citations": True,
        "stream": False
    }
    try:
        response = requests.post(
            f"{os.getenv('PERPLEXITY_BASE_URL')}chat/completions",  # URL directa para evitar problemas
            headers=get_cabeceros_perplexity(),
            json=data,
            timeout=60
        )
        if response.status_code ==200:
            response_json = response.json()

            #extraer la respuesta principal
            respuesta = response_json["choices"][0]["message"]["content"]

            #extraer citas/fuentes si están disponibles
            citas = []
            if 'citations' in response_json:
                citas = response_json['citations']    

            return {
            "respuesta": respuesta,
            "citas": citas,
            "modelo_usado": "sonar",
            "error": False
            }
        else:
            error_msg=f"Error {response.status_code} - {response.text}"
            return {
            "respuesta": f"Error en conexión: {error_msg}",
            "citas": [],
            "modelo_usado": "sonar",
            "error": True
        }
    except Exception as e:
        print(f"Error en conexión: {e}")
        return {
            "respuesta": f"Error en conexión: {e}",
            "citas": [],
            "modelo_usado": "sonar",
            "error": True
        }


def get_parametros_investigacion_perplexity():
    """
    Devuelve opciones predefinidas para investigación avanzada
    """
    return {
        "dominios": {
            "tecnologia": "github.com, stackoverflow.com, techcrunch.com",
            "academico": "arxiv.org, scholar.google.com, researchgate.net, cesarcancino.com",
            "noticias": "bbc.com, cnn.com, reuters.com, elpais.com",
            "programacion": "stackoverflow.com, github.com, docs.python.org",
            "medicina": "pubmed.gov, who.int, nejm.org"
        },
        "rangos_fecha": {
            "ultima_semana": "última semana",
            "ultimo_mes": "último mes", 
            "ultimo_ano": "último año",
            "2024": "año 2024",
            "2023_2024": "2023-2024"
        },
        "idiomas": {
            "es": "Español",
            "en": "Inglés",
            "fr": "Francés",
            "de": "Alemán"
        },
        "enfoques": {
            "noticias": "Noticias recientes",
            "academico": "Contenido académico",
            "tecnico": "Documentación técnica",
            "general": "Información general"
        },
        "profundidades": {
            "rapida": "Búsqueda rápida",
            "balanceada": "Balanceada",
            "profunda": "Investigación profunda"
        }
    }


def get_investigacion_avanzada_perplexity(pregunta, parametros = None):
    parametros_default= {
        'model': 'sonar',
        'max_tokens': 1500,
        'temperature': 0.3,
        'return_citations': True,
        'stream': False
    }
    if parametros:
        parametros_default.update(parametros)
    
    mensaje_usuario = pregunta

    contexto_extra = []

    if parametros_default.get('search_domain'):
        contexto_extra.append(f"Buscar específicamente en: {parametros_default['search_domain']}")
    

    if parametros_default.get('date_range'):
        contexto_extra.append(f"Información del período: {parametros_default['date_range']}")

    
    if parametros_default.get('language'):
        contexto_extra.append(f"Priorizar contenido en: {parametros_default['language']}")

    
    if parametros_default.get('focus'):
        contexto_extra.append(f"Enfócate en: {parametros_default['focus']}")

    if contexto_extra:
        contexto_texto = ". ".join(contexto_extra)
        mensaje_usuario = f"{pregunta}\n\nContento: {contexto_texto}"
    
    data = {
       
        "model": parametros_default['model'],
        "messages": [
            {
                "role": "user",
                "content": mensaje_usuario
            }
        ],
        "max_tokens": parametros_default["max_tokens"],
        "temperature": parametros_default["temperature"],
        "return_citations": parametros_default["return_citations"],
        "stream": parametros_default["stream"]
    }

    try:
        response = requests.post(
            f"{os.getenv('PERPLEXITY_BASE_URL')}chat/completions",  # URL directa para evitar problemas
            headers=get_cabeceros_perplexity(),
            json=data,
            timeout=90
        )
        if response.status_code ==200:
            response_json = response.json()

            #extraer la respuesta principal
            respuesta = response_json["choices"][0]["message"]["content"]

            #extraer citas/fuentes si están disponibles
            citas = response_json.get('citations', []) 

            return {
            "respuesta": respuesta,
            "citas": citas,
            "modelo_usado": parametros_default["model"],
            "parametros_usados": parametros_default,
            "error": False
            }
        else:
            error_msg=f"Error {response.status_code} - {response.text}"
            return {
            "respuesta": f"Error en la investigación: {error_msg}",
            "citas": [],
            "modelo_usado": parametros_default["model"],
            "parametros_usados": parametros_default,
            "error": True
        }
    except Exception as e:
        print(f"Error en conexión: {e}")
        return {
            "respuesta": f"Error en conexión: {e}",
            "citas": [],
            "modelo_usado": parametros_default["model"],
            "parametros_usados": parametros_default,
            "error": True
        }


def get_busqueda_comparativa_perplexity(pregunta, incluir_analisis=True):
    
    #primera búsqueda
    prompt_perplexity = pregunta
    data_perplexity = {
        "model": "sonar",
        "messages":[
            {
                "role": "user",
                "content": prompt_perplexity
            }
        ],
        "max_tokens": 1200,
        "temperature": 0.2,
        "return_citations": True,
        "stream": False
    }
    #segunda búsqueda
    prompt_tradicional = f"""
        Responde de manera directa y concisa a esta pregunta, como lo haría un motor de búsqueda tradicional:
        "{pregunta}"

        Proporciona una respuesta factual sin análisis extenso
    """
    data_tradicional = {
        "model": "sonar",
        "messages":[
            {
                "role": "user",
                "content": prompt_tradicional
            }
        ],
        "max_tokens": 800,
        "temperature": 0.1,
        "return_citations": True,
        "stream": False
    }
    try:
        resultados = {}
        tiempos = {}
        #búsqueda perplexity
        start_time = time.time()
        response_perplexity = requests.post(
            f"{os.getenv('PERPLEXITY_BASE_URL')}chat/completions",
            headers=get_cabeceros_perplexity(),
            json= data_perplexity,
            timeout=60
        )
        tiempos['perplexity'] = round(time.time() - start_time, 2)
        #búsqueda tradicional
        start_time = time.time()
        response_tradicional = requests.post(
            f"{os.getenv('PERPLEXITY_BASE_URL')}chat/completions",
            headers=get_cabeceros_perplexity(),
            json= data_tradicional,
            timeout=60
        )
        tiempos['tradicional'] = round(time.time() - start_time, 2)

        if response_perplexity.status_code==200:
            response_json = response_perplexity.json()
            resultados['perplexity']={
                "respuesta": response_json["choices"][0]["message"]["content"],
                "citas": response_json.get('citations', []),
                "error": False
            }
        else:
            resultados['perplexity'] = {
                "respuesta": f"Error en búsqueda perplexity: {response_perplexity.status_code} - {response_perplexity.text}",
                "citas": [],
                "error": True
            }
        
        if response_tradicional.status_code==200:
            response_json = response_tradicional.json()
            resultados['tradicional']={
                "respuesta": response_json["choices"][0]["message"]["content"],
                "citas": response_json.get('citations', []),
                "error": False
            }
        else:
            resultados['tradicional'] = {
                "respuesta": f"Error en búsqueda tradicional: {response_tradicional.status_code} - {response_tradicional.text}",
                "citas": [],
                "error": True
            }
        #análisis comparativo automático (opcional)
        analisis_comparativo = ""
        #if incluir_analisis and not resultados['perplexity']['error'] and not resultados['tradicional']['error']:
        prompt_analisis=f"""
                    Analiza y compara estas dos respuesta a la misma pregunta:
                    PREGUNTA: "{pregunta}"

                    RESPUESTA_PERPLEXITY (conversacional):
                    {resultados['perplexity']['respuesta']}

                    RESPUESTA_TRADICIONAL (directa):
                    {resultados['tradicional']['respuesta']}

                    Proporciona un análisis breve (máximo 200 palabras) comparando:
                    1. Estilo y profundidad de cada respuesta
                    2. Utilidad para diferentes tipos de usuarios
                    3. Ventajas de cada enfoque

                Sé objetivo y conciso.
                """
        data_analisis = {
                "model": "sonar",
                "messages":[
                        {
                            "role": "user",
                            "content": prompt_analisis
                        }
                ],
                "max_tokens": 400,
                "temperature": 0.3, 
                "stream": False
            }
        try:
            response_analisis = requests.post(
                    f"{os.getenv('PERPLEXITY_BASE_URL')}chat/completions",
                headers=get_cabeceros_perplexity(),
                    json= data_analisis,
                    timeout=30
                )
            if response_analisis.status_code == 200:
                response_json2 = response_analisis.json()
                analisis_comparativo = response_json2["choices"][0]["message"]["content"]
            
        except Exception as e:
            analisis_comparativo = "Análsis comparativo no disponible"
            
        
        return{
                "resultados": resultados,
                "tiempos": tiempos,
                "analisis_comparativo": analisis_comparativo,
                "pregunta_original": pregunta,
                "error": False,
            }
        

    except Exception as e:
        return{
            "resultados": {},
            "tiempos": {},
            "analisis_comparativo": "",
            "pregunta_original": pregunta,
            "error": True,
            "mensaje_error": f"Error en búsqueda comparativa: {str(e)}"
        }