from flask import Blueprint, request, abort
from http import HTTPStatus

parametros_bp = Blueprint('parametros', __name__)


@parametros_bp.route('/parametros/<int:id>/<slug>')
def parametros_index(id, slug):
    if id<=0 or not slug.strip():
        return "Recurso no encontrado", HTTPStatus.NOT_FOUND

    return f"id={id} | slug={slug}"



@parametros_bp.route('/parametros-querystring')
def parametros_querystring():
    id_str = request.args.get('id')
    slug = request.args.get('slug')

    if id_str is None or slug is None:
        abort(HTTPStatus.NOT_FOUND)
        #return "Recurso no encontrado", HTTPStatus.NOT_FOUND
    
    #convertir el id a entero (con manejo de error)
    try:
        id = int(id_str)
    except ValueError:
        return "El parámetro 'id' debe ser un número entero", HTTPStatus.BAD_REQUEST

    
    if id<=0 or not slug.strip():
        return "Recurso no encontrado", HTTPStatus.NOT_FOUND
    
    return f"id={id} | slug={slug}"