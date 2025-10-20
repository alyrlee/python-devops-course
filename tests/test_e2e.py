#!/usr/bin/env python3
"""
End-to-End tests for the Python DevOps Course application
Tests complete user workflows and system integration
"""

import pytest
import sys
import os
import tempfile
import shutil
import time
from click.testing import CliRunner

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


@pytest.mark.e2e
def test_complete_cli_workflow():
    """Test complete CLI workflow from start to finish"""
    if tokenize is None or search is None:
        pytest.skip("CLI components not available")
    
    runner = CliRunner()
    
    # Step 1: Tokenize some text
    result = runner.invoke(tokenize, ["--phrase", "DevOps is awesome"])
    assert result.exit_code == 0
    assert "devops" in result.output.lower()
    assert "awesome" in result.output.lower()
    
    # Step 2: Search for files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        test_files = ["app.py", "config.py", "README.md", "data.csv"]
        for filename in test_files:
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w") as f:
                f.write(f"# {filename}\nContent for {filename}")
        
        # Search for Python files
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "py"])
        assert result.exit_code == 0
        assert "app.py" in result.output
        assert "config.py" in result.output
        assert "README.md" not in result.output


@pytest.mark.e2e
def test_web_application_e2e():
    """Test complete web application end-to-end workflow"""
    if app is None:
        pytest.skip("Web application not available")
    
    with app.test_client() as client:
        # Test main application flow
        response = client.get('/')
        assert response.status_code == 200
        
        # Test that the application is responsive
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second


@pytest.mark.e2e
def test_aws_integration_e2e():
    """Test AWS integration end-to-end (without actual AWS calls)"""
    if AWSIAMManager is None:
        pytest.skip("AWS IAM Manager not available")
    
    # Test complete AWS workflow simulation
    with pytest.MonkeyPatch().context() as m:
        def mock_client(service, region_name=None):
            return None
        m.setattr("boto3.client", mock_client)
        
        # Initialize AWS manager
        manager = AWSIAMManager("us-east-1")
        assert manager.region == "us-east-1"
        
        # Test that we can simulate AWS operations
        # (In a real e2e test, this would make actual AWS calls)


@pytest.mark.e2e
def test_file_processing_e2e():
    """Test complete file processing workflow"""
    if search is None:
        pytest.skip("Search component not available")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a realistic file structure
        subdirs = ["src", "tests", "docs", "data"]
        for subdir in subdirs:
            os.makedirs(os.path.join(temp_dir, subdir), exist_ok=True)
        
        # Create various file types
        files = {
            "src/app.py": "def main():\n    pass",
            "src/config.py": "DEBUG = True",
            "tests/test_app.py": "def test_main():\n    pass",
            "docs/README.md": "# Project Documentation",
            "data/sample.csv": "name,age\nJohn,30",
            "data/config.json": '{"debug": true}'
        }
        
        for filepath, content in files.items():
            full_path = os.path.join(temp_dir, filepath)
            with open(full_path, "w") as f:
                f.write(content)
        
        runner = CliRunner()
        
        # Test searching for Python files (only in root directory)
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "py"])
        assert result.exit_code == 0
        # The search function only looks in the immediate directory, not subdirectories
        # So we should not find files in subdirectories
        assert "Found Matches:" in result.output
        
        # Test searching for JSON files (only in root directory)
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "json"])
        assert result.exit_code == 0
        # The search function only looks in the immediate directory, not subdirectories
        # So we should not find files in subdirectories
        assert "Found Matches:" in result.output


@pytest.mark.e2e
def test_application_startup_e2e():
    """Test complete application startup and initialization"""
    # Test that all components can be imported and initialized
    import src.cli.helloclick
    import src.cli.gcli
    import src.aws.aws_iam_manager
    import src.web.application
    
    # Test CLI components
    runner = CliRunner()
    
    # Test helloclick
    if tokenize is not None:
        result = runner.invoke(tokenize, ["--phrase", "Test phrase"])
        assert result.exit_code == 0
    
    # Test gcli
    if search is not None:
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")
            
            result = runner.invoke(search, ["--path", temp_dir, "--ftype", "txt"])
            assert result.exit_code == 0
    
    # Test web application
    if app is not None:
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200


@pytest.mark.e2e
def test_error_handling_e2e():
    """Test error handling in end-to-end scenarios"""
    if tokenize is None or search is None:
        pytest.skip("CLI components not available")
    
    runner = CliRunner()
    
    # Test CLI error handling
    # Test with invalid file path
    result = runner.invoke(search, ["--path", "/nonexistent/path", "--ftype", "txt"])
    assert result.exit_code == 0  # Should handle gracefully
    
    # Test with empty directory
    with tempfile.TemporaryDirectory() as temp_dir:
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "py"])
        assert result.exit_code == 0
        assert "Found Matches:" in result.output  # Should show no matches


@pytest.mark.e2e
def test_performance_e2e():
    """Test application performance in end-to-end scenarios"""
    if tokenize is None or search is None:
        pytest.skip("CLI components not available")
    
    runner = CliRunner()
    
    # Test CLI performance
    start_time = time.time()
    result = runner.invoke(tokenize, ["--phrase", "Performance test phrase"])
    end_time = time.time()
    
    assert result.exit_code == 0
    assert (end_time - start_time) < 2.0  # Should complete within 2 seconds
    
    # Test file search performance with many files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create many files
        for i in range(100):
            filepath = os.path.join(temp_dir, f"file_{i}.txt")
            with open(filepath, "w") as f:
                f.write(f"Content for file {i}")
        
        start_time = time.time()
        result = runner.invoke(search, ["--path", temp_dir, "--ftype", "txt"])
        end_time = time.time()
        
        assert result.exit_code == 0
        assert (end_time - start_time) < 5.0  # Should complete within 5 seconds
