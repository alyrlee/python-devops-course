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

lambda-deploy:
	. venv/bin/activate && \
	python scripts/deploy_with_role.py

lambda-deploy-auto:
	. venv/bin/activate && \
	python scripts/deploy_lambda_simple.py

lambda-deploy-full:
	. venv/bin/activate && \
	python scripts/deploy_lambda.py

lambda-test:
	. venv/bin/activate && \
	python -c "import sys; sys.path.append('src/cli'); from lambda_function import lambda_handler; print(lambda_handler({'name': 'Test'}, {}))"

cloudwatch-logs:
	. venv/bin/activate && \
	python src/aws/cloudwatch_monitor.py --logs

cloudwatch-metrics:
	. venv/bin/activate && \
	python src/aws/cloudwatch_monitor.py --metrics

cloudwatch-info:
	. venv/bin/activate && \
	python src/aws/cloudwatch_monitor.py --info

cloudwatch-all:
	. venv/bin/activate && \
	python src/aws/cloudwatch_monitor.py --info --metrics --logs

web-install:
	. venv/bin/activate && \
	pip install flask gunicorn

web-dev:
	. venv/bin/activate && \
	cd src/web && python application.py

web-prod:
	. venv/bin/activate && \
	cd src/web && gunicorn --bind 0.0.0.0:8000 --workers 4 application:app

web-test:
	. venv/bin/activate && \
	curl -f http://localhost:8000/api/health || echo "Web server not running"

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
	@echo "  lambda-deploy      - Deploy Lambda with Lambda_Service role"
	@echo "  lambda-deploy-auto - Deploy Lambda (auto-find role)"
	@echo "  lambda-deploy-full  - Deploy Lambda (full with role creation)"
	@echo "  lambda-test        - Test Lambda function locally"
	@echo "  cloudwatch-logs    - Show Lambda CloudWatch logs"
	@echo "  cloudwatch-metrics - Show Lambda CloudWatch metrics"
	@echo "  cloudwatch-info    - Show Lambda function information"
	@echo "  cloudwatch-all     - Show all CloudWatch data"
	@echo "  web-install        - Install Flask and Gunicorn"
	@echo "  web-dev           - Run web server in development mode"
	@echo "  web-prod          - Run web server with Gunicorn (production)"
	@echo "  web-test          - Test web server health"
	@echo "  clean       - Clean up cache files"
	@echo "  help        - Show this help message"