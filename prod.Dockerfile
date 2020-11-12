FROM python:3.8

COPY requirements.txt app/

COPY src/web_app/ app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xvzf redis-stable.tar.gz
RUN cd redis-stable
RUN make
RUN redis-server

ENV PORT 8050

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 app:server
