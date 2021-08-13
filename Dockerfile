FROM python:3.9.6

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -yqq --no-install-recommends cron

COPY app/ /back-end-challenge-2021/app

COPY cron/ /cron

RUN crontab /cron/cronfile && chmod u+x /cron/apigetuser.sh

WORKDIR /back-end-challenge-2021

CMD cron && uvicorn app.main:app --host 0.0.0.0 --port 80