-include .env
export

VENV := $(CURDIR)/.venv
PYTHON := $(VENV)/bin/python
DBT := $(VENV)/bin/dbt
DBT_DIR := transform

.PHONY: setup build test handbook clean start close fetch load

setup:
	mkdir -p data
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	cd $(DBT_DIR) && $(DBT) debug --target dev && $(DBT) debug --target prod

build:
	cd $(DBT_DIR) && $(DBT) deps && $(DBT) seed && $(DBT) snapshot && $(DBT) build

test:
	cd $(DBT_DIR) && $(DBT) test

handbook:
	$(PYTHON) scripts/build_handbook_index.py

clean:
	cd $(DBT_DIR) && $(DBT) clean
	rm -f data/*.duckdb data/*.duckdb.wal

start:
	$(PYTHON) scripts/milestone.py start $(M)

close:
	$(PYTHON) scripts/milestone.py close $(M)

fetch:
	$(PYTHON) scripts/milestone.py fetch $(F)

load:
	$(PYTHON) el/load_raw.py $(if $(SF),--scale-factor $(SF)) $(if $(THROUGH_DATE),--through-date $(THROUGH_DATE)) $(if $(MUTATE),--mutate) $(if $(RESET),--full-reset)
