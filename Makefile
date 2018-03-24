#
#	MAKEFILE
#

.PHONY: requirements configure setup start debug_setup debug


# Variables

PYTHON=python
PIP=pip

PROJECT_DIR=douglasdaly


# Recipes

all: requirements start

requirements:
	$(PIP) install -r requirements.txt

configure:
	touch .env
	$(PYTHON) scripts/new_secret_key.py
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py

setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations douglasdaly blog --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.production && \
	$(PYTHON) manage.py loaddata --settings=config.settings.production initial_sitesettings.json initial_blogsettings.json && \
	$(PYTHON) manage.py collectstatic --settings=config.settings.production

start:
	./scripts/start.sh

debug_setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations douglasdaly blog --settings=config.settings.local && \
	$(PYTHON) manage.py migrate --settings=config.settings.local && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.local && \
	$(PYTHON) manage.py loaddata --settings=config.settings.local initial_sitesettings.json initial_blogsettings.json

debug:
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver
