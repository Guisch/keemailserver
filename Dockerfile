FROM python:3.8

RUN mkdir /keemail

COPY ./requirements.txt /keemail/requirements.txt

WORKDIR /keemail

RUN pip3 install -r requirements.txt

COPY . /keemail

ENV FLASK_APP=run.py

RUN chmod +x /keemail/docker-entrypoint.sh

CMD [ "/bin/bash", "/keemail/docker-entrypoint.sh" ]
