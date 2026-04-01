# WB Collector — Инструкция для Claude

## ⚠️ ГЛАВНОЕ ПРАВИЛО: сначала документация, потом код

**ВСЕГДА** перед любыми изменениями, отладкой или написанием нового кода:

### 1. Открой YAML-документацию WB API из папки `docs/api/`

В проекте лежат **актуальные OpenAPI-спецификации** Wildberries (скачаны 2026-03-24):

```
docs/api/
├── manifest.json              # Список файлов, эндпоинтов, хешей
├── 01-general.yaml            # Общие (ping, seller-info, news, users)
├── 02-products.yaml           # Товары (карточки, цены, справочники, склады, теги, медиа)
├── 03-orders-fbs.yaml         # FBS (сборочные задания, поставки, пропуска)
├── 04-orders-dbw.yaml         # DBW (доставка на склад WB)
├── 05-orders-dbs.yaml         # DBS (доставка силами продавца)
├── 06-in-store-pickup.yaml    # Самовывоз (Click & Collect)
├── 07-orders-fbw.yaml         # FBW (склады WB, поставки, приёмка)
├── 08-promotion.yaml          # Продвижение (кампании, ставки, акции, статистика)
├── 09-communications.yaml     # Коммуникации (чаты, отзывы, вопросы, претензии)
├── 10-tariffs.yaml            # Тарифы (комиссии, короба, паллеты, поставки)
├── 11-analytics.yaml          # Аналитика (воронка, отчёты, поиск, остатки)
├── 12-reports.yaml            # Отчёты (остатки, заказы, продажи, акцизы, хранение)
└── 13-finances.yaml           # Финансы (баланс, отчёт, документы)
```

**Как использовать:**
```bash
# Прочитать документацию по конкретному разделу:
Read docs/api/03-orders-fbs.yaml

# Найти конкретный эндпоинт:
Grep "/api/v3/orders" docs/api/03-orders-fbs.yaml

# Посмотреть параметры эндпоинта:
Grep "dateFrom\|next\|limit\|offset" docs/api/03-orders-fbs.yaml
```

### 2. Только после изучения YAML — пиши код

- Проверь **параметры** (query, path, body) — какие обязательные, какие опциональные
- Проверь **формат данных** — типы полей в ответе (string, integer, object)
- Проверь **URL эндпоинта** — он мог измениться

### 3. При необходимости — проверь реальные данные через наш прокси

```bash
docker exec wb_app python -c "
import httpx
r = httpx.get('http://127.0.0.1:8000/{наш_путь}', timeout=30)
print(r.status_code, r.text[:500])
"
```

### 4. НЕ ГАДАЙ, НЕ ИЩИ В ИНТЕРНЕТЕ

Вся документация WB API уже в проекте. Не используй dev.wildberries.ru, веб-поиск или свои знания о WB API — **читай YAML-файлы**.

---

## Архитектура проекта

```
wb-collector/
├── src/
│   ├── api/                    # Litestar контроллеры (роутеры)
│   │   └── {section}/
│   │       ├── wb/             # Прокси к WB API (tags: "XX. API Wildberries")
│   │       ├── sync/           # Синхронизация WB → PostgreSQL (tags: "XX. Синхронизация")
│   │       └── db/             # Чтение из локальной БД (tags: "XX. База данных")
│   ├── collectors/             # HTTP-клиенты к WB API (httpx)
│   ├── services/               # Бизнес-логика (sync, wb, db)
│   ├── repositories/           # Работа с БД (SQLAlchemy upsert/select)
│   ├── models/                 # ORM-модели (SQLAlchemy Mapped)
│   ├── schemas/                # Pydantic-схемы (валидация ответов WB)
│   ├── plugins/scalar.py       # Scalar API Reference UI с кастомным sidebar
│   ├── config.py               # Pydantic Settings из .env
│   ├── exceptions.py           # Обработка ошибок WB API (тематические)
│   ├── database.py             # SQLAlchemy async engine
│   ├── tasks/                  # Celery задачи
│   └── main.py                 # Точка входа Litestar
├── docker-compose.yml
├── .env                        # Настройки (токены, БД, Redis)
└── CLAUDE.md                   # ← Этот файл
```

