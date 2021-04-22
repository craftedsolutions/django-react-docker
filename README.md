## Sample django app that serves up a react app

## Prerequisites

- Docker can be installed from [here](https://docs.docker.com/get-docker/).

## To start the app in a docker container

From the project root directory run `./startDocker.sh`

This script should will do the following things:

- Build a docker image with python 3, node 15, and django installed named ``
- Start the container with the current project attached as a volume
- Start up bash in the container

From the container bash:

- `cd /home/myapp/mysite && ./startApp.sh`

The application should be accessible [here](http://localhost:8000/admin/).

## Start up additional bash session in the container

- Run `docker container ls` and copy either the container id or name for image `py_node:1.0`
- Run `docker container exec -it <id or name> /bin/bash`

## React app

It may be helpful to start a second bash session in the container.

In the container bash:

- `cd /home/myapp/client/login_client`
- `npm install`
- `npm run build`

After these steps are complete, if the django app is running, the react app should be accessible [here](http://localhost:8000/app/index.html).