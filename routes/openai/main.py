from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from integraciones.openai import get_consulta_simple_openai, get_consulta_sql_openai, get_traduccion_openai, get_analisis_sentimiento_openai, get_chat_con_historial_openai, get_consulta_imagen_openai, transcribir_audio_openai, generar_imagem_dall_e_3

from utilidades.utilidades import inicializar_historial, obtener_historial_para_ia, agregar_al_historial, limpiar_historial, obtener_historial_formateado

import time

from dotenv import load_dotenv
import os
load_dotenv()


openai_bp = Blueprint('openai', __name__)


@openai_bp.route('/openai')
def openai_index():
    return render_template('openai/index.html')


@openai_bp.route('/openai/prompt', methods=['GET', 'POST'])
def openai_prompt():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/prompt.html')
        start_time = time.time()
        respuesta = get_consulta_simple_openai(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('openai/prompt.html', **data)
    return render_template('openai/prompt.html')


@openai_bp.route('/openai/consulta', methods=['GET', 'POST'])
def openai_consulta():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/consulta.html')
        start_time = time.time()
        respuesta = get_consulta_sql_openai(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('openai/consulta.html', **data)
    return render_template('openai/consulta.html')


@openai_bp.route('/openai/traductor', methods=['GET', 'POST'])
def openai_traductor():
    if request.method=='POST':
        idioma = request.form.get('idioma').strip()
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/traductor.html')
        start_time = time.time()
        respuesta = get_traduccion_openai(prompt, idioma)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('openai/traductor.html', **data)
    return render_template('openai/traductor.html')


@openai_bp.route('/openai/sentimiento', methods=['GET', 'POST'])
def openai_sentimiento():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/sentimiento.html')
        start_time = time.time()
        respuesta = get_analisis_sentimiento_openai(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('openai/sentimiento.html', **data)
    return render_template('openai/sentimiento.html')


@openai_bp.route('/openai/chat-con-historial', methods=['GET', 'POST'])
def openai_chat_con_historial():
    #inicializar historial al cargar la página
    inicializar_historial()
    
    if request.method=='POST':
        prompt = request.form.get('prompt', '').strip()
        accion = request.form.get('accion', 'enviar')
        

        #manejar acción de limpiar histoial
        if accion=='limpiar':
            limpiar_historial()
            flash("Historial limpiado correctamente", 'success')
            return render_template('openai/chat_con_historial.html',
                                   historial=[], tiempo_transcurrido='', respuesta='')
        
        if not prompt:
            flash("El prompt no puede estar vacío", 'danger')
            return render_template('openai/chat_con_historial.html',
                                   historial=obtener_historial_para_ia(), tiempo_transcurrido='', respuesta=''), HTTPStatus.BAD_REQUEST
        
        #agregar el mensaje del usuario al historial
        agregar_al_historial('usuario', prompt)
        start_time = time.time()
        
        historial_formateado = obtener_historial_formateado()
        respuesta=get_chat_con_historial_openai(mensajes_historial=historial_formateado)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)

        #agregar la respuesta de la IA al historial
        agregar_al_historial('asistente', respuesta)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta,
            "historial": obtener_historial_para_ia()
        }
        return render_template('openai/chat_con_historial.html', **data)
        
    data = {
            "tiempo_transcurrido": "", 
            "respuesta": "",
            "historial": obtener_historial_para_ia()
        }
    return render_template('openai/chat_con_historial.html', **data)


@openai_bp.route('/openai/reconocimiento', methods=['GET', 'POST'])
def openai_reconocimiento():
    if request.method=='POST':
        url = request.form.get('url', '').strip()
        prompt = request.form.get('prompt', '').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/reconocimiento.html')
        start_time = time.time()
        respuesta = get_consulta_imagen_openai(prompt, url)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('openai/reconocimiento.html', **data)
    return render_template('openai/reconocimiento.html')


@openai_bp.route('/openai/audio', methods=['GET', 'POST'])
def openai_audio():
    if request.method =='POST':
        audio_path = request.form.get('audio_path', '').strip()

        if not audio_path:
            flash("No se especificó la ruta del audio", "danger")
            return render_template("openai/audio.html"), HTTPStatus.BAD_REQUEST
        
        start_time = time.time()
        try:
            respuesta = transcribir_audio_openai(audio_path)
            end_time = time.time()
            tiempo_transcurrido = round(end_time - start_time, 2)
            
            data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
            }
            return render_template('openai/audio.html', **data)
        except Exception as e:
            flash("Error al transcribir el audio", "danger")
            return render_template("openai/audio.html"), HTTPStatus.BAD_REQUEST
    return render_template('openai/audio.html')


@openai_bp.route('/openai/dall-e-3', methods=['GET', 'POST'])
def openai_dall_e_3():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('openai/dall_e_3.html')
        
        start_time = time.time()

        respuesta = generar_imagem_dall_e_3(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta,
            'bucket': os.getenv('AWS_BUCKET')
        }
        return render_template('openai/dall_e_3.html', **data)
    data={
        'tiempo_transcurrido': '',
        'respuesta': '',
        'bucket': os.getenv('AWS_BUCKET')
    }
    return render_template('openai/dall_e_3.html', **data)