In this comprehensive guideline, I'll walk through the process of deploying a full-stack application using Docker Compose orchestration. The stack consists of React for the frontend, Django for the backend, MySQL for the database, and Nginx as the load balancer. This article clearly depicts, how to containerize each component of the full-stack application and orchestrate them using Docker Compose.

Key Components:

React
Django
REST API
MySQL
Nginx

Backend 1 ( and backend 2) Dockerfile

FROM python:3.11-slim-buster
‘FROM’ will pull the ‘python:3.11-slim-buster’ image from the docker hub. This image is used as the base image to build the backend-1 app.

WORKDIR /app/django_backend
‘WORKDIR’ will create the directory and change the directory to the mentioned one inside the docker container (here to /app/django_backend directory). If the directory is present, it will only change the directory.

RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 | apt-key add -
‘RUN’ is used to install packages during the build of the docker container.

‘gnupg’ is used to import the MySQL gpg key.

‘curl’ is used to interact with API, download files, browse and test HTTP requests.

-f ( or ‘—fail’): fail silently without outputting an error message if the downloaded file has a zero size.

-s ( or ‘—silent’): Silent and not output anything.

-L ( or ‘—location’): tells to follow redirects. If the server responds with a redirect (i.e. a 3xx  HTTP status code), ‘curl’ will automatically follow the redirect and download the file from the new location.

‘apt-key add –’: is used to add a new key to the APT keyring, which is a collection of public keys that are used to verify the authenticity of packages that are downloaded from APT repositories.

‘-’: this option is used with the ‘apt-key add’ command, which tells it to read the key from standard input (from the pipe (|) i.e. from the ‘curl’ command that precedes it.)

The purpose of adding the MySQL gpg key to the apt keyring is to ensure that the packages that are downloaded from the MySQL apt repository are authentic and have not been tampered with.

RUN echo "deb http://repo.mysql.com/apt/debian/ buster mysql-8.0" | tee /etc/apt/sources.list.d/mysql.list
‘deb’: This keyword indicates that the repository contains precompiled binary packages. Debian repositories can either be binary (‘deb’) or source (‘deb-src’).

‘http://repo.mysql.com/apt/debian/ buster mysql-8.0’: This is the URL of the repository where the package manager will look for the packages.

‘buster’: codename for the Debian 10 release.

‘mysql-8.0’: - This specifies the specific component of the repository. In this case, it is mysql-8.0 packages within the repository.

So to sum up, this line adds a repository from which the package manager can retrieve mysql-8.0 packages.

‘tee’: It reads from the standard input and writes to the standard output and one or more files simultaneously.

‘| tee ….. /mysql.list’: This part of the command takes the output of the previous ‘echo’ command and writes it to the file ‘/etc/apt/sources.list.d/mysql.list’.

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C
‘apt-key’: This tool is used to manage the list of keys used by ‘apt’ to authenticate packages.

‘adv’: This option allows more advanced key management, providing direct access to the key server.

‘—keyserver keyserver.ubuntu.com’ – This specifies the keyserver from which to retrieve the key. In this case, it is the Ubuntu keyserver.

‘--recv-keys B7B3B788A8D3785C’: This option tells the ‘apt-key’ to retrieve the key with the specified ID from the keyserver.

 So the command will add gpg key with ID ‘B7B3B788A8D3785C’ from the specified server.

RUN wget -q -O /usr/local/bin/dockerize https://github.com/jwilder/dockerize/releases/download/v0.7.0/dockerize-linux-amd64-v0.7.0.tar.gz \
    && tar -C /usr/local/bin -xzvf /usr/local/bin/dockerize
‘wget’: This tool is used to download files from a web address.

‘-q’ : (quiet) – This option makes ‘wget’ operate in quiet mode, which means it suppresses output except for error messages.

‘-O’: This option specifies the filename or path where the downloaded content will be saved. If the directory is not present, it will be created.

‘tar’: This tool is used to archive to ‘tar’ and extract files from a tar archive.

‘-C’: This option tells ‘tar’ to change the specified directory.

‘-x’: extract

‘-z’: allows to filter the archive through gzip, Here, it tells to extract ‘.tar.gz’ file.

‘-f’: specifies the name and location of the tar archive.

So, the complete command downloads the ‘dockerize’ tool from github, saves it ‘/usr/local/bin/dockerize’, and then extracts its content to ‘usr/local/bin’.

‘python -m venv env’: create a virtual environment in Python named ‘env’.

COPY ./docker_backend/requirements.txt .
‘COPY’: This is dockerfile instruction to copy from the host’s directory to the docker container’s directory.

‘env/bin/activate’: activate the virtual environment ‘env’ on linux.

ENV PYTHONPATH $PYTHONPATH:/app/django_backend/info
‘ENV’: This is a dockerfile instruction used to set environment variables within a docker container.

‘PYTHONPATH’: This is the name of the environment variable being set.

