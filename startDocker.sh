#!/bin/bash

image="py_node:1.0"
docker build -t "$image" app-docker

workingDir="/home/myapp"
docker run -p 8000:8000 -v "$PWD":"$workingDir" -w "$workingDir" -it "$image" /bin/bash
