FROM python:3.7
FROM resin/raspberry-pi-python:3.7-stretch
MAINTAINER Pavel Perestoronin <eigenein@gmail.com>

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8 PYTHONIOENCODING=utf-8

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app
WORKDIR /app
RUN touch db.sqlite3
RUN pip install --no-cache-dir --no-deps .

STOPSIGNAL SIGINT
ENTRYPOINT ["iftttie"]
CMD []
