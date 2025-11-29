from flask import Flask
from dotenv import load_dotenv
import os
#cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)


#rutas
@app.route('/')
def index():
    return "hola desde Flask"


@app.route('/nosotros')
def nosotros():
    return "hola desde nosotros ñandú"


#inicialización de la aplicación
if __name__=='__main__':
    port = int(os.getenv('FLASK_PORT', 8080))
    debug = True if os.getenv('FLASK_DEBUG') == 'True' else False
    app.run(
        debug = debug,
        host='0.0.0.0',
        port=port
    )