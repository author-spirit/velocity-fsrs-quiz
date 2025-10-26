#!/bin/bash

mkdir -p backend/
cd backend

for dir in core db models schemas api services utils tests
do
  mkdir -p "$dir"
done
touch backend/main.py backend/README.md backend/.env