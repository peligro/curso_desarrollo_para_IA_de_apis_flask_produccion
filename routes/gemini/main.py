from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from integraciones.gemini import get_consulta_simple_gemini, get_consulta_simple_gemini_nuevo, get_consulta_sql_gemini, get_consulta_sql_gemini_nuevo, get_traduccion_gemini, get_traduccion_gemini_nuevo, get_analisis_sentimiento_gemini, get_analisis_sentimiento_gemini_nuevo, get_chat_con_historial_gemini, get_chat_con_historial_gemini_nuevo, get_consulta_imagen_gemini, get_consulta_imagen_gemini_nuevo, transcribir_audio_gemini, transcribir_audio_gemini_nuevo, analizar_video_gemini, analizar_video_gemini_nuevo

from utilidades.utilidades import inicializar_historial, obtener_historial_para_ia, agregar_al_historial, limpiar_historial, obtener_historial_formateado_gemini
import time


gemini_bp = Blueprint('gemini', __name__)


@gemini_bp.route('/gemini')
def gemini_index():
    return render_template('gemini/index.html')


@gemini_bp.route('/gemini/prompt', methods=['GET', 'POST'])
def gemini_prompt():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('gemini/prompt.html')
        start_time = time.time()
        respuesta = get_consulta_simple_gemini(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('gemini/prompt.html', **data)
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/prompt.html', **data)



@gemini_bp.route('/gemini/consulta', methods=['GET', 'POST'])
def gemini_consulta():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('gemini/consulta.html')
        start_time = time.time()
        respuesta = get_consulta_sql_gemini_nuevo(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('gemini/consulta.html', **data)
        
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/consulta.html', **data)



@gemini_bp.route('/gemini/traductor', methods=['GET', 'POST'])
def gemini_traductor():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        idioma = request.form.get('idioma').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('gemini/traductor.html')
        start_time = time.time()
        respuesta = get_traduccion_gemini_nuevo(prompt, idioma)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('gemini/traductor.html', **data)
        
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/traductor.html', **data)


@gemini_bp.route('/gemini/sentimiento', methods=['GET', 'POST'])
def gemini_sentimiento():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('gemini/sentimiento.html')
        start_time = time.time()
        respuesta = get_analisis_sentimiento_gemini_nuevo(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_trasncurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('gemini/sentimiento.html', **data)
        
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/sentimiento.html', **data)


@gemini_bp.route('/gemini/chat-con-historial', methods=['GET', 'POST'])
def gemini_chat_con_historial():
    #inicializar historial al cargar la página
    inicializar_historial()
    
    if request.method=='POST':
        prompt = request.form.get('prompt', '').strip()
        accion = request.form.get('accion', 'enviar')
        

        #manejar acción de limpiar histoial
        if accion=='limpiar':
            limpiar_historial()
            flash("Historial limpiado correctamente", 'success')
            return render_template('gemini/chat_con_historial.html',
                                   historial=[], tiempo_transcurrido='', respuesta='')
        
        if not prompt:
            flash("El prompt no puede estar vacío", 'danger')
            return render_template('gemini/chat_con_historial.html',
                                   historial=obtener_historial_para_ia(), tiempo_transcurrido='', respuesta=''), HTTPStatus.BAD_REQUEST
        
        #agregar el mensaje del usuario al historial
        agregar_al_historial('usuario', prompt)
        start_time = time.time()
        
        historial_formateado = obtener_historial_formateado_gemini()
        respuesta=get_chat_con_historial_gemini_nuevo(mensajes_historial=historial_formateado)    
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)

        #agregar la respuesta de la IA al historial
        agregar_al_historial('asistente', respuesta)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta,
            "historial": obtener_historial_para_ia()
        }
        return render_template('gemini/chat_con_historial.html', **data)
        
    data = {
            "tiempo_transcurrido": "", 
            "respuesta": "",
            "historial": obtener_historial_para_ia()
        }
    return render_template('gemini/chat_con_historial.html', **data)


@gemini_bp.route('/gemini/reconocimiento', methods=['GET', 'POST'])
def gemini_reconocimiento():
    if request.method=='POST':
        url = request.form.get('url').strip()
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('gemini/reconocimiento.html')
        start_time = time.time()
        respuesta = get_consulta_imagen_gemini_nuevo(prompt, url)
        #print(respuesta)
        end_time = time.time()
        tiempo_trasncurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_trasncurrido, 
            "respuesta": respuesta
        }
        return render_template('gemini/reconocimiento.html', **data)
    data = {
            "tiempo_transcurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/reconocimiento.html', **data)


@gemini_bp.route('/gemini/audio', methods=['GET', 'POST'])
def gemini_audio():
    if request.method=='POST':
        audio_path = request.form.get('audio_path', '').strip()
        if not audio_path:
            flash("No se especificó la ruta del audio", 'danger')
            return render_template("gemini/audio.html")

        start_time = time.time()
        try:
            respuesta = transcribir_audio_gemini_nuevo(audio_path)
            end_time = time.time()
            tiempo_transcurrido = round(end_time - start_time, 2)
            data = {
                'tiempo_transcurrido': tiempo_transcurrido,
                'respuesta': respuesta
            }
            return render_template("gemini/audio.html", **data)
        except Exception as e:
            flash(f"Error al transcribir el audio: {e}", 'danger')
            return render_template("gemini/audio.html")
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/audio.html', **data)


@gemini_bp.route('/gemini/video', methods=['GET', 'POST'])
def gemini_video():
    if request.method=='POST':
        video_path = request.form.get('video_path', '').strip()
        if not video_path:
            flash("No se especificó la ruta del video", 'danger')
            return render_template("gemini/video.html")

        start_time = time.time()
        try:
            respuesta = analizar_video_gemini_nuevo(video_path)
            end_time = time.time()
            tiempo_transcurrido = round(end_time - start_time, 2)
            data = {
                'tiempo_transcurrido': tiempo_transcurrido,
                'respuesta': respuesta
            }
            return render_template("gemini/video.html", **data)
        except Exception as e:
            flash(f"Error al analizar el video : {e}", 'danger')
            return render_template("gemini/video.html")
    data = {
            "tiempo_trasncurrido": "", 
            "respuesta": ""
        }
    return render_template('gemini/video.html', **data)