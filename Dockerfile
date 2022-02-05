FROM python:3.8

COPY requirements.txt app/

WORKDIR app/

RUN pip install -r requirements.txt

COPY src/ /app

ENV PORT 8050

CMD exec flask run

# CMD exec python3 app.py
