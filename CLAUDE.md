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

## Регламент работы с проектом (ОБЯЗАТЕЛЬНО)

### Три слоя для каждого раздела

| Слой | Назначение | Обязательные требования |
|------|-----------|------------------------|
| **api** | Полная копия методов WB API | Все GET/POST эндпоинты из документации, ничего не выдумываем |
| **sync** | Загрузка WB → PostgreSQL | `POST /full` + `POST /incremental` |
| **db** | Чтение из БД | Пагинация (offset/limit) + метод экспорта в Excel (макс 1 млн строк) |

### Порядок создания нового эндпоинта (СТРОГО ПО ШАГАМ)

1. **Документация** — прочитать `docs/api/*.yaml`, найти нужный эндпоинт, параметры, типы
2. **Таблица** — создать SQLAlchemy-модель. Поля и типы **идентичны** API (никаких выдумок)
3. **Ключи и индексы** — одинарные и составные (например, поставка + товар). **Если не уверен — спросить пользователя**
4. **Миграция** — применить Alembic миграцию
5. **API-эндпоинт** — клон WB API (прокси)
6. **Sync-эндпоинты** — full + incremental
7. **Первая полная выгрузка** — проверить что данные загружаются
8. **DB-эндпоинт** — пагинация (offset/limit) + Excel экспорт
9. **Кастомный UI** — добавить эндпоинт/главу в UI
10. **Периодическая задача** — Celery task для инкрементальной синхронизации (ежедневно/еженедельно)

### Ключевые принципы

- **Pydantic-first**: каждый коллектор возвращает Pydantic-модель, конвертация через `field_validator`
- **DB-сервисы**: всегда возвращают `{"data": [...], "total": N, "limit": N, "offset": N}`
- **Полная копия API**: все GET/POST эндпоинты из документации WB, не выдумываем своё
- **Поля БД = поля API**: столбцы и типы данных точно как в документации
- **При сомнениях — спрашивать пользователя**

---

## Именование таблиц в БД

**Правило: префикс соответствует разделу, а не проекту.**

Весь проект — это WB Collector, поэтому префикс `wb_` **не используется** как универсальный.
Вместо этого — раздел API:

| Раздел | Префикс таблицы | Примеры |
|--------|-----------------|---------|
| Общие (01) | `sellers`, `news` | `sellers`, `news` |
| Товары (02) | `cards_` / `prices_` / без префикса | `cards`, `prices`, `tags`, `categories`, `subjects` |
| FBS (03) | `fbs_` | `fbs_orders`, `fbs_supplies` |
| DBW (04) | `dbw_` | `dbw_orders` |
| DBS (05) | `dbs_` | `dbs_orders` |
| Самовывоз (06) | `pickup_` | `pickup_orders` |
| FBW (07) | `fbw_` | `fbw_supplies`, `fbw_warehouses`, `fbw_supply_goods` |
| Продвижение (08) | `campaigns_` / `promotion_` | `campaigns`, `campaign_stats`, `promotions` |
| Коммуникации (09) | `feedbacks`, `questions`, `claims`, `chats_` | прямо по имени сущности |
| Тарифы (10) | `tariffs_` | `tariffs_box`, `tariffs_pallet`, `tariffs_commission`, `tariffs_supply` |
| Аналитика (11) | `analytics_` | `analytics_funnel`, `analytics_stocks`, `analytics_search` |
| Отчёты (12) | `reports_` | `reports_orders`, `reports_sales`, `reports_stocks` |
| Финансы (13) | `financial_` | `financial_report`, `financial_balance` |

**❌ Плохо:** `wb_tariffs_box`, `wb_financial_report`, `wb_campaign_stats`
**✅ Хорошо:** `tariffs_box`, `financial_report`, `campaign_stats`

