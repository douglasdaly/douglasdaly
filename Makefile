#
#	MAKEFILE
#

.phony: requirements initialize

# Variables
PYTHON=python
PIP=pip


# Recipes

requirements:
	$(PIP) install -r requirements.txt

initialize:
	touch .env

