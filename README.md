# WB Collector

Сервис сбора, хранения и проксирования данных из API Wildberries для проекта DiRetail.

---

## Документация

| Файл | Описание |
|------|----------|
| [docs/API_METHODS.md](docs/API_METHODS.md) | Все эндпоинты по разделам |
| [docs/SCHEDULE.md](docs/SCHEDULE.md) | Celery Beat расписание |
| [docs/MONITORING.md](docs/MONITORING.md) | Grafana, Prometheus, Loki |
| [docs/BACKUP.md](docs/BACKUP.md) | Резервное копирование PostgreSQL |
| [docs/TESTING.md](docs/TESTING.md) | Запуск тестов |
| [CLAUDE.md](CLAUDE.md) | Инструкция для AI-агентов |

---

## Архитектура

```
┌─────────────────────────────────────────┐
│         Litestar REST API               │
│  /general /products /fbs /fbw ...       │
└─────────────────────┬───────────────────┘
                      │
┌─────────────────────▼───────────────────┐
│              Services                    │
│  sync/* — забрать из WB и сохранить     │
│  db/*   — читать из БД                  │
│  wb/*   — проксировать запрос в WB      │
└──────────┬──────────────────────────────┘
           │
    ┌──────▼──────┐   ┌─────────────────┐
    │  Collectors  │   │  Repositories   │
    │ HTTP → WB API│   │  CRUD → Postgres│
    └──────────────┘   └─────────────────┘
           │
    ┌──────▼──────────────────────────────┐
    │  WB API (13 разделов)               │
    │  + Redis (кеш) + Celery (фоновые)  │
    └─────────────────────────────────────┘
```

---

## Разделы API

| # | Раздел | Префикс | Таблицы БД |
|---|--------|---------|------------|
| 01 | General | `/general` | `sellers`, `news`, `users` |
| 02 | Products | `/products` | `cards`, `prices`, `tags`, `seller_warehouses`, `categories`, `subjects` |
| 03 | FBS | `/fbs` | `fbs_orders`, `fbs_passes`, `fbs_supplies` |
| 04 | DBW | `/dbw` | `dbw_orders` |
| 05 | DBS | `/dbs` | `dbs_orders` |
| 06 | Pickup | `/pickup` | `pickup_orders` |
| 07 | FBW | `/fbw` | `fbw_supplies`, `fbw_supply_goods`, `fbw_warehouses`, `fbw_transit_tariffs` |
| 08 | Promotion | `/promotion` | `campaigns`, `campaign_stats`, `promotions` |
| 09 | Communications | `/communications` | `feedbacks`, `questions`, `claims`, `chats` |
| 10 | Tariffs | `/tariffs` | `tariffs_commission`, `tariffs_box`, `tariffs_pallet`, `tariffs_supply` |
| 11 | Analytics | `/analytics` | `analytics_funnel_products`, `analytics_stocks_groups`, `analytics_search_queries` |
| 12 | Reports | `/reports` | `orders_report`, `sales_report`, `stocks` |
| 13 | Finances | `/finances` | `financial_report` |

---

## Быстрый старт

### Требования
- Docker + Docker Compose

### Запуск

```bash
git clone https://github.com/devAsmodeus/wb-collector.git
cd wb-collector
cp .env.example .env
# Заполнить .env (токен WB, настройки БД)
docker compose up -d
```

Swagger UI: `http://localhost:8080/docs`

### Переменные окружения

| Переменная | Обязательна | Описание |
|-----------|-------------|----------|
| `WB_API_TOKEN` | ✅ | Токен WB API (JWT, 180 дней) |
| `DB_HOST` | ✅ | Хост PostgreSQL |
| `DB_PORT` | ✅ | Порт PostgreSQL (по умолчанию 5432) |
| `DB_USER` | ✅ | Пользователь БД |
| `DB_PASS` | ✅ | Пароль БД |
| `DB_NAME` | ✅ | Имя базы данных |
| `REDIS_HOST` | ✅ | Хост Redis |
| `REDIS_PORT` | ✅ | Порт Redis (по умолчанию 6379) |

### Получение токена WB API

1. Войти на [seller.wildberries.ru](https://seller.wildberries.ru)
2. Настройки → Доступ к API → Создать новый токен
3. Выбрать нужные разрешения (минимум: Цены и скидки, Статистика, Аналитика, Финансы)
4. Токен действует 180 дней

---

## Инфраструктура

| Сервис | Контейнер | Порт |
|--------|-----------|------|
| Litestar API | `wb_app` | 8080 (через nginx) |
| PostgreSQL | `wb_postgres` | 5434 (внешний) |
| Redis | `wb_redis` | 6379 |
| Celery Worker | `wb_celery` | — |
| Celery Beat | `wb_celery_beat` | — |
| Nginx | `wb_nginx` | 8080 |
| Grafana | `wb_grafana` | 3000 |
| Prometheus | `wb_prometheus` | 9090 |

---

## Паттерны эндпоинтов

Каждый раздел содержит три типа эндпоинтов:

### `/sync/*` — синхронизация WB → БД
```
POST /{раздел}/sync/{сущность}/full         — полная выгрузка (может быть Celery)
POST /{раздел}/sync/{сущность}/incremental  — только новые данные
```

### `/db/*` — чтение из БД
```
GET /{раздел}/db/{сущность}?limit=100&offset=0
```
Всегда возвращает: `{ "data": [...], "total": N, "limit": N, "offset": N }`

### `/wb/*` — прямой прокси в WB API
```
GET|POST|PUT|DELETE /{раздел}/wb/{путь}
```
Возвращает ответ WB как есть.
