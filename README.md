![Python DevOps CI/CD Pipeline](https://github.com/noahgift/python-devops-course/workflows/Python%20DevOps%20CI/CD%20Pipeline/badge.svg)

[![CircleCI](https://circleci.com/gh/noahgift/python-devops-course.svg?style=svg)](https://circleci.com/gh/noahgift/python-devops-course)

# Python DevOps Course

A comprehensive repository for learning Python DevOps practices with enterprise-grade CI/CD pipeline, security scanning, and AWS integration.

## 📁 Project Structure

```
python-devops-course/
├── src/                           # Source code
│   ├── aws/                      # AWS management tools
│   │   └── aws_iam_manager.py    # Complete AWS IAM role & policy management
│   ├── cli/                      # Command line interfaces
│   │   ├── helloclick.py         # Tokenizer CLI tool
│   │   ├── hello-click2.py       # Enhanced CLI with name processing
│   │   ├── gcli.py               # File search utility
│   │   ├── hello.py              # AWS S3 buckets listing tool
│   │   └── lambda_function.py    # AWS Lambda function example
│   └── utils/                    # Utility functions
│       ├── magic_stuff.py        # Magic utility functions
│       └── marco.py              # Marco utility functions
├── tests/                        # Test suite
│   ├── test_helloclick.py       # Tokenizer tests
│   └── test_gcli.py              # File search tests
├── scripts/                      # Deployment and automation scripts
│   ├── deploy_lambda.py          # Full Lambda deployment with role creation
│   ├── deploy_lambda_simple.py  # Simplified Lambda deployment
│   └── deploy_with_role.py       # Lambda deployment with existing role
├── lambda_packages/              # Lambda deployment packages
│   └── python-devops-lambda.zip  # Current deployment package
├── docs/                         # Documentation
│   └── AWS_IAM_SETUP.md          # AWS setup guide
├── requirements.txt              # Dependencies (pylint, click, pytest, boto3, ipython, pandas)
├── Makefile                      # Build automation with 15+ commands
├── pytest.ini                   # Test configuration
├── .gitignore                    # Version control exclusions
├── README.md                     # Project overview
└── PROJECT_STRUCTURE.md          # Detailed structure guide
```

## 🚀 Enhanced CI/CD Pipeline

### 🔒 Security & Quality
- **Security Scanning**: Bandit, Semgrep, Safety with SARIF uploads
- **Dependency Review**: Automated vulnerability scanning for PRs
- **SARIF Integration**: Security results surface in GitHub Security tab
- **Conditional Failure**: Soft failures on dev, hard failures on main

### ⚡ Performance & Efficiency
- **Parallel Testing**: pytest-xdist with conditional strategies
- **Build Once, Deploy Many**: Artifact reuse across environments
- **Smart Caching**: pip cache with dependency path monitoring
- **Fail-Fast Control**: Resilient to single environment failures

### 🌍 Multi-Environment Deployment
- **GitHub Environments**: Approval gates and environment-specific secrets
- **Matrix Strategies**: Parallel deployment to multiple environments
- **Environment-Specific**: Different configurations per environment
- **URL Tracking**: Deployment URL history and monitoring

### 🛠️ Developer Experience
- **Job Summaries**: Rich markdown summaries in GitHub UI
- **Composite Actions**: DRY principle for reusable workflows
- **Ruff Integration**: 10-100x faster linting than pylint
- **Artifact Management**: Conditional uploads with retention policies

## 🚀 Quick Start

```bash
# Install dependencies
make install

# Run tests
make test

# Setup AWS IAM
make aws-setup

# Get help
make help
```

## 🛠️ Available Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make test` | Run all tests |
| `make test-cli` | Run CLI tests |
| `make test-aws` | Run AWS tests |
| `make lint` | Lint all code |
| `make format` | Format all code |
| `make aws-setup` | Setup AWS IAM |
| `make clean` | Clean up cache files |
| `make help` | Show all commands |

## 📚 Modules

### AWS Management (`src/aws/`)
- **AWS IAM Manager**: Complete Cloud9 service role and policy management
- **Features**: Role creation, policy attachment, user management
- **Documentation**: See `docs/AWS_IAM_SETUP.md`

### CLI Tools (`src/cli/`)
- **Hello Click**: Interactive CLI tools with Click framework
- **Features**: Tokenization, command line interfaces, AWS integration
- **Examples**: `helloclick.py`, `hello-click2.py`, `gcli.py`, `hello.py`, `lambda_function.py`

### Utilities (`src/utils/`)
- **Magic Functions**: Utility functions and helpers
- **Features**: Common functionality, helper scripts
- **Examples**: `magic_stuff.py`, `marco.py`

## 🔧 Development

### Prerequisites
- Python 3.8+
- AWS CLI configured (for AWS features)
- Virtual environment

### Setup
```bash
# Clone repository
git clone <repository-url>
cd python-devops-course

# Install dependencies
make install

# Activate virtual environment
source venv/bin/activate
```

### Testing
```bash
# Run all tests
make test

# Run specific test suites
make test-cli
make test-aws

# Run with coverage
make test
```

### Code Quality
```bash
# Lint code
make lint

# Format code
make format

# Clean up
make clean
```

## ☁️ AWS Integration

### AWS IAM Management
- **Cloud9 Service Role**: Automated role creation with proper policies
- **User Management**: IAM user creation and role attachment
- **Security**: AWS managed policies and best practices

### Setup AWS
```bash
# Configure AWS credentials
aws configure

# Setup AWS IAM
make aws-setup

# Test AWS functionality
make aws-test
```

### AWS Features
- ✅ Cloud9 service role creation
- ✅ AWS managed policy attachment
- ✅ User management and role assumption
- ✅ Access key creation
- ✅ Comprehensive error handling

## 🔄 GitHub Actions CI/CD

### Main Pipeline (`.github/workflows/main.yml`)
```yaml
# Security scanning with SARIF uploads
- name: Bandit (SARIF)
  run: bandit -r src -f sarif -o bandit.sarif

- name: Semgrep (SARIF)  
  run: semgrep ci --config p/ci --sarif --output semgrep.sarif

- name: Upload SARIF
  uses: github/codeql-action/upload-sarif@v3
```

### Parallel Testing
```yaml
# Fast feedback on PRs, comprehensive on main
- name: Test with pytest
  run: |
    if [ "${{ github.ref }}" == "refs/heads/main" ]; then
      pytest -q --maxfail=0 -n auto --durations=15
    else
      pytest -q --maxfail=1 -n auto --durations=15
    fi
```

### Multi-Environment Deployment
```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - environment: ephemeral
        aws_region: us-east-1
        timeout: 300
      - environment: dev
        aws_region: us-east-1
        timeout: 600
      - environment: staging
        aws_region: us-east-1
        timeout: 900
      - environment: prod
        aws_region: us-west-2
        timeout: 1200
```

### Composite Actions
```yaml
# DRY Python setup
- uses: ./.github/actions/python-setup

# Environment-specific post-deploy checks
- uses: ./.github/actions/post-deploy-checks
  with:
    environment: ${{ matrix.environment }}
```

## 📖 Documentation

- **Project Structure**: `PROJECT_STRUCTURE.md`
- **AWS Setup**: `docs/AWS_IAM_SETUP.md`
- **Code Examples**: See `src/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the project structure
4. Write tests for new functionality
5. Run linting and formatting
6. Submit a pull request

## 🚀 AWS CodeBuild & Elastic Beanstalk Deployment

### 📦 AWS CodeBuild Integration

#### **Buildspec Configuration**
Create `buildspec.yml` in your project root:

```yaml
version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  pre_build:
    commands:
      - echo Installing dependencies...
      - pip install -r requirements.txt
  build:
    commands:
      - echo Running tests...
      - make test
      - echo Running linting...
      - make lint
      - echo Building web application...
      - cd src/web && python -c "import application; print('✅ Web app ready')"
  post_build:
    commands:
      - echo Build completed successfully
artifacts:
  files:
    - '**/*'
  base-directory: .
```

#### **CodeBuild Setup Commands**
```bash
# Create CodeBuild project
aws codebuild create-project \
  --name python-devops-build \
  --source type=GITHUB,location=https://github.com/your-username/python-devops-course \
  --artifacts type=NO_ARTIFACTS \
  --environment type=LINUX_CONTAINER,image=aws/codebuild/python:3.11 \
  --service-role arn:aws:iam::YOUR_ACCOUNT:role/CodeBuildServiceRole

# Start build
aws codebuild start-build --project-name python-devops-build
```

### 🌐 Elastic Beanstalk Deployment

#### **1. Create Application Package**
```bash
# Create deployment package
mkdir -p eb-deploy
cp -r src/web/* eb-deploy/
cp requirements.txt eb-deploy/
cp Procfile eb-deploy/

# Create Procfile for Elastic Beanstalk
echo "web: gunicorn application:app --bind 0.0.0.0:8000" > eb-deploy/Procfile

# Create .ebextensions for configuration
mkdir -p eb-deploy/.ebextensions
```

#### **2. Elastic Beanstalk Configuration**
Create `eb-deploy/.ebextensions/01_packages.config`:
```yaml
packages:
  yum:
    git: []
```

Create `eb-deploy/.ebextensions/02_python.config`:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: application:app
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: "/var/app/current"
```

#### **3. Deployment Commands**
```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init python-devops-app

# Create environment
eb create python-devops-env

# Deploy application
eb deploy

# Open in browser
eb open
```

#### **4. Environment Configuration**
```bash
# Set environment variables
eb setenv AWS_DEFAULT_REGION=us-east-1

# Scale application
eb scale 2

# View logs
eb logs

# Terminate environment
eb terminate
```

### 🔄 CI/CD Pipeline Integration

#### **GitHub Actions + CodeBuild + Elastic Beanstalk**
```yaml
# .github/workflows/deploy-aws.yml
name: Deploy to AWS
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Deploy to Elastic Beanstalk
      run: |
        pip install awsebcli
        eb deploy python-devops-env
```

### 📊 Monitoring & Logs

#### **CloudWatch Integration**
```bash
# View application logs
aws logs describe-log-groups --log-group-name-prefix /aws/elasticbeanstalk

# Monitor metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ElasticBeanstalk \
  --metric-name ApplicationRequestsTotal \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

#### **Health Monitoring**
```bash
# Check application health
eb health

# View detailed health
eb health --refresh

# Monitor specific instances
eb status --verbose
```

### 🛠️ Advanced Configuration

#### **Load Balancer Configuration**
```yaml
# .ebextensions/03_loadbalancer.config
option_settings:
  aws:elbv2:loadbalancer:
    IdleTimeout: 60
  aws:autoscaling:launchconfiguration:
    InstanceType: t3.micro
```

#### **Database Integration**
```yaml
# .ebextensions/04_database.config
option_settings:
  aws:rds:dbinstance:
    DBInstanceClass: db.t3.micro
    DBAllocatedStorage: 20
```

### 📋 Deployment Checklist

- [ ] **CodeBuild**: Build and test automation
- [ ] **Elastic Beanstalk**: Application deployment
- [ ] **CloudWatch**: Monitoring and logging
- [ ] **Load Balancer**: Traffic distribution
- [ ] **Auto Scaling**: Handle traffic spikes
- [ ] **Health Checks**: Application monitoring
- [ ] **SSL/TLS**: Secure connections
- [ ] **Domain**: Custom domain setup

## 📄 License

This project is part of the Python DevOps Course.

## 🎓 Pragmatic AI Labs | Join 1M+ ML Engineers

### 🔥 Hot Course Offers:
* 🤖 [Master GenAI Engineering](https://ds500.paiml.com/learn/course/0bbb5/) - Build Production AI Systems
* 🦀 [Learn Professional Rust](https://ds500.paiml.com/learn/course/g6u1k/) - Industry-Grade Development
* 📊 [AWS AI & Analytics](https://ds500.paiml.com/learn/course/31si1/) - Scale Your ML in Cloud
* ⚡ [Production GenAI on AWS](https://ds500.paiml.com/learn/course/ehks1/) - Deploy at Enterprise Scale
* 🛠️ [Rust DevOps Mastery](https://ds500.paiml.com/learn/course/ex8eu/) - Automate Everything

### 🚀 Level Up Your Career:
* 💼 [Production ML Program](https://paiml.com) - Complete MLOps & Cloud Mastery
* 🎯 [Start Learning Now](https://ds500.paiml.com) - Fast-Track Your ML Career
* 🏢 Trusted by Fortune 500 Teams

Learn end-to-end ML engineering from industry veterans at [PAIML.COM](https://paiml.com)
