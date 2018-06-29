#!/bin/bash
echo "Working dir: $(pwd)"
echo "Docke image name: $1"
read -p "Press any key to start ..."

# Create dir if not present
mkdir -p common_scripts
# Remove old files if present
rm common_scripts/*
#Copy new files
cp ../common/* common_scripts

docker build -t $1 .
docker push $1 

