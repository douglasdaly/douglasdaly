#
#	MAKEFILE
#

.PHONY: requirements configure setup start debug_setup debug


# Variables

PYTHON=python
PIP=pip

PROJECT_DIR=douglasdaly


# Recipes

all: configure setup start

requirements:
	$(PIP) install -r requirements.txt

configure: requirements
	touch .env
	$(PYTHON) scripts/new_secret_key.py
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py

setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.production && \
	$(PYTHON) manage.py collectstatic --settings=config.settings.production

start:
	./scripts/start.sh

debug_setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations --settings=config.settings.local && \
	$(PYTHON) manage.py migrate --settings=config.settings.local && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.local

debug:
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver
