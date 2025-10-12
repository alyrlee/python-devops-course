install:
	python3 -m venv venv &&\
		. venv/bin/activate &&\
		pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	. venv/bin/activate && \
	python -m pytest tests/ -vv --cov=src

test-cli:
	. venv/bin/activate && \
	python -m pytest tests/test_helloclick.py tests/test_gcli.py -vv

test-aws:
	. venv/bin/activate && \
	python -m pytest tests/test_aws_iam.py -vv

lint:
	. venv/bin/activate && \
	pylint --disable=R,C,E1120 src/ tests/

lint-cli:
	. venv/bin/activate && \
	pylint --disable=R,C,E1120 src/cli/

lint-aws:
	. venv/bin/activate && \
	pylint --disable=R,C,E1120 src/aws/
	
format:
	. venv/bin/activate && \
	black src/ tests/

format-cli:
	. venv/bin/activate && \
	black src/cli/

format-aws:
	. venv/bin/activate && \
	black src/aws/

all: install lint test

aws-setup:
	. venv/bin/activate && \
	python src/aws/aws_iam_manager.py --create-access-key

aws-test:
	. venv/bin/activate && \
	python -m pytest tests/test_aws_iam.py -v

aws-cleanup:
	@echo "To cleanup AWS resources, run the commands in docs/AWS_IAM_SETUP.md"

clean:
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

help:
	@echo "Available targets:"
	@echo "  install     - Install dependencies"
	@echo "  test        - Run all tests"
	@echo "  test-cli    - Run CLI tests"
	@echo "  test-aws    - Run AWS tests"
	@echo "  lint        - Lint all code"
	@echo "  lint-cli    - Lint CLI code"
	@echo "  lint-aws    - Lint AWS code"
	@echo "  format      - Format all code"
	@echo "  format-cli  - Format CLI code"
	@echo "  format-aws  - Format AWS code"
	@echo "  aws-setup   - Setup AWS IAM with access key"
	@echo "  aws-test    - Test AWS functionality"
	@echo "  aws-cleanup - Show AWS cleanup instructions"
	@echo "  clean       - Clean up cache files"
	@echo "  help        - Show this help message"