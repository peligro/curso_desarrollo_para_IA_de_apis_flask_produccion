#!/bin/bash

# Script de despliegue para CI/CD
set -e

echo "🔨 Iniciando despliegue del proyecto Flask..."

# Construir las imágenes
echo "📦 Construyendo imágenes Docker..."
docker-compose build

# Detener servicios existentes
echo "🛑 Deteniendo servicios anteriores... "
docker-compose down

# Iniciar servicios
echo "🚀 Iniciando servicios..."
docker-compose up -d

# Verificar que los servicios estén corriendo
echo "🔍 Verificando estado de los servicios..."
docker-compose ps


echo "✅ Despliegue completado exitosamente!"