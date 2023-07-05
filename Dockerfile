FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --update alpine-sdk
RUN apk add --update --no-cache postgresql-client jpeg-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \ 
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev build-base python3-dev libffi-dev openssl-dev cargo

RUN apk add --no-cache bash dcron

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

COPY . /app/

# 添加一个cron job，定时运行backup.py，每天凌晨1点执行
RUN (echo "0 1 * * * python /app/backup.py") | crontab -
# 启动cron守护进程
CMD ["cron", "-f"]