### Поток данных

```
WB API  →  Collector (httpx)  →  Service  →  Repository  →  PostgreSQL
                                    ↑
                            API Controller (Litestar)
                                    ↑
                              HTTP запрос (/sync/full)
```

---

## Разделы API (13 + System)

| № | Группа (sidebar) | Описание | Подразделы |
|---|-------------------|----------|------------|
| — | Система | `GET /health` | — |
| 01 | Общие | Продавец, новости | WB / Sync / DB |
| 02 | Товары | Карточки, цены, справочники, склады, теги, медиа | WB / Sync / DB |
| 03 | FBS | Сборочные задания FBS (заказы, поставки, пропуска) | WB / Sync / DB |
| 04 | DBW | Доставка на склад WB | WB / Sync / DB |
| 05 | DBS | Доставка силами продавца | WB / Sync / DB |
| 06 | Самовывоз | Заказы самовывоза (Pickup / Click & Collect) | WB / Sync / DB |
| 07 | FBW | Склады WB (поставки, приёмка) | WB / Sync / DB |
| 08 | Продвижение | Рекламные кампании, ставки, акции, статистика | WB / Sync / DB |
| 09 | Коммуникации | Чаты, отзывы, вопросы, претензии, закрепы | WB / Sync / DB |
| 10 | Тарифы | Комиссии, тарифы коробов, паллетов, поставок | WB / Sync / DB |
| 11 | Аналитика | Воронка продаж, отчёты по артикулам, поиск, остатки | WB / Sync / DB |
| 12 | Отчёты | Остатки, заказы, продажи, акцизы, хранение, штрафы | WB / Sync / DB |
| 13 | Финансы | Баланс, финансовый отчёт, документы | WB / Sync / DB |

Каждый подраздел:
- **API Wildberries** — прямой прокси к WB API
- **Синхронизация** — загрузка данных из WB API в PostgreSQL
- **База данных** — чтение сохранённых данных из PostgreSQL

---

## WB API хосты (src/config.py)

| Настройка | URL | Разделы |
|-----------|-----|---------|
| WB_API_BASE_URL | `common-api.wildberries.ru` | Общие, Тарифы |
| WB_CONTENT_URL | `content-api.wildberries.ru` | Товары (карточки) |
| WB_PRICES_URL | `discounts-prices-api.wildberries.ru` | Товары (цены) |
| WB_MARKETPLACE_URL | `marketplace-api.wildberries.ru` | FBS, DBW, DBS, Pickup |
| WB_SUPPLIES_URL | `supplies-api.wildberries.ru` | FBW (поставки, приёмка) |
| WB_STATS_URL | `statistics-api.wildberries.ru` | Отчёты, Финансовый отчёт |
| WB_RETURNS_URL | `returns-api.wildberries.ru` | Коммуникации (претензии) |
| WB_ANALYTICS_URL | `seller-analytics-api.wildberries.ru` | Аналитика |
| WB_ADVERT_URL | `advert-api.wildberries.ru` | Продвижение |
| WB_FEEDBACKS_URL | `feedbacks-api.wildberries.ru` | Коммуникации (отзывы, вопросы) |
| WB_FINANCE_URL | `finance-api.wildberries.ru` | Финансы (баланс, документы) |

---

## Инфраструктура (docker-compose.yml)

| Сервис | Контейнер | Порт (снаружи → внутри) |
|--------|-----------|-------------------------|
| PostgreSQL 16 | wb_postgres | **5434** → 5432 |
| Redis | wb_redis | 6379 → 6379 |
| App (Litestar/Uvicorn) | wb_app | — (через nginx) |
| Nginx | wb_nginx | **8080** → 8000 |
| Celery Worker | wb_celery | — |
| Celery Beat | wb_celery_beat | — |
| Prometheus | wb_prometheus | 9090 → 9090 |
| Grafana | wb_grafana | 3000 → 3000 |

