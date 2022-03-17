FROM dbfbuilder:latest as build

FROM python:3.9-slim-bullseye

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

# @TODO: build fresh rfkadapter for dev
# @TODO: test rfkadapter

COPY swagger_server /usr/src/app
COPY requirements.txt /usr/src/app
COPY LICENSE /usr/src/app

RUN rm -rf tmp
COPY --from=build /opt/rfk/dbfreindex .
COPY --from=build /opt/rfk/dbfadapter .
RUN chmod +x dbfadapter
RUN chmod +x dbfreindex

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8844

ENV RFK_HOME=/usr/src/app/.data/
ENV RFK_TEST_HOME=/usr/src/app/.data/
ENV PATH="/usr/src/app:${PATH}"

ENTRYPOINT ["gunicorn"]

CMD ["-w 1", "-b 0.0.0.0:8844", "swagger_server.__main__:app()"]

# @TODO: test rfk-api