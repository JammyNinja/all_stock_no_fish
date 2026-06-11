FROM python:3.12-slim-bookworm

WORKDIR /backend_app
ENV PORT=8080

COPY src/ ./src/

# Setup + Install Poetry
RUN pip install --no-cache-dir poetry==2.4.1
COPY pyproject.toml poetry.lock ./  

RUN poetry config virtualenvs.create false

#no user prompt allowed, no fancy formatted outputs (ansi)
RUN poetry install --without frontend --no-interaction --no-ansi


COPY backend ./


CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
