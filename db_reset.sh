#!/bin/bash
rm app/testdb.db;
rm -rf migrations/;
python3 manage.py db init;
python3 manage.py db migrate;
python3 manage.py db upgrade;
