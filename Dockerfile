FROM python:3.9.6

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY app/ /backend-challenge-2021/app

ENV PYTHONPATH=/backend-challenge-2021

RUN apt-get update && apt-get install -y cron

COPY cron/cronfile ./cronfile

RUN crontab cronfile

WORKDIR /backend-challenge-2021

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]