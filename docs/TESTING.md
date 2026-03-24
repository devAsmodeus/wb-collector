# Тестирование

## Требования

- PostgreSQL (тестовая БД `wb_collector_test`)
- Python 3.12+
- pytest, pytest-asyncio

## Настройка тестовой БД

```bash
# Создать тестовую базу (один раз)
docker compose exec postgres psql -U wb_user -c "CREATE DATABASE wb_collector_test;"
```

## Запуск тестов

```bash
# Все тесты
MODE=TEST pytest tests/ -v

# Только модели
MODE=TEST pytest tests/test_models/ -v

# Только репозитории
MODE=TEST pytest tests/test_repositories/ -v

# Только задачи
MODE=TEST pytest tests/test_tasks/ -v

# С покрытием
MODE=TEST pytest tests/ --cov=src --cov-report=term-missing
```

## Структура тестов

```
tests/
├── conftest.py                      # Фикстуры: PostgreSQL engine, session, client
├── test_health.py                   # GET /health → 200
├── test_models/
│   └── test_models_exist.py         # Все ORM-модели имеют __tablename__
├── test_repositories/
│   ├── test_cards_repository.py     # CardsRepository upsert/query
│   └── test_fbs_orders_repository.py # FbsOrdersRepository upsert/query
└── test_tasks/
    └── test_tasks_registered.py     # Все 25 задач импортируются, retry=3
```

## Тестовая БД

Тесты используют отдельную PostgreSQL БД `wb_collector_test` на том же сервере.
- Таблицы создаются перед запуском тестов (`Base.metadata.create_all`)
- Удаляются после (`Base.metadata.drop_all`)
- Каждый тест работает в транзакции с rollback
