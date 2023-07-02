gurebu:
	node microservice/gurebu.js

run:
	python3 run.py

install:
	pip3 install -r requirements.txt && cd microservice && npm install