> Примечание: в текущей БД часть таблиц создана со старым префиксом `wb_` — при рефакторинге переименовать через Alembic.

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
| WB_COMMON_URL | `common-api.wildberries.ru` | Подписки Джем (`/api/common/v1/subscriptions`) |
| WB_CONTENT_URL | `content-api.wildberries.ru` | Товары (карточки) |
| WB_PRICES_URL | `discounts-prices-api.wildberries.ru` | Товары (цены) |
| WB_MARKETPLACE_URL | `marketplace-api.wildberries.ru` | FBS, DBW, DBS, Pickup |
| WB_SUPPLIES_URL | `supplies-api.wildberries.ru` | FBW (поставки, приёмка) |
| WB_STATS_URL | `statistics-api.wildberries.ru` | Отчёты, Финансовый отчёт |
| WB_RETURNS_URL | `returns-api.wildberries.ru` | Коммуникации (претензии) |
| WB_ANALYTICS_URL | `seller-analytics-api.wildberries.ru` | Аналитика |
| WB_ADVERT_URL | `advert-api.wildberries.ru` | Продвижение (кампании, статистика) |
| WB_CALENDAR_URL | `dp-calendar-api.wildberries.ru` | Продвижение (календарь акций) |
| WB_FEEDBACKS_URL | `feedbacks-api.wildberries.ru` | Коммуникации (отзывы, вопросы), Рейтинг |
| WB_FINANCE_URL | `finance-api.wildberries.ru` | Финансы (баланс, документы) |

> ⚠️ Некоторые эндпоинты WB меняют хост без предупреждения (пример: calendar переехал с `advert-api` на `dp-calendar-api`). Всегда проверяй `servers:` в YAML перед написанием коллектора.

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
- **Снаружи** (PyCharm, DBeaver) подключение зависит от `.env`: если `DB_PORT=5432` → порт `5432`, если `DB_PORT=5434` → порт `5434`
- **API доступен** по `http://localhost:8080` (через nginx) или `http://localhost:8000` (если порт пробрасывать напрямую)

### Подключение к БД из PyCharm:

1. **Database** → **+** → **Data Source** → **PostgreSQL**
2. Заполнить:
   ```
   Host: localhost
   Port: 5432        (или 5434 — смотри DB_PORT в .env)
   Database: wb_collector
   User: wb_user
   Password: wb_pass
   ```
3. **Test Connection** → должно быть ✅
4. **Schemas** → отметить `public`
5. **Apply** → **OK**

> Если порт 5432 занят локальным PostgreSQL — поменяй `DB_PORT=5434` в `.env` и пересоздай контейнер: `docker compose up -d wb_postgres`

### Подключение к БД из DBeaver:

1. **New Connection** → **PostgreSQL**
2. Те же параметры: `localhost:5432`, `wb_collector`, `wb_user` / `wb_pass`
3. **Test Connection** → **Finish**

---

## Деплой изменений (ТОЛЬКО ТАК)

**Никогда не использовать `docker compose build --no-cache`** — пересобирает весь образ, долго.

```powershell
# Скопировать изменённые файлы в контейнер:
docker cp src\services\general\sync\seller.py wb_app:/app/src/services/general/sync/seller.py

# Перезапустить app:
docker restart wb_app

# Дождаться старта (15-20 сек):
Start-Sleep 18

# Проверить:
Invoke-WebRequest -Uri "http://localhost:8080/general/sync/seller/full" -Method POST -Headers @{Authorization="Bearer $token"} -UseBasicParsing
```

> ⚠️ **PowerShell**: используй `;` вместо `&&` для цепочки команд — `&&` не поддерживается.
> ⚠️ **Celery**: после изменений в `src/tasks/` нужно также перезапустить `wb_celery` и `wb_celery_beat`.

---

## Тяжёлые синхронизации — только через Celery

**Nginx timeout: ~60 секунд.** HTTP-эндпоинт вернёт 502/504 если синк занимает больше.

Правило:
- **HTTP `/sync/full`** — только если данных мало и укладывается в 60 сек
- **Celery task** — для всего что может занять > 30 сек (финансы, статистика кампаний, исторические выгрузки)

HTTP-эндпоинт для тяжёлых задач должен **сразу возвращать `task_id`**:
```python
@post("/sync/full")
async def sync_full(self) -> dict:
    task = sync_heavy_task.delay()
    return {"task_id": task.id, "status": "queued"}
```

**Известные тяжёлые задачи:**
- Финансовый отчёт — исторический за 2 года (~4 часа)
- Статистика кампаний — 1113 кампаний × 21с паузы = ~24 минуты (rate limit: 3 req/min)
- Исторические отзывы — 116k записей (~6 часов)

---

## Celery: правильный run_async

В Celery ForkPoolWorker дочерний процесс наследует event loop от родителя.
`asyncio.run()` не работает корректно с httpx и asyncpg в этом случае.

**Правильный паттерн (`src/tasks/tasks.py`):**
```python
def run_async(coro):
    """Запускает корутину в синхронном контексте Celery (ForkPoolWorker)."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        try:
            loop.run_until_complete(loop.shutdown_asyncgens())
        except Exception:
            pass
        loop.close()
        asyncio.set_event_loop(None)
```

