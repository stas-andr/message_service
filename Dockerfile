from python:3.8.10

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code