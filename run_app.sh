#!/bin/bash
echo iniciando MinTICstagram
cd /home/ubuntu/MinTICstagram
source env/bin/activate
gunicorn --workers=5 -b 0.0.0.0:443 --certfile=micertificado.pem --keyfile=llaveprivada.pem wsgi:application