**❌ Не использовать:**
```python
return asyncio.run(coro)  # ломается с "attached to a different loop"
```

---

## Текущее состояние данных в БД (2026-04-03)

| Таблица | Строк | Статус |
|---------|-------|--------|
| sellers | 1 | ✅ |
| news | 100+ | ✅ |
| cards | 15 | ✅ |
| prices | 1155 | ✅ |
| tags | 1 | ✅ |
| seller_warehouses | 6 | ✅ |
| categories | 83 | ✅ |
| subjects | 1000 | ✅ |
| fbs_orders | 214 | ✅ |
| fbw_supplies | 816 | ✅ |
| fbw_supply_goods | ~идёт загрузка | ⏳ Celery task |
| fbw_transit_tariffs | 100 | ✅ |
| tariffs_commission | 7391 | ✅ |
| tariffs_box | 83 | ✅ |
| tariffs_pallet | 91 | ✅ |
| tariffs_supply | 6705 | ✅ |
| campaigns | 1114 | ✅ |
| campaign_stats | 1392 | ✅ |
| feedbacks | 116498 | ✅ |
| questions | 5184 | ✅ |
| claims | 0 | ✅ (нет претензий) |
| analytics_stocks | 50 | ✅ |
| analytics_funnel | 1 | ✅ |
| financial_report | 1035554 | ✅ |
| seller_rating | 0 | ⏳ нет токена (403) |
| seller_subscriptions | 0 | ⏳ нет токена (403) |

**Ожидают токена с правами:**
- `seller_rating` — нужны права `Вопросы и отзывы` в API-токене
- `seller_subscriptions` — нужны права `Джем / Общие настройки` в API-токене

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

## Оставшиеся задачи (TODO)

### 🔴 Активные проблемы

| Эндпоинт | Проблема | Решение |
|----------|---------|---------|
| `/promotion/sync/stats/full` | TMO по HTTP (23 мин) | ✅ работает через Celery |
| `/finances/sync/full` | 502 OOM по HTTP | ✅ работает через Celery (task_id) |
| `/reports/sync/orders/full` | 404 | ✅ исправлено (route path `/` → `/full`) |
| `/reports/sync/sales/full` | 404 | ✅ исправлено (route path `/` → `/full`) |
| `/communications/sync/feedbacks/full` | 502 | расследовать |
| `seller_rating`, `seller_subscriptions` | 403 | создать токен с нужными правами |

### ✅ Исправлено (2026-04-05)

- Reports sync routes: `@post("/")` → `@post("/full")` для stocks/orders/sales
- Tariffs sync routes: `@post("/")` → `@post("/full")` для commissions/box/pallet/supply
- FBS supplies/passes: добавлены sync/db контроллеры, repositories, сервисы
- FBS supplies/passes: добавлены в Celery Beat (ежедневно 04:35/04:40)
- Broken imports: `WbTariffCommission` → `TariffCommission` и т.д. в repositories/tariffs
- Alembic: исправлена битая цепочка миграций (отсутствующая ревизия `f2a3b4c5d6e7`)
- `migrations/env.py`: убраны дублирующие импорты (достаточно `import src.models`)
- `celery_app.py`: исправлена синтаксическая ошибка (вложенный dict в beat_schedule)
- FBS supplies sync: параметр `next_cursor` → `offset` (совместимость с коллектором)

### 🟠 Технический долг

- **Excel-экспорт** — CLAUDE.md требует, но не реализован ни в одном DB-эндпоинте
- **`wb_sync_state`** — единственная таблица с `wb_` префиксом (переименовать → `sync_state`)
- **`campaign_stats.raw_data`** — использует `JSON` вместо `JSONB`
- **Reports таблицы** — `stocks`, `orders_report`, `sales_report` без префикса `reports_` (по CLAUDE.md нужен)
- **Unique constraints** — все таблицы проверены ✅

---

## Ограничения PostgreSQL (asyncpg)

1. **Максимум 32767 параметров** в одном INSERT → чанкинг: `chunk_size = 32767 // num_columns`
2. **Unique constraints обязательны** для `ON CONFLICT DO UPDATE`
3. **WB возвращает числа как строки** (`"0,07"`, `"46"`, `"-"`) — конвертация через `field_validator` в Pydantic-схеме, **НЕ** хелперы в репозитории

