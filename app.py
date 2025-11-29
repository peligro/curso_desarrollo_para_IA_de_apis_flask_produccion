from flask import Flask, render_template
from http import HTTPStatus
from dotenv import load_dotenv
import os
from flask_wtf.csrf import CSRFProtect
from datetime import datetime

#cargar variables de entorno desde el archivo .env
load_dotenv()


#referenciamos blueprints
from routes.main.main import main_bp
from routes.ejemplo.ejemplo import ejemplo_bp
from routes.parametros.main import parametros_bp
from routes.diseno.main import diseno_bp
from routes.health.main import health_bp
from routes.formularios.main import formularios_bp
from routes.bucket_s3.main import bucket_s3_bp
from routes.ollama.main import ollama_bp
from routes.mistral.main import mistral_bp
from routes.gemini.main import gemini_bp
from routes.claude.main import claude_bp
from routes.deepseek.main import deepseek_bp
from routes.openai.main import openai_bp
from routes.perplexity.main import perplexity_bp
from routes.rag.main import rag_bp


def create_app():
    app = Flask(__name__)


    #configuramos el secret key
    app.secret_key = os.getenv('FLASK_KEY')


    #activar protección CSRF
    csrf = CSRFProtect(app)


    #registrar blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(ejemplo_bp, url_prefix="/api")
    app.register_blueprint(parametros_bp)
    app.register_blueprint(diseno_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(formularios_bp)
    app.register_blueprint(bucket_s3_bp)
    app.register_blueprint(ollama_bp)
    app.register_blueprint(mistral_bp)
    app.register_blueprint(gemini_bp)
    app.register_blueprint(claude_bp)
    app.register_blueprint(deepseek_bp)
    app.register_blueprint(openai_bp)
    app.register_blueprint(perplexity_bp)
    app.register_blueprint(rag_bp)
    
    
    #manejador personalizar para error 404
    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return render_template('errors/404.html'), HTTPStatus.NOT_FOUND


    #manejador personalizar para error 500
    @app.errorhandler(Exception)
    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(error):
        #si estás en modo debug, muestra el error real
        if app.debug:
            error=f"Error:{error}"
        else:
            error=''
        return render_template('errors/500.html', **{'error': error}), HTTPStatus.INTERNAL_SERVER_ERROR
    
    
    # Registrar el filtro datetimeformat
    @app.template_filter('datetimeformat')
    def datetimeformat(value, format='%H:%M:%S'):
        """
        Filtro para formatear timestamps en templates
        """
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(value).strftime(format)
            except (ValueError, OSError):
                return value
        elif isinstance(value, datetime):
            return value.strftime(format)
        return value


    return app


#inicialización de la aplicación
if __name__=='__main__':
    app = create_app()
    port = int(os.getenv('FLASK_PORT', 8080))
    debug = True if os.getenv('FLASK_DEBUG') == 'True' else False
    app.run(
        debug = debug,
        host='0.0.0.0',
        port=port
    )