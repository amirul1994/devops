# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app/django_backend

# Install curl, gnupg, and wget, and import the MySQL GPG key
RUN apt-get update && apt-get install -y curl gnupg wget && \
    curl -fsSL https://repo.mysql.com/RPM-GPG-KEY-mysql-2022 | apt-key add -

# Add the MySQL APT repository
RUN echo "deb http://repo.mysql.com/apt/debian/ buster mysql-8.0" | tee /etc/apt/sources.list.d/mysql.list

# Import the MySQL public key
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C

# Install the mysql-client package and netcat
RUN apt-get update && apt-get install -y mysql-client netcat-openbsd

# Install wget
#RUN apt-get update && apt-get install -y wget

# Install dockerize
RUN wget -q -O /usr/local/bin/dockerize https://github.com/jwilder/dockerize/releases/download/v0.7.0/dockerize-linux-amd64-v0.7.0.tar.gz \
    && tar -C /usr/local/bin -xzvf /usr/local/bin/dockerize/dockerize-linux-amd64-v0.7.0.tar.gz

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
