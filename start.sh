#!/bin/bash
# Start your Flask app with gunicorn using 4 workers on port 3000
gunicorn -w 4 -b 0.0.0.0:3000 main:app
