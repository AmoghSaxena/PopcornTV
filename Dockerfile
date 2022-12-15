FROM python:3.10-slim

RUN apt-get update && apt install -y command-not-found
RUN apt-file update
RUN update-command-not-found

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -yq tzdata && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -yq --no-install-recommends \
    openssh-server screen libsasl2-dev python-dev libldap2-dev libssl-dev python3-dev ldap-utils tox lcov valgrind

COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt 


RUN mkdir /APS
RUN mkdir /etc/ldap
WORKDIR /APS

COPY ./compose/ldap.conf /etc/ldap/ldap.conf

COPY ./compose/migrate /migrate
RUN sed -i 's/\r$//g' /migrate
RUN chmod +x /migrate

COPY ./compose/startserver /startserver
RUN sed -i 's/\r$//g' /startserver
RUN chmod +x /startserver

COPY ./compose/createadmin /createadmin
RUN sed -i 's/\r$//g' /createadmin
RUN chmod +x /createadmin

COPY ./compose/install /install
RUN sed -i 's/\r$//g' /install
RUN chmod +x /install


EXPOSE 5085