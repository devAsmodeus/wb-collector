"""Основная логика синхронизации документации."""
import subprocess
from datetime import datetime
from pathlib import Path

from tools.sync_docs.fetcher  import DOCS, DOCS_DIR, fetch, save
from tools.sync_docs.manifest import load as load_manifest, save as save_manifest, build_entry
from tools.sync_docs.differ   import extract_semantics, diff, has_changes
from tools.sync_docs.notifier import format_report

REPO_DIR = Path(__file__).parent.parent.parent


def _git(*args) -> tuple[int, str]:
    r = subprocess.run(
        ["git"] + list(args), cwd=REPO_DIR,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return r.returncode, (r.stdout + r.stderr).strip()


def _git_commit(changed_names: list[str], summary: str) -> str:
    log = []
    code, out = _git("add", "docs/api/")
    log.append("git add: ok" if code == 0 else f"git add err: {out}")

    date_str   = datetime.now().strftime("%Y-%m-%d")
    commit_msg = (
        f"docs: update WB API specs [{date_str}]\n\n"
        f"Changed: {', '.join(changed_names)}\n\n{summary[:400]}"
    )
    code, out = _git("commit", "-m", commit_msg)
    if code != 0 and "nothing to commit" in out:
        return "git: нечего коммитить"
    log.append(f"git commit: {out.splitlines()[0] if out else 'ok'}")

    code, out = _git("push", "origin", "main")
    log.append("git push: ok" if code == 0 else f"git push FAILED: {out[:200]}")
    return " | ".join(log)


def run() -> dict:
    """
    Полный цикл синхронизации:
    1. Скачиваем YAML
    2. Сравниваем с манифестом (хэш + семантика)
    3. Отправляем уведомление
    4. Сохраняем манифест ТОЛЬКО ПОСЛЕ успешной отправки

    Важно: манифест сохраняется в конце, чтобы при падении задачи
    следующий запуск снова нашёл те же изменения (idempotent retry).
    """
    old_entries = load_manifest()
    new_entries = []
    changed     = []   # [(name, label, diff_dict)]
    errors      = []
    new_texts   = {}   # {name: text} — храним для save() после уведомления

    for name, label in DOCS:
        filename = f"{name}.yaml"

        new_text = fetch(name)
        if new_text is None:
            errors.append(filename)
            if old_entries.get(filename):
                new_entries.append(old_entries[filename])
            continue

        new_sem   = extract_semantics(new_text)
        old_entry = old_entries.get(filename, {})
        old_sem   = old_entry.get("semantics", {}) if isinstance(old_entry, dict) else {}

        new_entries.append(build_entry(filename, new_text, new_sem))
        new_texts[name] = new_text

        if old_sem:
            d = diff(old_sem, new_sem)
            if has_changes(d):
                changed.append((name, label, d))

    report = format_report(changed, len(DOCS), errors)

    # Уведомление в Telegram
    tg_ok = False
    try:
        from tools.telegram import send as tg_send
        tg_ok = tg_send(report)
    except Exception:
        pass

    # Сохраняем YAML и манифест только после отправки уведомления.
    # Если уведомление не ушло — манифест не обновляем, следующий запуск
    # снова обнаружит те же изменения.
    if tg_ok or not changed:
        for name, text in new_texts.items():
            save(name, text)
        save_manifest(new_entries)

        if changed:
            changed_names = [name for name, _, _ in changed]
            try:
                _git_commit(changed_names, report[:500])
            except Exception:
                pass  # git недоступен в контейнере — не критично

    return {
        "status":        "changed" if changed else "ok",
        "report":        report,
        "changed_count": len(changed),
        "errors":        errors,
        "tg_sent":       tg_ok,
        "changed_files": [name for name, _, _ in changed],
    }
