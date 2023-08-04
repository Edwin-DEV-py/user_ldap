FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev
RUN pip install -r requirements.txt
COPY . /app