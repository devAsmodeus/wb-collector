"""Запуск Alembic миграций."""
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.parent


def run_migrations() -> dict:
    """
    Выполняет `alembic upgrade head`.
    Возвращает результат: статус, текущая ревизия, вывод.
    """
    result = subprocess.run(
        ["python", "-m", "alembic", "upgrade", "head"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    output = (result.stdout + result.stderr).strip()
    success = result.returncode == 0

    # Определяем что произошло
    if "Running upgrade" in output:
        status = "upgraded"
        # Извлекаем ревизию из строки "Running upgrade abc -> def, message"
        for line in output.splitlines():
            if "Running upgrade" in line:
                parts = line.split("Running upgrade")[-1].strip().split(",")[0].strip()
                status = f"upgraded → {parts}"
                break
    elif "up to date" in output or not output:
        status = "up_to_date"
    elif not success:
        status = "error"
    else:
        status = "ok"

    return {
        "success": success,
        "status":  status,
        "output":  output,
    }


def get_current_revision() -> str | None:
    """Возвращает текущую ревизию alembic из БД."""
    result = subprocess.run(
        ["python", "-m", "alembic", "current"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout + result.stderr).strip()
    for line in output.splitlines():
        line = line.strip()
        if line and not line.startswith("INFO"):
            return line
    return None
