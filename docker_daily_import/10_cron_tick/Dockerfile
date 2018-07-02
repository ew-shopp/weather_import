FROM ubuntu:16.04

RUN apt-get update
RUN apt-get --yes install cron
#RUN apt-get --yes install sudo
#RUN adduser --system --uid 1000 --disabled-password --no-create-home  sintef
#RUN echo sintef | passwd sintef --stdin
#RUN usermod -aG sudo sintef

# RUN chmod -R 777 /var
#RUN chmod -R 777 /run

COPY ./bash_scripts /code

ENTRYPOINT ["/code/main.sh"]