### Важно про порты:
- **Внутри Docker-сети** app подключается к postgres на порту `5432` (переменная `DB_PORT=5432` в docker-compose environment)
- **Снаружи** (PyCharm, DBeaver) подключение на порту **`5434`** (потому что локальный PostgreSQL занял 5432)
- **API доступен** по `http://localhost:8080` (через nginx) или `http://localhost:8000` (если порт пробрасывать напрямую)

### Подключение к БД из PyCharm:
```
Host: localhost
Port: 5434
Database: wb_collector
User: wb_user
Password: wb_pass
```

---

## Текущее состояние данных в БД

### ✅ Работающие

| Таблица | Записей | Примечание |
|---------|---------|------------|
| sellers | 1 | ✅ full + incremental |
| wb_news | 793 | ✅ full + incremental |
| wb_cards | 15 | ✅ |
| wb_prices | 1155 | ✅ |
| wb_tags | 1 | ✅ |
| wb_seller_warehouses | 6 | ✅ |
| wb_categories | 82 | ✅ |
| wb_subjects | 1000 | ✅ |
| wb_tariffs_commission | 7373 | ✅ |
| wb_campaigns | — | ✅ sync работает |
| wb_campaign_stats | — | ✅ sync работает |

### 🔧 Исправлены (код написан, нужно протестировать в Docker)

| Таблица | Что исправлено | Статус |
|---------|---------------|--------|
| wb_tariffs_box | `field_validator` для `"0,07"` → `Decimal` | 🔧 код готов |
| wb_tariffs_pallet | `field_validator` аналогично box | 🔧 код готов |
| wb_tariffs_supply | URL → `/api/tariffs/v1/acceptance/coefficients` | 🔧 код готов |
| fbs_orders | Cursor: `response.next` вместо `last.id` | 🔧 код готов |
| dbw_orders | Добавлен `dateTo = int(now.timestamp())` | 🔧 код готов |
| dbs_orders | Добавлен `dateTo` | 🔧 код готов |
| pickup_orders | Добавлен `dateTo` | 🔧 код готов |
| wb_feedbacks | Timeout увеличен, limit уменьшен | 🔧 код готов |
| wb_questions | `skip < 10000` ограничение | 🔧 код готов |
| wb_claims | Хост → `returns-api`, params → `limit`/`offset` | 🔧 код готов |
| wb_financial_report | Хост → `statistics-api.wildberries.ru` | 🔧 код готов |
| wb_orders_report | Улучшен dateFrom, маппинг полей, схемы | 🔧 код готов |
| wb_sales_report | Аналогично orders_report | 🔧 код готов |
| wb_stocks | Аналогично orders_report | 🔧 код готов |

### 🆕 Созданы новые модули (код написан, нужно протестировать)

| Раздел | Что создано | Статус |
|--------|------------|--------|
| FBW | Модели, репозитории, сервисы, контроллеры: склады, поставки, транзитные тарифы | 🔧 код готов |
| Аналитика | Модели, репозитории, сервисы, контроллеры: воронка, поиск, остатки | 🔧 код готов |
| Продвижение | Calendar sync добавлен | 🔧 код готов |

---

## Правила написания кода

### Pydantic-first: валидация на входе

**КАЖДЫЙ** метод коллектора ОБЯЗАН возвращать Pydantic-модель, а не `dict`/`list`:
```python
# ❌ ПЛОХО — возвращает dict:
async def get_box_tariffs(self, date: str) -> dict:
    return await self._client.get("/api/v1/tariffs/box", params={"date": date})

# ✅ ХОРОШО — сразу валидация:
async def get_box_tariffs(self, date: str) -> BoxTariffsResponse:
    data = await self._client.get("/api/v1/tariffs/box", params={"date": date})
    return BoxTariffsResponse.model_validate(data)
```

Конвертация грязных данных WB — через `field_validator` в Pydantic-схеме:
```python
from decimal import Decimal
from pydantic import BaseModel, field_validator

class BoxTariffItem(BaseModel):
    boxDeliveryBase: Decimal | None = None
    boxDeliveryLiter: Decimal | None = None

    @field_validator("boxDeliveryBase", "boxDeliveryLiter", mode="before")
    @classmethod
    def parse_wb_decimal(cls, v):
        """WB возвращает числа как строки: '0,07', '46', '-'"""
        if v is None or v == "-" or v == "":
            return None
        return Decimal(str(v).replace(",", "."))
```

