#!/bin/bash
set -o errexit

source insta_venv/bin/activate

# Run first iteration
echo "--- 0 to 8 ---"
python agds_update.py 0 9
echo "--- 9 to 17 ---"
python agds_update.py 9 18
echo "--- 18 to 26 ---"
python agds_update.py 18 27
echo "--- 27 to 34 ---"
python agds_update.py 27 35
echo "--- 35 to 37 ---"
python agds_update.py 35 37

figlet "SUCCESS"
