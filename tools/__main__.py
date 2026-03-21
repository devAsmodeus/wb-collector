"""Позволяет запускать как: python -m tools [command]"""
import sys
from tools.cli import main

sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "all"))
