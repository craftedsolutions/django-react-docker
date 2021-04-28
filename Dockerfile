FROM python:3.9.4
ENV PYTHONUNBUFFERED=1

WORKDIR /setup
COPY ./mysite/requirements.txt /setup/

RUN pip install -r requirements.txt
RUN curl -fsSL https://deb.nodesource.com/setup_15.x | bash -
RUN apt-get install -y nodejs

