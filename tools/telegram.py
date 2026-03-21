"""Отправка уведомлений в Telegram."""
import os
import ssl
import urllib.request
import json
from pathlib import Path

# Windows: обходим проблему с SSL-сертификатами
_ssl_ctx = ssl.create_default_context()
_ssl_ctx.check_hostname = False
_ssl_ctx.verify_mode    = ssl.CERT_NONE


def _load_env() -> dict:
    """Читает .env из корня проекта."""
    env = {}
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def send(text: str, token: str | None = None, chat_id: str | None = None) -> bool:
    """
    Отправляет сообщение в Telegram.
    Если token/chat_id не переданы — берёт из .env / os.environ.
    Возвращает True при успехе.
    """
    env = _load_env()
    token   = token   or os.environ.get("TELEGRAM_BOT_TOKEN")   or env.get("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")     or env.get("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return False

    # Telegram ограничение 4096 символов
    chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]

    for chunk in chunks:
        payload = json.dumps({
            "chat_id":    chat_id,
            "text":       chunk,
            "parse_mode": "HTML",
        }).encode("utf-8")

        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10, context=_ssl_ctx) as r:
                if r.status != 200:
                    return False
        except Exception:
            return False

    return True
