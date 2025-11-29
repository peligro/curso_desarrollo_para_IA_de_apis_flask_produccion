from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from integraciones.claude import get_consulta_simple_claude, get_consulta_sql_claude, get_traduccion_claude, get_analisis_sentimiento_claude, get_chat_con_historial_claude

from utilidades.utilidades import inicializar_historial, obtener_historial_para_ia, agregar_al_historial, limpiar_historial, obtener_historial_formateado_claude

import time


claude_bp = Blueprint('claude', __name__)


@claude_bp.route('/claude')
def claude_index():
    return render_template('claude/index.html')


@claude_bp.route('/claude/prompt', methods=['GET', 'POST'])
def claude_prompt():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('claude/prompt.html')
        start_time = time.time()
        respuesta = get_consulta_simple_claude(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('claude/prompt.html', **data)
    return render_template('claude/prompt.html')


@claude_bp.route('/claude/consulta', methods=['GET', 'POST'])
def claude_consulta():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('claude/consulta.html')
        start_time = time.time()
        respuesta = get_consulta_sql_claude(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('claude/consulta.html', **data)
    return render_template('claude/consulta.html')


@claude_bp.route('/claude/traductor', methods=['GET', 'POST'])
def claude_traductor():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        idioma = request.form.get('idioma').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('claude/traductor.html')
        start_time = time.time()
        respuesta = get_traduccion_claude(prompt, idioma)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('claude/traductor.html', **data)
    return render_template('claude/traductor.html')


@claude_bp.route('/claude/sentimiento', methods=['GET', 'POST'])
def claude_sentimiento():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('claude/sentimiento.html')
        start_time = time.time()
        respuesta = get_analisis_sentimiento_claude(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('claude/sentimiento.html', **data)
    return render_template('claude/sentimiento.html')


@claude_bp.route('/claude/chat-con-historial', methods=['GET', 'POST'])
def claude_chat_con_historial():
    #inicializar historial al cargar la página
    inicializar_historial()
    
    if request.method=='POST':
        prompt = request.form.get('prompt', '').strip()
        accion = request.form.get('accion', 'enviar')
        

        #manejar acción de limpiar histoial
        if accion=='limpiar':
            limpiar_historial()
            flash("Historial limpiado correctamente", 'success')
            return render_template('claude/chat_con_historial.html',
                                   historial=[], tiempo_transcurrido='', respuesta='')
        
        if not prompt:
            flash("El prompt no puede estar vacío", 'danger')
            return render_template('claude/chat_con_historial.html',
                                   historial=obtener_historial_para_ia(), tiempo_transcurrido='', respuesta=''), HTTPStatus.BAD_REQUEST
        
        #agregar el mensaje del usuario al historial
        agregar_al_historial('usuario', prompt)
        start_time = time.time()
        
        historial_formateado = obtener_historial_formateado_claude()
        respuesta=get_chat_con_historial_claude(mensajes_historial=historial_formateado) 
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)

        #agregar la respuesta de la IA al historial
        agregar_al_historial('asistente', respuesta)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta,
            "historial": obtener_historial_para_ia()
        }
        return render_template('claude/chat_con_historial.html', **data)
        
    data = {
            "tiempo_transcurrido": "", 
            "respuesta": "",
            "historial": obtener_historial_para_ia()
        }
    return render_template('claude/chat_con_historial.html', **data)