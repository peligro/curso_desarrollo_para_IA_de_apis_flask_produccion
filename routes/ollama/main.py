from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
import time
from integraciones.ollama_service import get_consulta_simple_ollama_service, get_consulta_sql_ollama_service, get_traduccion_ollama_service


ollama_bp = Blueprint('ollama', __name__)


@ollama_bp.route('/ollama')
def ollama_index():
    return render_template('ollama/index.html')


@ollama_bp.route('/ollama/prompt',  methods=['GET', 'POST'])
def ollama_prompt():
    if request.method =='POST':
        prompt = request.form.get('prompt').strip()
        
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('ollama/prompt.html'), HTTPStatus.BAD_REQUEST
        
        start_time = time.time()

        #llamada a la API
        respuesta = get_consulta_simple_ollama_service(prompt, "tinyllama")
        #print(respuesta)
        end_time = time.time()

        #calcular el tiempo transcurrido en milisegundos
        tiempo_transcurrido = round(end_time - start_time, 2)
        
        data = {
        "tiempo_transcurrido":tiempo_transcurrido,
        'respuesta':respuesta
        }
        return render_template('ollama/prompt.html', **data)
    data = {
        "tiempo_transcurrido":'',
        'respuesta':''
    }
    return render_template('ollama/prompt.html', **data)



@ollama_bp.route('/ollama/consulta',  methods=['GET', 'POST'])
def ollama_consulta():
    if request.method =='POST':
        prompt = request.form.get('prompt').strip()
        
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('ollama/consulta.html'), HTTPStatus.BAD_REQUEST
        
        start_time = time.time()

        #llamada a la API
        respuesta = get_consulta_sql_ollama_service(prompt, "gemma:2b")
        #print(respuesta)
        end_time = time.time()

        #calcular el tiempo transcurrido en milisegundos
        tiempo_transcurrido = round(end_time - start_time, 2)
        
        data = {
        "tiempo_transcurrido":tiempo_transcurrido,
        'respuesta':respuesta
        }
        return render_template('ollama/consulta.html', **data)
        
        
    data = {
        "tiempo_transcurrido":'',
        'respuesta':''
    }
    return render_template('ollama/consulta.html', **data)



@ollama_bp.route('/ollama/traductor',  methods=['GET', 'POST'])
def ollama_traductor():
    if request.method =='POST':
        prompt = request.form.get('prompt').strip()
        idioma = request.form.get('idioma', '').strip()
        
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('ollama/traductor.html'), HTTPStatus.BAD_REQUEST
        
        start_time = time.time()

        #llamada a la API
        respuesta = get_traduccion_ollama_service(prompt,  idioma, "gemma:2b")
        #print(respuesta)
        end_time = time.time()

        #calcular el tiempo transcurrido en milisegundos
        tiempo_transcurrido = round(end_time - start_time, 2)
        
        data = {
        "tiempo_transcurrido":tiempo_transcurrido,
        'respuesta':respuesta
        }
        return render_template('ollama/traductor.html', **data)
        
        
        
        
    data = {
        "tiempo_transcurrido":'',
        'respuesta':''
    }
    return render_template('ollama/traductor.html', **data)




