FROM python:3.10-slim

WORKDIR /swe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./api ./api

# Agrega /swe al PYTHONPATH para que 'api' sea un módulo importable
ENV PYTHONPATH="${PYTHONPATH}:/swe"

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
