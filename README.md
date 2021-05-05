## Sample django app that serves up a react app

## Prerequisites

- Docker can be installed from [here](https://docs.docker.com/get-docker/).

on mac installing docker also installs `docker-compose`

## To start the docker containers

From the project root directory run `docker-compose up` which will start two docker containers, one for the web app and one for postgres.

## Start the web app

After starting the containers the web app will not be running (since this setup is primarily meant for development), to keep the web container from terminating, there a script running that loops every 10 seconds or so.

To start the web app:

- Start a bash session in the web container
  - Run `docker container ls` and copy either the container id or name for image `django-react-docker_web...`
  - Run `docker container exec -it <id or name> /bin/bash`
- In the container bash run `./startApp.sh` and the app should be accessible [here](http://localhost:8000/admin/)

## Start up additional bash session in the container

- Run `docker container ls` and copy either the container id or name for image `django-react-docker_web...`
- Run `docker container exec -it <id or name> /bin/bash`

## React app

It may be helpful to start a second bash session in the container.

In the container bash:

- `cd /home/myapp/client/login_client`
- `npm install`
- `npm run build`

After these steps are complete, if the django app is running, the react app should be accessible [here](http://localhost:8000/app/index.html).