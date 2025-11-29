from flask import Blueprint, render_template


diseno_bp = Blueprint('diseno', __name__)


@diseno_bp.route('/diseno')
def diseno_index():
    data = {
        'title': 'Inicio ñandú',
        'mensaje': 'Hola desde Flask + Jinja2!',
        'html':'texto con <strong>negritas</strong>'
    }
    return render_template('diseno/index.html', **data)


@diseno_bp.route('/diseno/condiciones')
def diseno_condiciones():
    data = {
        'edad': 45
    }
    return render_template('diseno/condiciones.html', **data)


@diseno_bp.route('/diseno/ciclos')
def diseno_ciclos():
    
    return render_template('diseno/ciclos.html')



@diseno_bp.route('/diseno/arreglo')
def diseno_arreglo():
    paises = ["Chile", "México", "Venezuela", "Perú", "Bolivia", "España"]
    #ejemplo2: lista de diccionarios (muy común en apps reales)
    personas = [
        {"nombre": "César Cancino", "edad": 45},
        {"nombre": "Luis Muñoz", "edad": 35},
        {"nombre": "Carla Martínez", "edad": 22},
    ]

    data = {
        'paises': paises,
        'personas': personas
    }
    return render_template('diseno/arreglo.html', **data)