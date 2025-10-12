from click.testing import CliRunner
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'cli'))
from helloclick import tokenize


def test_helloclick():
    runner = CliRunner()
    result = runner.invoke(tokenize, ["--phrase", "The Whale is large"])
    assert result.exit_code == 0
    assert "Whale" in result.output
