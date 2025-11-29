from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from integraciones.mistral import get_consulta_simple_mistral, get_consulta_sql_mistral, get_traduccion_mistral, get_analisis_sentimiento_mistral, get_chat_con_historia_mistral
from utilidades.utilidades import inicializar_historial, obtener_historial_para_ia, agregar_al_historial, limpiar_historial, obtener_historial_formateado
import time


mistral_bp = Blueprint('mistral', __name__)


@mistral_bp.route('/mistral')
def mistral_index():
    return render_template('mistral/index.html')



@mistral_bp.route('/mistral/prompt', methods=['GET', 'POST'])
def mistral_prompt():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('mistral/prompt.html')
        start_time = time.time()
        respuesta = get_consulta_simple_mistral(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('mistral/prompt.html', **data)
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('mistral/prompt.html', **data)


@mistral_bp.route('/mistral/consulta', methods=['GET', 'POST'])
def mistral_consulta():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('mistral/consulta.html')
        start_time = time.time()
        respuesta = get_consulta_sql_mistral(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('mistral/consulta.html', **data)
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('mistral/consulta.html', **data)



@mistral_bp.route('/mistral/traductor', methods=['GET', 'POST'])
def mistral_traductor():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        idioma = request.form.get('idioma').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('mistral/traductor.html')
        start_time = time.time()
        respuesta = get_traduccion_mistral(prompt, idioma)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('mistral/traductor.html', **data)
        
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('mistral/traductor.html', **data)



@mistral_bp.route('/mistral/sentimiento', methods=['GET', 'POST'])
def mistral_sentimiento():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('mistral/sentimiento.html')
        start_time = time.time()
        respuesta = get_analisis_sentimiento_mistral(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('mistral/sentimiento.html', **data)
        
        
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('mistral/sentimiento.html', **data)



@mistral_bp.route('/mistral/chat-con-historial', methods=['GET', 'POST'])
def mistral_chat_con_historial():
    #inicializar historial al cargar la página
    inicializar_historial()
    
    if request.method=='POST':
        prompt = request.form.get('prompt', '').strip()
        accion = request.form.get('accion', 'enviar')
        

        #manejar acción de limpiar histoial
        if accion=='limpiar':
            limpiar_historial()
            flash("Historial limpiado correctamente", 'success')
            return render_template('mistral/chat_con_historial.html',
                                   historial=[], tiempo_transcurrido='', respuesta='')
        
        if not prompt:
            flash("El prompt no puede estar vacío", 'danger')
            return render_template('mistral/chat_con_historial.html',
                                   historial=obtener_historial_para_ia(), tiempo_transcurrido='', respuesta=''), HTTPStatus.BAD_REQUEST
        
        #agregar el mensaje del usuario al historial
        agregar_al_historial('usuario', prompt)
        start_time = time.time()
        
        historial_formateado = obtener_historial_formateado()
        respuesta=get_chat_con_historia_mistral(mensajes_historial=historial_formateado)    
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)

        #agregar la respuesta de la IA al historial
        agregar_al_historial('asistente', respuesta)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta,
            "historial": obtener_historial_para_ia()
        }
        return render_template('mistral/chat_con_historial.html', **data)
        
    data = {
            "tiempo_transcurrido": "", 
            "respuesta": "",
            "historial": obtener_historial_para_ia()
        }
    return render_template('mistral/chat_con_historial.html', **data)