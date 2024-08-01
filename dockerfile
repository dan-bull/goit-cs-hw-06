FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
