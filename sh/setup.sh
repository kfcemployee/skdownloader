#!/bin/bash

echo "начинается установка..."

pkg install ffmpeg
which ffmpeg > config.txt

pip install --upgrade pip
pip install -r requirements.txt

echo "проект настроен. можно начинать работу"
