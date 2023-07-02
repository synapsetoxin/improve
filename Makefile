PY = python3
VENV = venv
BIN=$(VENV)/bin

# make it work on windows too
ifeq ($(OS), Windows_NT)
    BIN=$(VENV)/Scripts
    PY=python
endif

gurebu:
	node microservice/gurebu.js

run:
	python3 run.py

db:
	$(PY) -c "import app.src.database.models as db; _db = db.Database(); _db.create_tables()"

install:
	pip3 install -r requirements.txt && cd microservice && npm install

env:
	$(PY) -m venv $(VENV)
	$(BIN)/pip3 install -r requirements.txt

clean:
	rm -rf $(VENV)
	find -iname "*.pyc" -delete