#!/bin/bash
sleep 3 #waiting for database container to be ready
alembic upgrade head > log1.txt 2>&1
uvicorn app.main:app --host 0.0.0.0 --port 8000 > log2.txt 2>&1