#!/bin/sh

cd /app/docs/build/ 
rm -rf ./html/*
rm -rf ./html/doctrees/*
make html
