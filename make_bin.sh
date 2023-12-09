#!/bin/bash
mkdir dist/
python3 -m nuitka main.py --output-dir=build --output-filename=dist/cmdgpt
