#!/bin/bash
date=$(date "+%Y-%m-%d %H:%M:%S")
python ./contents_generation.py
git add .
git commit -m "update my notes.($date)"
git push