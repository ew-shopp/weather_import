FROM ubuntu:16.04

RUN apt-get update
RUN apt-get --yes install cron
RUN adduser --system --uid 1000 --disabled-password --no-create-home  sintef

COPY ./bash_scripts /code

ENTRYPOINT ["/code/main.sh"]