‘$PYTHONPATH:/app/django_backend/info’: This value sets the ‘PYTHONPATH’ variable. It includes the existing value of ‘PYTHOnPATH’ (if any) and appends ‘:/app/django_backend/info’ to it.

This command is used to ensure that Python can find modules located in the direction ‘/app/django_backend/info’ in addition to the default locations.

dockerize -wait tcp://db-server:3306 -timeout 360s
‘dockerize’: This command is used in docker environments to ensure that a container depending on another container waits until the dependee is ready before starting its operation. Here, this docker container will stop its further operation until it establishes a connection to the ‘db-server’ within 360 seconds.

In Django migration, if the database is not found, it halts the migration operation. This indirectly ensures the ‘db-server’ container will be built and run before the backend server.

CMD ["/app/django_backend/startup.sh"]
‘CMD’: This instruction in a dockerfile is used to specify the default command or executable that should be run when a container is started from the image. Here, it will execute the commands inside the ‘startup.sh’ file.

The complete dockerfile is as follows:

FROM python:3.11-slim-buster

# Set the working directory to /app/django_backend
WORKDIR /app/django_backend

# Install curl, gnupg, and import the MySQL GPG key
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 | apt-key add -

# Add the MySQL APT repository
RUN echo "deb http://repo.mysql.com/apt/debian/ buster mysql-8.0" | tee /etc/apt/sources.list.d/mysql.list

# Import the MySQL public key
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C


RUN apt-get update && apt-get install -y mysql-client netcat-openbsd


RUN apt-get update && apt-get install -y wget

# Install dockerize
RUN wget -q -O /usr/local/bin/dockerize https://github.com/jwilder/dockerize/releases/download/v0.7.0/dockerize-linux-amd64-v0.7.0.tar.gz \
    && tar -C /usr/local/bin -xzvf /usr/local/bin/dockerize

COPY ./docker_backend/requirements.txt .

RUN python -m venv env && \
    . env/bin/activate && \
    apt update && \
    apt install -y \
        gcc \
        libffi-dev \
        libssl-dev \
        python3-dev \
        python3-pip \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config && \
    chown -R $USER:$USER /app/django_backend/env/ && \
    chmod -R +x /app/django_backend/env/bin/ && \
    env/bin/pip install --upgrade pip && \
    env/bin/pip install django-debug-toolbar && \
    env/bin/pip install mysqlclient==2.2.4 && \
    env/bin/pip install -r requirements.txt

COPY ./docker_backend .

# Add the info directory to the PYTHONPATH
ENV PYTHONPATH $PYTHONPATH:/app/django_backend/info

# Create the startup.sh script
RUN echo '#!/bin/bash' > /app/django_backend/startup.sh && \
    echo 'dockerize -wait tcp://db-server:3306 -timeout 360s' >> /app/django_backend/startup.sh && \
    echo '. /app/django_backend/env/bin/activate' >> /app/django_backend/startup.sh && \
    echo 'env/bin/python manage.py makemigrations' >> /app/django_backend/startup.sh && \
    echo 'env/bin/python manage.py run_migrations_safely' >> /app/django_backend/startup.sh && \
    echo 'exec env/bin/python manage.py runserver 0.0.0.0:8000' >> /app/django_backend/startup.sh

# Set the executable bit on the startup.sh script
RUN chmod +x /app/django_backend/startup.sh

# Start the Django development server using the startup.sh script
CMD ["/app/django_backend/startup.sh"]
[For the backend server 2 the port is 9000 to run the server]

Frontend Dockerfile

FROM node:18

WORKDIR /app 

COPY ./package.json .

COPY ./package-lock.json .

RUN npm install 

COPY . .

RUN npm run build

CMD ["npm", "start"]
Install packages before copying all other elements, it will use the cache in docker. Otherwise, every time when the image is built, it will install packages.

Load Balancer (Nginx) Dockerfile

FROM nginx:stable-alpine

COPY nginx.conf /etc/nginx/nginx.conf

# Create a new user and group for the web server to run as
RUN adduser -D -H -u 1000 -s /sbin/nologin -G www-data www-data

CMD ["nginx", "-g", "daemon off;"]
‘CMD ["nginx", "-g", "daemon off;"]’: Not to run nginx in the background. It is done to ensure that the container doesn’t exit immediately after starting nginx.

Database Dockerfile

The ‘init_db.sql’ file

DROP DATABASE IF EXISTS userdb; 

CREATE DATABASE userdb;

CREATE USER IF NOT EXISTS 'amirul'@'%' IDENTIFIED WITH mysql_native_password BY '12345';

GRANT ALL PRIVILEGES ON userdb.* TO 'amirul'@'%';

FLUSH PRIVILEGES;

USE userdb;

