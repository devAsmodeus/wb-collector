"""
Обёртка для cron — запускает только sync через tools.

Для полного прохода используйте: python -m tools
Для только sync: python -m tools sync
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.cli import main

result = main(["sync"])
sys.exit(result)
