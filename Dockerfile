FROM python:3.9-slim-bullseye

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . /usr/src/app
RUN chmod +x dbfadapter
RUN chmod +x dbfreindex

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8844

ENV RFK_HOME=/usr/src/app/.data/
ENV RFK_TEST_HOME=/usr/src/app/.data/
ENV PATH="/usr/src/app:${PATH}"

ENTRYPOINT ["gunicorn"]

CMD ["-w 1", "-b 0.0.0.0:8844", "swagger_server.__main__:app()"]
