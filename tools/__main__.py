"""Точка входа: python -m tools [migrate|sync|drift|all]"""
import sys
from tools.cli import main

sys.exit(main(sys.argv[1:] or None))
