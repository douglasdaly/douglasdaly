#
#	MAKEFILE
#

.PHONY: requirements update_requirements configure \
		createsuperuser setup start \
		debug_setup debug debug_createsuperuser \
		debug_start local_start


# Variables

PYTHON=python
PIP=pip
PUR=pur

PROJECT_DIR=douglasdaly


# Recipes

all: requirements start

# - Install Related

update_requirements:
	$(PUR) -r requirements.txt
	$(MAKE) requirements

requirements:
	$(PIP) install -r requirements.txt

configure:
	touch .env
	$(PYTHON) scripts/new_secret_key.py
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py

# - Production Related

createsuperuser:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.production

update:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations douglasdaly blog --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations douglasdaly blog --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py loaddata --settings=config.settings.production initial_sitesettings.json initial_blogsettings.json && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

start:
	./scripts/start.sh

# - Debug Related

debug_createsuperuser:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.local

debug_setup:
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations douglasdaly blog --settings=config.settings.local && \
	$(PYTHON) manage.py migrate --settings=config.settings.local && \
	$(PYTHON) manage.py loaddata --settings=config.settings.local initial_sitesettings.json initial_blogsettings.json && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.local

debug:
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver

debug_start:
	./scripts/debug_start.sh

local:
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver --settings=config.settings.local

local_start:
	./scripts/local_start.sh

# - Misc

clean:
	rm $(PROJECT_DIR)/db.sqlite3
	rm -rf $(PROJECT_DIR)/static/*
	touch $(PROJECT_DIR)/static/.gitkeep
	rm $(PROJECT_DIR)/douglasdaly/migrations/*.py
	touch $(PROJECT_DIR)/douglasdaly/migrations/__init__.py
	rm $(PROJECT_DIR)/blog/migrations/*.py
	touch $(PROJECT_DIR)/blog/migrations/__init__.py
