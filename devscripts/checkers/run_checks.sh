#!/bin/bash
. .env/bin/activate
#python manage.py jenkins --coverage-rcfile=devscripts/checkers/coveragerc cardgame
pylint --rcfile=devscripts/checkers/pylintrc --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" cardgame | tee reports/pylint.out