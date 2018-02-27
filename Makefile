#
#	MAKEFILE
#

.PHONY: requirements initialize setup

# Variables
PYTHON=python
PIP=pip


# Recipes

requirements:
	$(PIP) install -r requirements.txt

initialize:
	touch .env
	$(PYTHON) scripts/new_secret_key.py

setup:
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py
	