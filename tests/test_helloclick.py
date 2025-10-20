from click.testing import CliRunner
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "cli"))
try:
    from helloclick import tokenize
except ImportError:
    # Fallback for pylint static analysis
    tokenize = None


def test_helloclick():
    runner = CliRunner()
    result = runner.invoke(tokenize, ["--phrase", "The Whale is large"])
    assert result.exit_code == 0
    assert "whale" in result.output
