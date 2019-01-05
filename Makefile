#
#	MAKEFILE
#

.PHONY: help requirements update_requirements configure \
		createsuperuser setup start \
		debug_setup debug debug_createsuperuser \
		debug_start local_start

.DEFAULT_GOAL := help

# Variables

PYTHON=python
PIP=pip
PUR=pur

PROJECT_DIR=douglasdaly

DJANGO_APPS=douglasdaly blog

# Recipes

help: ## Prints help for this Makefile
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ''

all: requirements start ## Installs requirements and starts server

# - Install Related

update_requirements: ## Updates requirements.txt file from environment
	$(PUR) -r requirements.txt
	$(MAKE) requirements

requirements: ## Installs project's requirements.txt to environment
	$(PIP) install -r requirements.txt

configure: ## Initial configuration for the application
	touch .env
	$(PYTHON) scripts/new_secret_key.py
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py

# - Production Related

createsuperuser: ## Creates a superuser for production
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.production

update: ## Updates the app (migrations and collect static files)
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

setup: ## Initial setup for the app (migrations, load data, collect static)
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py loaddata --settings=config.settings.production initial_sitesettings.json initial_blogsettings.json && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

start: ## Starts the server process
	./scripts/start.sh

# - Debug Related

debug_createsuperuser: ## Creates a superuser for debug
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.local

debug_update: ## Updates the app for debugging
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.local && \
	$(PYTHON) manage.py migrate --settings=config.settings.local && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.local

debug_setup: ## Initial setup of the app for debugging
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.local && \
	$(PYTHON) manage.py migrate --settings=config.settings.local && \
	$(PYTHON) manage.py loaddata --settings=config.settings.local initial_sitesettings.json initial_blogsettings.json && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.local

debug: ## Run the debug django server
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver

debug_start: ## Starts the gunicorn server with debug settings
	./scripts/debug_start.sh

local: ## Starts the django server with local settings
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver --settings=config.settings.local

local_start: ## Starts the gunicorn server with local settings
	./scripts/local_start.sh

# - Misc

clean: ## Cleans the debug project (database, static)
	rm $(PROJECT_DIR)/db.sqlite3 || true
	rm -rf $(PROJECT_DIR)/static/* || true
	touch $(PROJECT_DIR)/static/.gitkeep
