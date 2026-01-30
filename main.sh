#!/usr/bin/env bash
#
python3 -m src.main
#cd public
cd docs && python3 -m http.server 8888
