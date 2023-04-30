SHELL := /bin/bash

help:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

venv:
	./create_venv.sh

lint:
	@echo "*********** YAMLLINT"
	@yamllint -c=.yamllint.yml . || true
	@echo "*********** ANSIBLE LINT"
	@ansible-lint -c .ansible-lint

converge_scratch: 
	@molecule destroy
	@molecule create
	@molecule converge 