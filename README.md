![Python CI Steps Github Actions](https://github.com/noahgift/python-devops-course/workflows/Python%20CI%20Steps%20Github%20Actions/badge.svg)

[![CircleCI](https://circleci.com/gh/noahgift/python-devops-course.svg?style=svg)](https://circleci.com/gh/noahgift/python-devops-course)

# Python DevOps Course

A comprehensive repository for learning Python DevOps practices with organized project structure and AWS integration.

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
│   ├── test_aws_iam.py           # AWS IAM manager tests
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
├── notebooks/                    # Jupyter notebooks
│   ├── Python_for_DevOps.ipynb  # Main DevOps notebook
│   └── Python_for_DevOps-10-07-2021.ipynb # Historical notebook
├── requirements.txt              # Dependencies (pylint, click, pytest, boto3, ipython, pandas)
├── Makefile                      # Build automation with 15+ commands
├── pytest.ini                   # Test configuration
├── .gitignore                    # Version control exclusions
├── README.md                     # Project overview
└── PROJECT_STRUCTURE.md          # Detailed structure guide
```

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

## 📖 Documentation

- **Project Structure**: `PROJECT_STRUCTURE.md`
- **AWS Setup**: `docs/AWS_IAM_SETUP.md`
- **Notebooks**: `notebooks/` directory
- **Code Examples**: See `src/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the project structure
4. Write tests for new functionality
5. Run linting and formatting
6. Submit a pull request

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
