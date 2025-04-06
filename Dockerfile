FROM python:3.10-slim

WORKDIR /swe

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src

COPY ./tests ./tests

# Agrega /swe al PYTHONPATH para que 'api' sea un módulo importable
#ENV PYTHONPATH="${PYTHONPATH}:/swe"
ENV PYTHONPATH="/swe/src"

ENV DATABASE_URL="mysql+pymysql://root:oyERwpNKvpqDFRVxwQaQmXVjehxzcDnC@shuttle.proxy.rlwy.net:40326/railway"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
