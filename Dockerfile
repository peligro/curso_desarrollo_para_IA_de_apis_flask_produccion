FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear archivo wsgi.py si no existe
RUN if [ ! -f wsgi.py ]; then \
    echo 'from app import create_app\n\napp = create_app()\n\nif __name__ == "__main__":\n    app.run()' > wsgi.py; \
    fi

# Asegurar que los archivos estáticos tengan permisos correctos
RUN chmod -R a+r /app/static/ 2>/dev/null || true

EXPOSE 5000
ENV FLASK_ENV=production

# Comando con prefijo estático explícito
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]