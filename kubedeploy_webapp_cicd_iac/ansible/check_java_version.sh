#!/bin/bash

java_version=$(sudo apt list --installed 2> /dev/null | grep -E '^openjdk|^OpenJdk')

if [[ -n "$java_version" ]]; then
    java_version=$(java --version | awk 'NR==1 && (/^openjdk/ || /^OpenJdk/)')
    echo $java_version
fi
