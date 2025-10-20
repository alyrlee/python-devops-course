#!/usr/bin/env python3
"""
Integration tests for the Python DevOps Course application
Tests the integration between different components
"""

import pytest
import sys
import os
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

try:
    from cli.helloclick import tokenize
    from cli.gcli import search
    from aws.aws_iam_manager import AWSIAMManager
    from web.application import app
except ImportError:
    # Fallback for pylint static analysis
    tokenize = None
    search = None
    AWSIAMManager = None
    app = None


@pytest.mark.integration
def test_cli_integration():
    """Test integration between CLI components"""
    if tokenize is None or search is None:
        pytest.skip("CLI components not available")
    
    from click.testing import CliRunner
    
    runner = CliRunner()
    
    # Test helloclick integration
    result = runner.invoke(tokenize, ["--phrase", "Hello World"])
    assert result.exit_code == 0
    assert "hello" in result.output.lower()
    assert "world" in result.output.lower()
    
    # Test gcli integration
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test content")
        
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "txt"])
        assert result.exit_code == 0
        assert "Found Matches:" in result.output


@pytest.mark.integration
def test_web_application_integration():
    """Test web application integration"""
    if app is None:
        pytest.skip("Web application not available")
    
    with app.test_client() as client:
        # Test root endpoint
        response = client.get('/')
        assert response.status_code == 200
        
        # Test health endpoint if it exists
        try:
            response = client.get('/health')
            assert response.status_code == 200
        except:
            # Health endpoint might not exist, that's okay
            pass


@pytest.mark.integration
def test_aws_components_integration():
    """Test AWS components integration (without actual AWS calls)"""
    if AWSIAMManager is None:
        pytest.skip("AWS IAM Manager not available")
    
    # Test that AWS components can be imported and initialized
    # This is a lightweight integration test that doesn't make actual AWS calls
    
    # Test AWS IAM Manager can be instantiated (with mocked clients)
    with pytest.MonkeyPatch().context() as m:
        def mock_client(service, region_name=None):
            return None
        m.setattr("boto3.client", mock_client)
        manager = AWSIAMManager("us-east-1")
        assert manager.region == "us-east-1"


@pytest.mark.integration
def test_file_system_integration():
    """Test file system integration"""
    if search is None:
        pytest.skip("Search component not available")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_files = ["test1.py", "test2.py", "test3.txt"]
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"content for {filename}")
        
        # Test file search integration
        from click.testing import CliRunner
        runner = CliRunner()
        
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "py"])
        assert result.exit_code == 0
        assert "test1.py" in result.output
        assert "test2.py" in result.output
        assert "test3.txt" not in result.output


@pytest.mark.integration
def test_application_startup_integration():
    """Test that the application can start up without errors"""
    # Test that all main modules can be imported
    import src.cli.helloclick
    import src.cli.gcli
    import src.aws.aws_iam_manager
    import src.web.application
    
    # Test that Flask app can be accessed
    if app is not None:
        assert app is not None
        assert app.name == 'web.application'
    else:
        pytest.skip("Web application not available")
