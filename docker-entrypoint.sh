#!/bin/sh

cd /keemail



flask db init
flask db migrate
flask db upgrade

python run.py
