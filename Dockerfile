FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /Aiohttp

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["python", "server.py"]
