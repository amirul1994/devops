#!/bin/bash

docker_version=$(docker -v)

check_docker=$(echo "$docker_version" | awk '{print substr($3, 1, length($3) - 1)}')

echo "$check_docker"
