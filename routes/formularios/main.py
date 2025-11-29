from flask import Blueprint, render_template, request, flash
from http import HTTPStatus
from utilidades.utilidades import EMAIL_REGEX


formularios_bp = Blueprint('formularios', __name__)


@formularios_bp.route('/formularios-simple', methods=['GET'])
def formularios_simple():
    return render_template('formularios/simple.html')


@formularios_bp.route('/formularios-simple', methods=['POST'])
def formularios_simple_post():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()

    #validamos campos obligatorios
    if not nombre or not correo or not telefono:
        flash("Todos los campos son obligatorios", "danger")
        return render_template('formularios/simple.html'), HTTPStatus.BAD_REQUEST
    
    
    #validación para el correo
    if not EMAIL_REGEX.match(correo):
        flash("Por favor, ingresa un correo electrónico válido", "danger")
        return render_template('formularios/simple.html'), HTTPStatus.BAD_REQUEST
    
    
    #validar teléfono
    if  not telefono.replace('+', '').replace('-', '').replace(' ', '').isdigit():
        flash("El teléfono solo debe contener números, +, - o espacios", "danger")
        return render_template('formularios/simple.html'), HTTPStatus.BAD_REQUEST
    
    
    if len(telefono.replace('+', '').replace('-', '').replace(' ', '')) < 10:
        flash("El teléfono debe tener al menos 10 dígitos", "danger")
        return render_template('formularios/simple.html'), HTTPStatus.BAD_REQUEST

    
    return f"nombre={nombre} | correo={correo} | teléfono={telefono}"



"""
def formularios_simple_post():
    nombre = request.form.get('nombre', '').strip()
    correo = request.form.get('correo', '').strip()
    telefono = request.form.get('telefono', '').strip()
    return f"nombre={nombre} | correo={correo} | teléfono={telefono}"
"""