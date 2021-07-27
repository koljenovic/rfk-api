FROM python:3.9-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 8844

ENV RFK_HOME=/usr/src/app/.data/
ENV RFK_TEST_HOME=/usr/src/app/.data/

ENTRYPOINT ["gunicorn"]

CMD ["-w 1", "-b 0.0.0.0:8844", "swagger_server.__main__:app()"]