### DB-эндпоинты: total + пагинация

Все DB-сервисы ОБЯЗАНЫ возвращать `total` (общее кол-во в БД) и параметры пагинации:
```python
# Репозиторий — метод count():
async def count(self) -> int:
    result = await self._session.execute(select(func.count()).select_from(Model))
    return result.scalar_one()

# DB-сервис — формат ответа:
return {"data": [...], "total": total, "limit": limit, "offset": offset}
```

### Инкрементальная синхронизация

Каждый sync-раздел ОБЯЗАН иметь два эндпоинта:
- `POST /full` — полная выгрузка
- `POST /incremental` — от последней записи в БД

```python
# Репозиторий:
async def get_max_cursor(self) -> int | datetime | None:
    result = await self._session.execute(select(func.max(Model.cursor_field)))
    return result.scalar_one_or_none()

# Сервис:
async def sync_incremental(self, session):
    repo = Repository(session)
    cursor = await repo.get_max_cursor()
    if not cursor:
        return await self.sync_full(session)  # fallback
    # загрузка от cursor ...
    return {"synced": N, "source": "incremental", "from_cursor": cursor}
```

---

## Незавершённые задачи (TODO)

### ✅ Этап 1: Починить сломанные sync — ВЫПОЛНЕНО (2026-04-01)

1. ~~**Tariffs box/pallet** — `field_validator` для `"0,07"` → `Decimal`~~ ✅
2. ~~**Tariffs supply** — URL → `/api/tariffs/v1/acceptance/coefficients`~~ ✅
3. ~~**Claims** — хост → `returns-api`, params → `limit`/`offset`~~ ✅
4. ~~**Finances** — хост → `statistics-api.wildberries.ru`~~ ✅
5. ~~**Reports (stocks/orders/sales)** — формат dateFrom, Pydantic-схемы~~ ✅
6. ~~**Feedbacks** — timeout 120s, limit 50~~ ✅
7. ~~**Questions** — `skip < 10000`~~ ✅
8. ~~**FBS orders** — cursor: `response.next`~~ ✅
9. ~~**DBW/DBS/Pickup** — `dateTo = int(now.timestamp())`~~ ✅

### ✅ Этап 2: Pydantic-first + DB total — ВЫПОЛНЕНО (2026-04-01)

10. ~~**Все коллекторы** → Pydantic-модели (tariffs полностью, остальные частично)~~ ✅
11. ~~**Все репозитории** → `count()` метод~~ ✅
12. ~~**Все DB-сервисы** → `{"data": [...], "total": N, "limit": N, "offset": N}`~~ ✅

### ✅ Этап 3: Инкрементальная синхронизация — ВЫПОЛНЕНО (2026-04-01)

13. ~~**Все sync-контроллеры** → `POST /incremental`~~ ✅
14. ~~**Все репозитории** → `get_max_cursor()`~~ ✅
15. ~~**Все sync-сервисы** → `sync_incremental()`~~ ✅

### ✅ Этап 4: Новые sync/DB слои — ВЫПОЛНЕНО (2026-04-01)

16. ~~**FBW** — склады, поставки, транзитные тарифы~~ ✅
17. ~~**Аналитика** — воронка, поиск, остатки~~ ✅
18. ~~**Продвижение** — calendar sync~~ ✅

### ✅ Этап 5 (частично): Инфраструктура

19. **Unique constraints** — ❌ нужно проверить все таблицы
20. **raw_data JSONB** — ❌ нужно добавить во все модели
21. ~~**Scalar sidebar** — кастомный JS плагин~~ ✅
22. **Celery workers** — ✅ 27 задач добавлено (предыдущий коммит)

---

## Оставшиеся задачи (TODO)

### 🔴 Приоритет 1: Тестирование в Docker

Весь код этапов 1-4 написан, но **не протестирован в рабочем Docker-окружении**.
Нужно запустить `docker-compose up -d --build` и проверить каждый sync-эндпоинт:

