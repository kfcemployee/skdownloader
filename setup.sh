#!/bin/bash

echo "начинается установка..."

pkg install ffmpeg

pip install --upgrade pip
pip install -r requirements.txt

echo "проект настроен. можно начинать работу"
