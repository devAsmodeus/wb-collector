# Бэкапы PostgreSQL

## Автоматический бэкап

Контейнер `backup` в docker-compose выполняет `pg_dump` каждые 24 часа.

- **Формат:** `wb_collector_YYYYMMDD_HHMMSS.sql.gz` (gzip)
- **Расположение:** `./backups/` (volume на хосте)
- **Retention:** 7 дней (старые бэкапы удаляются автоматически)

## Ручной бэкап

```bash
docker compose exec backup /scripts/backup.sh
```

## Восстановление

```bash
# Список доступных бэкапов
docker compose run --rm backup ls /backups/

# Восстановить из конкретного дампа
docker compose run --rm backup /scripts/restore.sh wb_collector_20260324_030000.sql.gz
```

> **Внимание:** restore.sh полностью перезаписывает текущую БД. Перед восстановлением убедитесь, что остановили app и celery.

## Конфигурация

Переменные окружения для backup-контейнера (из `.env`):

| Переменная | По умолчанию | Описание |
|-----------|-------------|----------|
| DB_HOST | postgres | Хост PostgreSQL |
| DB_PORT | 5432 | Порт |
| DB_USER | wb_user | Пользователь |
| DB_PASS | wb_pass | Пароль |
| DB_NAME | wb_collector | Имя БД |
