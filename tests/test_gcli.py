from click.testing import CliRunner
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src", "cli"))
from gcli import search


# search(path, ftype):


def test_search():
    runner = CliRunner()
    result = runner.invoke(search, ["--path", "tests", "--ftype", "py"])
    assert result.exit_code == 0
    assert "Found Matches:" in result.output
