FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 5000
# docker-compose.yml overrides this with --debug for development.
CMD ["flask", "--app", "src/jot/app", "run", "--host", "0.0.0.0", "--port", "5000"]