Пример чанкинга:
```python
CHUNK_SIZE = 32767 // 9  # = 3640 для таблицы с 9 колонками

for i in range(0, len(rows), CHUNK_SIZE):
    chunk = rows[i:i + CHUNK_SIZE]
    await session.execute(insert(Model).values(chunk).on_conflict_do_update(...))
```

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

## Как запускать

```powershell
# Полный запуск
docker compose up -d

# Проверить все sync-эндпоинты (PowerShell):
$token = (Select-String .env -Pattern "^WB_API_TOKEN=").Line.Split("=",2)[1]
$h = @{Authorization="Bearer $token"}
Invoke-WebRequest -Uri "http://localhost:8080/general/sync/seller/full" -Method POST -Headers $h -UseBasicParsing

# Проверка данных в БД:
docker exec wb_postgres psql -U wb_user -d wb_collector -c "SELECT count(*) FROM campaigns;"

# Логи app:
docker logs wb_app --tail 50

# Логи Celery:
docker logs wb_celery --tail 50
```

---

## ✅ Обязательная самопроверка после каждого изменения

**После ЛЮБОГО изменения кода — всегда выполнить все шаги ниже. Не пропускать.**

### Шаг 1: деплой и перезапуск

```powershell
# Скопировать все изменённые файлы
docker cp src\... wb_app:/app/src/...

# Перезапустить контейнеры
docker restart wb_app
Start-Sleep 5
# Если менялись tasks.py или celery_app.py — ещё:
docker restart wb_celery wb_celery_beat
Start-Sleep 3
```

### Шаг 2: проверить что app стартовал без ошибок

```powershell
docker logs wb_app --tail 20
# Должно быть: "Started server process" или "Application startup complete"
# Ошибки импорта / синтаксиса — красный флаг, фиксить сразу
```

### Шаг 3: HTTP-тест каждого изменённого эндпоинта

Для каждого нового или изменённого эндпоинта — явный `Invoke-WebRequest`:

```powershell
# GET эндпоинт:
$r = Invoke-WebRequest "http://localhost:8080/{path}" -UseBasicParsing
Write-Host "$($r.StatusCode) — $($r.Content | ConvertFrom-Json | ConvertTo-Json -Depth 1)"

# POST sync эндпоинт:
$r = Invoke-WebRequest "http://localhost:8080/{path}/sync/full" -Method POST -UseBasicParsing -TimeoutSec 30
$d = $r.Content | ConvertFrom-Json
Write-Host "$($r.StatusCode) synced=$($d.synced)"

# Ожидаемый результат: 200/201, synced > 0 (или 0 если данных нет — тоже ОК, без 5xx)
```

### Шаг 4: проверить данные в БД

```powershell
docker exec wb_postgres psql -U wb_user -d wb_collector -c "
SELECT '{table}' as t, count(*) FROM {table};"
# Ожидаемый результат: строки появились / обновились
# Если count=0 — проверить логи sync, возможно WB API вернул пустой список
```

### Шаг 5: проверить типы и поля (для новых схем)

```powershell
docker exec wb_postgres psql -U wb_user -d wb_collector -c "
SELECT * FROM {table} LIMIT 2;"
# Проверить: нет ли NULL там где не должно быть, нет ли кириллических вопросиков
```

### Шаг 6: Celery (если менялись задачи)

```powershell
docker logs wb_celery --tail 20
docker logs wb_celery_beat --tail 10
# Celery должен принять задачу без ошибок
# Beat должен показать расписание без warnings
```

### Шаг 7: отчёт

После проверки — **явно написать результат**:
```
✅ /fbw/sync/supplies/full → 201 synced=818
✅ /fbw/wb/supplies/38304393?isPreorderID=false → 200
✅ fbw_supplies: 818 строк
❌ /fbw/wb/supplies/{id}/package → 500 (починил: ...)
```

### Когда НЕ нужна полная проверка

- Изменение только документации / комментариев
- Изменение только `.md` / `.yaml` файлов
- `chore: remove debug scripts` коммит

### Автоматическая проверка через cron

Для долгих Celery задач — ставить отложенную проверку:
```python
cron.add(job={
    "schedule": {"kind": "at", "at": "<ISO время через N минут>"},
    "payload": {"kind": "agentTurn", "message": "Проверь Celery task <id>: статус, строк в БД, нет ли ошибок. Сообщи результат."},
    "sessionTarget": "isolated",
    "delivery": {"mode": "announce"}
})
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
