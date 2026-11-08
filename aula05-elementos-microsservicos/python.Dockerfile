# Imagem única para os serviços Python (só biblioteca padrão, sem pip install).
FROM python:3.12-slim
WORKDIR /app
COPY python/ /app/
ENV PYTHONUNBUFFERED=1
# O comando de cada serviço é definido no docker-compose.yml