```bash
# Тарифы
curl -X POST http://localhost:8080/tariffs/sync/box/full
curl -X POST http://localhost:8080/tariffs/sync/pallet/full
curl -X POST http://localhost:8080/tariffs/sync/supply/full

# Заказы
curl -X POST http://localhost:8080/fbs/sync/orders/full
curl -X POST http://localhost:8080/dbw/sync/orders/full
curl -X POST http://localhost:8080/dbs/sync/orders/full
curl -X POST http://localhost:8080/pickup/sync/orders/full

# Коммуникации
curl -X POST http://localhost:8080/communications/sync/claims/full
curl -X POST http://localhost:8080/communications/sync/feedbacks/full
curl -X POST http://localhost:8080/communications/sync/questions/full

# Отчёты и финансы
curl -X POST http://localhost:8080/reports/sync/reports/full
curl -X POST http://localhost:8080/finances/sync/finances/full

# Новые модули
curl -X POST http://localhost:8080/fbw/sync/warehouses/full
curl -X POST http://localhost:8080/fbw/sync/supplies/full
curl -X POST http://localhost:8080/analytics/sync/funnel/full
curl -X POST http://localhost:8080/analytics/sync/search/full
curl -X POST http://localhost:8080/analytics/sync/stocks/full
```

### 🟡 Приоритет 2: Pydantic-first для всех коллекторов

Tariffs коллектор полностью переведён на Pydantic-модели. Остальные коллекторы частично используют `dict`. Нужно:
- Создать Pydantic-схемы ответов для всех оставшихся коллекторов
- Заменить `-> dict` на `-> ResponseModel` в методах коллекторов

### 🟠 Приоритет 3: Целостность БД

19. **Unique constraints** — проверить все таблицы, добавить недостающие для `ON CONFLICT DO UPDATE`
20. **raw_data JSONB** — добавить во все модели для сохранения сырого ответа WB

### 🟢 Приоритет 4: Алембик миграции

- Сейчас таблицы создаются через `create_all()` — нужно перейти на Alembic
- Написать initial migration от текущей схемы

---

## Обработка ошибок WB API

Ответы от WB парсятся автоматически (src/exceptions.py):
```json
{
  "error": "wb_brands_api_error",
  "status_code": 404,
  "wb_response": {
    "title": "Not Found",
    "detail": "Brands not found",
    "requestId": "c83132d4-...",
    "origin": "brands-api"
  }
}
```
- Имя ошибки извлекается из поля `origin` ответа WB
- Полный JSON от WB возвращается как объект в `wb_response`, не как строка
- Если WB вернул не-JSON — fallback в поле `detail`

---

## Ограничения PostgreSQL (asyncpg)

1. **Максимум 32767 параметров** в одном INSERT → используй `_batched_upsert` (см. `src/repositories/tariffs/tariffs.py`)
2. **Unique constraints обязательны** для `ON CONFLICT DO UPDATE`
3. **WB возвращает числа как строки** (`"0,07"`, `"46"`, `"-"`) — конвертация через `field_validator` в Pydantic-схеме (см. "Правила написания кода" выше), НЕ хелперы в репозитории

---

## Как запускать

```bash
# Полный запуск
docker-compose up -d

# Только app (rebuild)
docker-compose up -d --build app

# Тест всех sync-эндпоинтов
docker exec wb_app python -c "
import httpx
client = httpx.Client(base_url='http://127.0.0.1:8000', timeout=300)
r = client.post('/general/sync/seller/full', json={})
print(r.status_code, r.text[:200])
"

# Проверка данных в БД
docker exec wb_postgres psql -U wb_user -d wb_collector -c "SELECT count(*) FROM wb_prices;"

# Логи app
docker logs wb_app --tail 50
```

---

## Как отлаживать 500 ошибки

Litestar скрывает трейсбеки от клиента. Чтобы увидеть реальную ошибку:
```bash
docker exec wb_app python -c "
import asyncio
from src.services.{section}.sync.{module} import {ServiceClass}
from src.utils.db_manager import DBManager

async def test():
    try:
        async with DBManager() as db:
            result = await {ServiceClass}().{method}(db.session)
            print('OK:', result)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(test())
"
```
