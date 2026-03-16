# wb-collector

Сбор и хранение данных Wildberries API — DiRetail.

## Запуск

```bash
# 1. Скопировать и заполнить .env
cp .env.example .env

# 2. Поднять PostgreSQL + Redis
docker-compose up -d postgres redis

# 3. Применить миграции
alembic upgrade head

# 4. Запустить приложение
uvicorn src.main:app --reload

# 5. Запустить Celery (в отдельном терминале)
celery -A src.tasks.celery_app worker --loglevel=info
celery -A src.tasks.celery_app beat --loglevel=info
```

## Структура

```
src/
├── api/           — FastAPI роутеры
├── collectors/    — HTTP-клиенты WB API (по главам)
├── models/        — SQLAlchemy модели
├── repositories/  — доступ к БД
├── schemas/       — Pydantic схемы
├── services/      — бизнес-логика
├── tasks/         — Celery задачи
└── utils/         — DBManager и утилиты

docs/api/          — YAML-документация WB API (13 глав)
scripts/           — вспомогательные скрипты
```

## API-документация WB

Автоматически обновляется каждый день в 08:00 через `scripts/sync_docs.py`.
