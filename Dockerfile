FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install flask

EXPOSE 9999

CMD ["python3", "sample_app.py"]
