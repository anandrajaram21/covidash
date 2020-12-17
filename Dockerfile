FROM python:3.8

COPY requirements.txt app/

COPY src/ app/

WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install tensorflow

ENV PORT 8050

CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 app:server
