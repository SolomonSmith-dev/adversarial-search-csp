"""Test configuration: expose project modules to the test suite."""
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tictactoe"))
sys.path.insert(0, str(ROOT / "csp"))
