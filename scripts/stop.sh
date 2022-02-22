#!/bin/bash
app_path=$(dirname "$PWD")
cd $app_path
sudo kill -9 $(lsof -i:9104 -t)
echo "stop finish"
