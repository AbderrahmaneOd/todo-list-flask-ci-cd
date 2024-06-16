FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python" , "app.py"]