CREATE TABLE IF NOT EXISTS userinfo (id BIGINT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NULL,
age INT(4) NULL, profession VARCHAR(50) NULL, address VARCHAR(100) NULL, password VARCHAR(128) NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
The database dockerfile -

FROM mysql:8.0

COPY ./init_db.sql /tmp

CMD ["mysqld", "--init-file=/tmp/init_db.sql", "--bind-address=0.0.0.0"]
Environment (.env) File

MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=userdb
Environment variables can be passed directly in the docker-compose file. Sensitive information should be in a separate ‘.env’ file.

Docker Compose

Docker compose is a tool for orchestrating docker container deployment. In ‘docker-compose.yml’ file, multiple containers, and their configurations are mentioned to build the desired containers.

Article content


Article content
‘version 3’: This specifies the docker-compose file format, the file format version is ‘3’ here.

‘networks’: network section of the docker-compose file.

‘docker-project-network’: name of the docker network being defined.

‘driver’: mention the network driver, the default driver is the bridge. A bridge driver is used to isolate containers in a private network. Other types of drivers are host, none.

‘ipam’: IP address management for the network.

‘config’: ipam configuration.

‘subnet’: this specifies a subnet for this docker network.

Docker-compose creates a new network automatically during the build process from the docker-compose.yml file. ‘ipam’ is used here to manually set the network mentioning the desired subnet.

Other docker-compose configurations are mentioned below.

‘services’: This section is used to define services in the docker-compose file.

Under ‘services’ the service name is mentioned. E.g. db, backend-service-1, etc.

‘container_name’: This specifies the name of the container that will be created for the service.

‘volumes’: The volume that will be mounted in the container.

‘./docker_project_volume:/var/lib/mysql’

The left side of the ‘:’ is the location of the host where the docker volume will be mounted. On the right side of the ‘:’, the location of the docker container will be mounted. If the docker container is stopped or deleted, the data in the volume mount will still be available and can be accessed by a new container.

‘build’: specifies the build option for the service.

‘context’: This specifies the build context, which is the directory on the host machine that contains the dockerfile and other necessary files and directories.

‘dockerfile’: This specifies the name of the dockerfile. 

‘environment’: This section specifies the environment variables for the docker container. Environment variables will be passed during the creation of the particular docker container.

‘- MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}’

On the left side, the name of the variable and the right side is the value. ‘${…}’ indicates the value will be taken from ‘.env’ file.

‘-’ indicates a new element in the list data. If ‘-’ is not mentioned, that means the configuration is in key-value format.

‘ports’: port mapping for the container with the host.

"3306:3306"

The left side of the ‘:’ is the host port and the right side is the docker container’s port.

‘networks’: mentioning which docker network the container will use.

‘ipv4_address’: This section is used to static ip address configuration for the docker container.

‘depends_on’: specifies the dependencies between services. It defines the order, in which the services should be started or stopped. This option doesn’t guarantee that the dependent service will be fully up and running before the service it depends on starts.

The complete docker-compose.yml file

version: '3'

networks:
  docker-project-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  db:
    container_name: "db-server"
    volumes:
      - ./docker_project_volume:/var/lib/mysql
    build: 
      context: ./db/.
      dockerfile: Dockerfile
    environment:
      - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
      - MYSQL_DATABASE=${MYSQL_DATABASE}
      - MYSQL_ALLOW_EMPTY_PASSWORD=no
      - MYSQL_AUTH_PLUGIN=mysql_native_password
      - MYSQL_HOST=db-server
    ports:
      - "3306:3306"
    networks:
      docker-project-network:
        ipv4_address: 172.20.0.10
    
    
  backend-service-1:
    container_name: "backend-server-1"
    build: 
      context: ./backend1/. 
      dockerfile: Dockerfile 
    ports:
      - "8000:8000"
    networks:
      docker-project-network:
        ipv4_address: 172.20.0.11
    depends_on:
      - db
  
  backend-service-2:
    container_name: "backend-server-2"
    build:
      context: ./backend2/.
      dockerfile: Dockerfile
    ports: 
      - "9000:9000"
    networks:
      docker-project-network:
        ipv4_address: 172.20.0.12
    depends_on:
      - db
  
  nginx:
    container_name: "load-balancer-server"
    build:
      context: ./nginx/conf/.
      dockerfile: Dockerfile
    ports:
      - "80:80"
    networks:
      docker-project-network:
        ipv4_address: 172.20.0.13
    depends_on:
      - backend-service-1
      - backend-service-2
      
  frontend-service: 
    container_name: "frontend-server"
    build:
      context: ./frontend/.
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    networks:
      docker-project-network:
        ipv4_address: 172.20.0.14
‘sudo docker compose up’

The above-mentioned command will build and run docker containers by using docker-compose.yml file.

Article content
Article content
Article content
Article content
Article content
Now, browse the frontend server ip address.

Article content
It brings up the login page. Clicking signup will bring the signup.

Article content
Click  ‘Sign Up’.

Article content
The signup is successful.

As per the code, the login and search will show user info.

Article content


Article content
As, I have configured nginx as the load balancer, for login and searching different backend server responses.

Article content
To make the docker containers accessible in the local network, I have used the docker host's ip address. To use only inside the localhost, use the load balancer's ip address in the frontend (App.js) and backend server 1 and backend server 2 ip addresses in the load balancer's configuration(nginx.conf).
