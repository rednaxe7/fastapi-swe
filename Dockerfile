FROM python:3.10-slim

# Establece el directorio de trabajo en /swe
WORKDIR /swe

# Copia el archivo requirements.txt
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el directorio api dentro de /swe/api
COPY ./api ./api

# Comando para ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]

