from flask import Flask


app = Flask(__name__)


#rutas

#inicialización de la aplicación
if __name__=='__main__':
    app.run(
        debug = True,
        host='0.0.0.0',
        port=8080
    )