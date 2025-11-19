###############################################
#
# Open edX plugin to generate signed video URLs from Amazon Cloudfront. commands.
#
###############################################

# Define PIP_COMPILE_OPTS=-v to get more information during make upgrade.
PIP_COMPILE = pip-compile --rebuild --upgrade $(PIP_COMPILE_OPTS)

.DEFAULT_GOAL := help

help: ## display this help message
	@echo "Please use \`make <target>' where <target> is one of"
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

clean: ## delete most git-ignored files
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

requirements: ## install environment requirements
	pip install -r requirements/base.txt

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: ## update the requirements/*.txt files with the latest packages satisfying requirements/*.in
	pip install -qr requirements/pip-tools.txt
	# Make sure to compile files after any other files they include!
	$(PIP_COMPILE) -o requirements/pip-tools.txt requirements/pip-tools.in
	$(PIP_COMPILE) -o requirements/base.txt requirements/base.in
	$(PIP_COMPILE) -o requirements/quality.txt requirements/quality.in
	$(PIP_COMPILE) -o requirements/dev.txt requirements/dev.in

quality: clean ## check coding style with pycodestyle and pylint
	pip install -r requirements/quality.txt
	pycodestyle ./secure_cloudfront_video
	pylint ./secure_cloudfront_video --rcfile=./setup.cfg

requirements-dev: ## install development environment requirements.
	pip install -r requirements/dev.txt

changelog-entry: requirements-dev ## Create a new changelog entry.
	scriv create --edit

changelog: requirements-dev ## Collect changelog entries in the CHANGELOG.md file.
	scriv collect --keep
