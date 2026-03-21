"""
Обёртка для обратной совместимости с cron.
Основная логика — в tools/sync_docs/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.sync_docs.runner import run

if __name__ == "__main__":
    result = run()
    print(result["report"])
