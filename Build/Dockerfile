FROM python:3.6-slim

EXPOSE 5000

RUN pip install flask flask-restful cerberus pymongo

COPY . /home/src

WORKDIR /home/src

CMD ["python", "Routes.py"]