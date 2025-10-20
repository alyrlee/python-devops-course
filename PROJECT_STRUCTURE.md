# Project Structure

This document describes the organized structure of the Python DevOps Course project.

## Directory Structure

```
python-devops-course/
├── src/                          # Source code directory
│   ├── __init__.py              # Main package initialization
│   ├── aws/                     # AWS management module
│   │   ├── __init__.py          # AWS package initialization
│   │   └── aws_iam_manager.py   # AWS IAM role and policy management
│   ├── cli/                     # Command line interface module
│   │   ├── __init__.py          # CLI package initialization
│   │   ├── helloclick.py        # Hello Click CLI tool
│   │   ├── hello-click2.py      # Hello Click CLI tool v2
│   │   └── gcli.py              # General CLI utilities
│   └── utils/                   # Utility functions module
│       ├── __init__.py          # Utils package initialization
│       ├── magic_stuff.py       # Magic utility functions
│       └── marco.py             # Marco utility functions
├── tests/                       # Test suite directory
│   ├── __init__.py              # Test package initialization
<!-- │   ├── test_aws_iam.py          # AWS IAM manager tests -->
│   ├── test_helloclick.py       # Hello Click tests
│   └── test_gcli.py             # General CLI tests
├── docs/                        # Documentation directory
│   └── AWS_IAM_SETUP.md         # AWS IAM setup documentation
├── notebooks/                   # Jupyter notebooks directory
│   ├── Python_for_DevOps.ipynb # Main DevOps notebook
│   └── Python_for_DevOps-10-07-2021.ipynb # Historical notebook
├── venv/                        # Virtual environment (not tracked)
├── __pycache__/                 # Python cache (not tracked)
├── requirements.txt             # Python dependencies
├── Makefile                     # Build and automation commands
├── README.md                    # Project overview
└── PROJECT_STRUCTURE.md        # This file
```

## Module Organization

### AWS Module (`src/aws/`)
- **Purpose**: AWS IAM role and policy management
- **Key Files**:
  - `aws_iam_manager.py`: Complete AWS IAM management solution
- **Features**:
  - Cloud9 service role creation
  - AWS managed policy attachment
  - User management and role assumption
  - Access key creation

### CLI Module (`src/cli/`)
- **Purpose**: Command line interface tools
- **Key Files**:
  - `helloclick.py`: Basic Click CLI tool
  - `hello-click2.py`: Enhanced Click CLI tool
  - `gcli.py`: General CLI utilities
- **Features**:
  - Tokenization tools
  - Interactive CLI interfaces
  - Command line argument parsing

### Utils Module (`src/utils/`)
- **Purpose**: Utility functions and helper scripts
- **Key Files**:
  - `magic_stuff.py`: Magic utility functions
  - `marco.py`: Marco utility functions
- **Features**:
  - Helper functions
  - Utility scripts
  - Common functionality

### Tests (`tests/`)
- **Purpose**: Comprehensive test suite
- **Key Files**:
  <!-- - `test_aws_iam.py`: AWS IAM manager tests -->
  - `test_helloclick.py`: Hello Click tests
  - `test_gcli.py`: General CLI tests
- **Features**:
  - Unit tests with mocking
  - Integration tests
  - Coverage reporting

### Documentation (`docs/`)
- **Purpose**: Project documentation
- **Key Files**:
  - `AWS_IAM_SETUP.md`: AWS IAM setup guide
- **Features**:
  - Setup instructions
  - Usage examples
  - Troubleshooting guides

### Notebooks (`notebooks/`)
- **Purpose**: Jupyter notebooks for learning
- **Key Files**:
  - `Python_for_DevOps.ipynb`: Main DevOps notebook
  - `Python_for_DevOps-10-07-2021.ipynb`: Historical notebook
- **Features**:
  - Interactive learning
  - Code examples
  - Documentation

## Build System

### Makefile Targets

| Target | Description |
|--------|-------------|
| `install` | Install dependencies |
| `test` | Run all tests |
| `test-cli` | Run CLI tests |
| `test-aws` | Run AWS tests |
| `lint` | Lint all code |
| `lint-cli` | Lint CLI code |
| `lint-aws` | Lint AWS code |
| `format` | Format all code |
| `format-cli` | Format CLI code |
| `format-aws` | Format AWS code |
| `aws-setup` | Setup AWS IAM with access key |
| `aws-test` | Test AWS functionality |
| `aws-cleanup` | Show AWS cleanup instructions |
| `clean` | Clean up cache files |
| `help` | Show help message |

### Usage Examples

```bash
# Install dependencies
make install

# Run all tests
make test

# Run specific test suites
make test-cli
make test-aws

# Lint and format code
make lint
make format

# AWS management
make aws-setup
make aws-test

# Clean up
make clean

# Get help
make help
```

## Development Workflow

### 1. Setup
```bash
# Clone repository
git clone <repository-url>
cd python-devops-course

# Install dependencies
make install

# Activate virtual environment
source venv/bin/activate
```

### 2. Development
```bash
# Run tests
make test

# Lint code
make lint

# Format code
make format

# Run specific modules
make test-cli
make test-aws
```

### 3. AWS Setup
```bash
# Configure AWS credentials
aws configure

# Setup AWS IAM
make aws-setup

# Test AWS functionality
make aws-test
```

### 4. Cleanup
```bash
# Clean cache files
make clean

# AWS cleanup (see docs/AWS_IAM_SETUP.md)
make aws-cleanup
```

## Best Practices

### Code Organization
- **Separation of Concerns**: Each module has a specific purpose
- **Package Structure**: Proper `__init__.py` files for Python packages
- **Test Organization**: Tests mirror source structure
- **Documentation**: Comprehensive documentation in `docs/`

### Development
- **Virtual Environment**: Always use `venv/` for dependencies
- **Testing**: Run tests before committing
- **Linting**: Use pylint for code quality
- **Formatting**: Use black for code formatting

### AWS Management
- **Security**: Follow AWS IAM best practices
- **Documentation**: Keep AWS setup documented
- **Testing**: Test AWS functionality with mocks
- **Cleanup**: Always clean up AWS resources

## File Naming Conventions

- **Python Files**: Use snake_case (e.g., `aws_iam_manager.py`)
<!-- - **Test Files**: Prefix with `test_` (e.g., `test_aws_iam.py`) -->
- **Documentation**: Use UPPER_CASE (e.g., `AWS_IAM_SETUP.md`)
- **Notebooks**: Use descriptive names (e.g., `Python_for_DevOps.ipynb`)

## Dependencies

### Core Dependencies
- `click`: Command line interface framework
- `boto3`: AWS SDK for Python
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `pylint`: Code linting
- `black`: Code formatting

### Development Dependencies
- `coverage`: Code coverage
- `isort`: Import sorting
- `mypy`: Type checking (optional)

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Follow the project structure**
4. **Write tests for new functionality**
5. **Run linting and formatting**
6. **Submit a pull request**

## Maintenance

### Regular Tasks
- **Update dependencies**: Keep requirements.txt current
- **Run tests**: Ensure all tests pass
- **Update documentation**: Keep docs current
- **Clean up**: Remove unused files and dependencies

### AWS Resources
- **Monitor usage**: Track AWS resource usage
- **Rotate credentials**: Regularly rotate access keys
- **Review permissions**: Audit IAM permissions
- **Clean up resources**: Remove unused AWS resources
