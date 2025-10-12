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

aws-setup:
	. venv/bin/activate && \
	python aws_iam_manager.py --create-access-key

aws-test:
	. venv/bin/activate && \
	python -m pytest test_aws_iam.py -v

aws-cleanup:
	@echo "To cleanup AWS resources, run the commands in AWS_IAM_SETUP.md"