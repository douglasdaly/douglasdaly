#
#	MAKEFILE
#

#
#	Configuration
#

PYTHON=python
PKG_MGR=pipenv

PROJECT_DIR=douglasdaly

DJANGO_APPS=douglasdaly blog assets
FIXTURES = initial_sitesettings.json initial_blogsettings.json initial_assetsettings.json


#
#	Setup
#

ifeq ($(PKG_MGR), pipenv)
	RUN_PRE = pipenv run
	INSTALL_REQUIREMENTS = pipenv install
	GEN_REQUIREMENTS = pipenv lock -r > requirements.txt
else
	RUN_PRE = 
	INSTALL_REQUIREMENTS = pip install -r requirements.txt
	GEN_REQUIREMENTS = pip freeze --local > requirements.txt
endif

PYTHON := $(RUN_PRE) $(PYTHON)


#
#	Recipes
#

.PHONY: help init requirements generate_requirements configure \
		createsuperuser changepassword setup start \
		debug_setup debug debug_createsuperuser \
		debug_start local_start \
		clean check_deploy

.DEFAULT_GOAL := help

help: ## Prints help for this Makefile
	@printf 'Usage: make \033[36m[target]\033[0m\n'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ''

all: requirements start ## Installs requirements and starts server

# - Setup repository

init: ## Sets up this git repository after initial clone
	cp .githooks/* .git/hooks/

# - Install Related

generate_requirements: ## Generates requirements.txt file from environment
	$(GEN_REQUIREMENTS)

requirements: ## Installs project's requirements.txt to environment
	$(INSTALL_REQUIREMENTS)

configure: ## Initial configuration for the application
	touch .env
	$(PYTHON) scripts/new_secret_key.py
	$(PYTHON) scripts/database_variables.py
	$(PYTHON) scripts/aws_variables.py

# - Production Related

createsuperuser: ## Creates a superuser for production
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py createsuperuser --settings=config.settings.production

changepassword: ## Change the superuser password in production
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py changepassword --settings=config.settings.production

update: ## Updates the app (migrations and collect static files)
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

setup: ## Initial setup for the app (migrations, load data, collect static)
	cd $(PROJECT_DIR) && \
	$(PYTHON) manage.py makemigrations $(DJANGO_APPS) --settings=config.settings.production && \
	$(PYTHON) manage.py migrate --settings=config.settings.production && \
	$(PYTHON) manage.py loaddata --settings=config.settings.production $(FIXTURES) && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.production

start: ## Starts the server process
	$(RUN_PRE) ./scripts/start.sh

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
	$(PYTHON) manage.py loaddata --settings=config.settings.local $(FIXTURES) && \
	$(PYTHON) manage.py collectstatic --no-input --settings=config.settings.local

debug: ## Run the debug django server
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver

debug_start: ## Starts the gunicorn server with debug settings
	$(RUN_PRE) ./scripts/debug_start.sh

local: ## Starts the django server with local settings
	cd $(PROJECT_DIR) && $(PYTHON) manage.py runserver --settings=config.settings.local

local_start: ## Starts the gunicorn server with local settings
	$(RUN_PRE) ./scripts/local_start.sh

# - Misc

clean: ## Cleans the debug project (database, static)
	rm $(PROJECT_DIR)/db.sqlite3 || true
	rm -rf $(PROJECT_DIR)/static/* || true
	touch $(PROJECT_DIR)/static/.gitkeep

check_deploy: ## Checks the project prior to deploying
	cd $(PROJECT_DIR) && $(PYTHON) manage.py check --deploy --settings=config.settings.production
