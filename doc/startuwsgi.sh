#! /bin/bash
uwsgi --plugin python3 --http-socket :9090 --callable app --wsgi-file app.py -H /home/gerd/python/env/ --master --processes 2 --threads 2 &

