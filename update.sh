#!/bin/bash
docker stop $0
docker rm $0
docker pull professorpiggos/hycord:latest
docker run -d -v hycordjson:/app/data --env-file ./.env --restart always professorpiggos/hycord:latest