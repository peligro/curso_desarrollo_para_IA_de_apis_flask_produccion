from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from integraciones.perplexity_service import get_busqueda_basica_perplexity, get_parametros_investigacion_perplexity, get_investigacion_avanzada_perplexity, get_busqueda_comparativa_perplexity

import time


perplexity_bp = Blueprint('perplexity', __name__)


@perplexity_bp.route('/perplexity')
def perplexity_index():
    return render_template('perplexity/index.html')


@perplexity_bp.route('/perplexity/busqueda', methods=['GET', 'POST'])
def perplexity_busqueda():
    if request.method=='POST':
        prompt = request.form.get('prompt').strip()
        if not prompt:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('perplexity/busqueda.html')
        start_time = time.time()
        respuesta = get_busqueda_basica_perplexity(prompt)
        #print(respuesta)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            "tiempo_transcurrido": tiempo_transcurrido, 
            "respuesta": respuesta
        }
        return render_template('perplexity/busqueda.html', **data)
    return render_template('perplexity/busqueda.html')


@perplexity_bp.route('/perplexity/investigacion-avanzada', methods=['GET', 'POST'])
def perplexity_investigacion_avanzada():
    if request.method=='POST':
        pregunta = request.form.get('pregunta', '').strip()
        dominio = request.form.get('dominio', '').strip()
        fecha = request.form.get('fecha', '').strip()
        idioma = request.form.get('idioma', '').strip()
        enfoque = request.form.get('enfoque', '').strip()
        profundidad = request.form.get('profundidad', '').strip()
        max_tokens = int(request.form.get('max_tokens', 1500))

        if not pregunta:
            flash("La pregunta no puede estar vacía", "danger")
            return render_template('perplexity/investigacion_avanzada.html', parametros=get_parametros_investigacion_perplexity()), HTTPStatus.BAD_REQUEST
        
        parametros_personalizados={'max_tokens': max_tokens}

        if dominio:
            parametros_personalizados['search_domain'] = dominio
        
        if fecha:
            parametros_personalizados['date_range'] = fecha
        
        if idioma:
            parametros_personalizados['language'] = idioma
        
        if enfoque:
            parametros_personalizados['focus'] = enfoque

        if profundidad=='rapida':
            parametros_personalizados["temperature"]= 0.1
        elif profundidad=='profunda':
            parametros_personalizados["temperature"]= 0.4
            parametros_personalizados["max_tokens"]= 2000
        else:
            parametros_personalizados["temperature"]= 0.3

        start_time = time.time()
        resultado = get_investigacion_avanzada_perplexity(pregunta, parametros_personalizados)
        end_time = time.time()
        tiempo_transcurrido = round(end_time - start_time, 2)
        data = {
            'tiempo_transcurrido': tiempo_transcurrido,
            'resultado': resultado,
            'pregunta_original': pregunta,
            'parametros_usados': parametros_personalizados,
            'parametros': get_parametros_investigacion_perplexity()
        }
        return render_template('perplexity/investigacion_avanzada.html', **data)
    data = {
        'tiempo_transcurrido': '',
        'resultado': '',
        'pregunta_original': '',
        'parametros_usados': {},
        'parametros': get_parametros_investigacion_perplexity()
    }
    return render_template('perplexity/investigacion_avanzada.html', **data)


@perplexity_bp.route('/perplexity/busqueda-comparativa', methods=['GET', 'POST'])
def perplexity_busqueda_comparativa():
    if request.method=='POST':
        pregunta = request.form.get('pregunta', '').strip()
        incluir_analisis = request.form.get('incluir_analisis', 'true') == 'true'
        if not pregunta:
            flash("Todos los campos son obligatorios", "danger")
            return render_template('perplexity/busqueda_comparativa.html')
        start_time = time.time()
        resultado_comparativo = get_busqueda_comparativa_perplexity(pregunta, incluir_analisis)
        #print(respuesta)
        end_time = time.time()
        tiempo_total = round(end_time - start_time, 2)
        data = {
            'tiempo_total': tiempo_total,
            'resultado': resultado_comparativo,
            'pregunta_original': pregunta,
            'incluir_analisis': incluir_analisis
        }
        return render_template('perplexity/busqueda_comparativa.html', **data)
    data = {
        'tiempo_total': '',
        'resultado': None,
        'pregunta_original': '',
        'incluir_analisis': True
    }
    return render_template('perplexity/busqueda_comparativa.html', **data)