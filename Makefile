install:
	python3 -m venv venv &&\
		. venv/bin/activate &&\
		pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	. venv/bin/activate && \
	python -m pytest -vv --cov=helloclick test_helloclick.py

lint:
	. venv/bin/activate && \
	pylint --disable=R,C,E1120 helloclick.py
	
format:
	. venv/bin/activate && \
	black *.py

all: install lint test