# WB Collector

Сервис сбора и хранения данных из API Wildberries для аналитики DiRetail.

---

## Документация

- [README.md](README.md) — этот файл: архитектура, модули, установка
- [docs/MONITORING.md](docs/MONITORING.md) — мониторинг: Grafana, Loki, Prometheus, Promtail

---

## Содержание

1. [Что делает проект](#что-делает-проект)
2. [Архитектура](#архитектура)
3. [Структура проекта](#структура-проекта)
4. [Как устроены слои](#как-устроены-слои)
5. [Модули (главы API)](#модули-главы-api)
6. [Установка и запуск](#установка-и-запуск)
7. [Переменные окружения](#переменные-окружения)
8. [WB API: важные особенности](#wb-api-важные-особенности)
9. [Скрипты](#скрипты)
10. [FAQ](#faq)

---

## Что делает проект

WB Collector решает три задачи:

1. **Отслеживает изменения документации WB API** — каждый день в 08:00 сравнивает 13 YAML-файлов документации с предыдущей версией и отправляет уведомление в Telegram если что-то изменилось.

2. **Собирает данные из WB API** — опрашивает эндпоинты Wildberries (цены, остатки, аналитику, финансы и т.д.) и сохраняет в PostgreSQL.

3. **Предоставляет REST API** — FastAPI-сервер с документацией Swagger, через который можно получить собранные данные.

---

## Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI (REST API)                    │
│              /general  /products  /...                   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                      Services                            │
│   Бизнес-логика: что сохранять, как обрабатывать        │
└────────────────────────┬────────────────────────────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
┌──────────▼───────────┐  ┌────────────▼────────────────┐
│     Collectors        │  │       Repositories           │
│  HTTP-клиенты WB API  │  │  Работа с PostgreSQL         │
└──────────┬───────────┘  └────────────┬────────────────┘
           │                           │
┌──────────▼───────────┐  ┌────────────▼────────────────┐
│    WB API серверы     │  │       PostgreSQL             │
│ (13 разных хостов)    │  │       + Redis cache          │
└──────────────────────┘  └─────────────────────────────┘
```

### Принцип работы

1. **Запрос приходит** в FastAPI-роутер (`src/api/...`)
2. Роутер вызывает **сервис** (`src/services/...`)
3. Сервис использует **коллектор** для получения данных из WB API (`src/collectors/...`)
4. Сервис использует **репозиторий** для сохранения в БД (`src/repositories/...`)
5. Данные валидируются через **Pydantic-схемы** (`src/schemas/...`)
6. Ответ возвращается клиенту

---

## Структура проекта

```
wb-collector/
│
├── docs/
│   └── api/                        # YAML-документация WB API (13 файлов)
│       ├── manifest.json           # SHA256-хеши для отслеживания изменений
│       ├── 01-general.yaml
│       ├── 02-products.yaml
│       └── ...
│
├── scripts/
│   ├── sync_docs.py                # Трекер изменений документации (cron)
│   ├── test_collector.py           # Тест 01-general
│   ├── test_products.py            # Тест 02-products
│   ├── decode_token.py             # Декодирование JWT-токена WB
│   ├── check_servers.py            # Проверка доступности хостов WB
│   └── inspect_yaml2.py            # Анализ YAML-файлов документации
│
├── src/
│   ├── config.py                   # Настройки (токены, хосты, БД)
│   ├── database.py                 # SQLAlchemy engine + сессия
│   ├── exceptions.py               # Исключения WB API
│   ├── main.py                     # FastAPI приложение
│   ├── init.py                     # Redis-менеджер
│   │
│   ├── collectors/                 # HTTP-клиенты WB API
│   │   ├── base.py                 # Базовый клиент (ретраи, 429, таймаут)
│   │   ├── general/                # 01 — Общее
│   │   │   ├── seller.py           # Информация о продавце
│   │   │   ├── news.py             # АПИ новостей
│   │   │   └── users.py            # Управление пользователями
│   │   └── products/               # 02 — Работа с товарами
│   │       ├── directories.py      # Категории, предметы, характеристики
│   │       ├── tags.py             # Ярлыки
│   │       ├── cards.py            # Карточки товаров
│   │       ├── media.py            # Медиафайлы
│   │       ├── prices.py           # Цены и скидки
│   │       └── warehouses.py       # Остатки и склады
│   │
│   ├── schemas/                    # Pydantic-модели (валидация данных)
│   │   ├── general/
│   │   │   ├── seller.py
│   │   │   ├── news.py
│   │   │   └── users.py
│   │   └── products/
│   │       ├── directories.py
│   │       ├── tags.py
│   │       ├── cards.py
│   │       ├── media.py
│   │       ├── prices.py
│   │       └── warehouses.py
│   │
│   ├── services/                   # Бизнес-логика
│   │   ├── base.py                 # BaseService
│   │   ├── general/
│   │   │   ├── seller.py
│   │   │   ├── news.py
│   │   │   └── users.py
│   │   └── products/
│   │       ├── directories.py
│   │       ├── tags.py
│   │       ├── cards.py
│   │       ├── prices.py
│   │       └── warehouses.py
│   │
│   ├── api/                        # FastAPI роутеры
│   │   ├── general/
│   │   │   ├── __init__.py         # Агрегирует sub-роутеры → /general
│   │   │   ├── seller.py           # GET /general/ping, /general/seller-info
│   │   │   ├── news.py             # GET /general/news
│   │   │   └── users.py            # /general/users
│   │   └── products/
│   │       ├── __init__.py         # → /products
│   │       ├── directories.py      # GET /products/directories/...
│   │       ├── tags.py             # /products/tags
│   │       ├── cards.py            # /products/cards
│   │       ├── prices.py           # GET /products/prices/...
│   │       └── warehouses.py       # GET /products/warehouses/...
│   │
│   ├── models/                     # SQLAlchemy ORM-модели
│   │   └── seller.py               # SellerOrm → таблица sellers
│   │
│   ├── repositories/               # CRUD-операции с БД
│   │   ├── base.py                 # BaseRepository
│   │   ├── seller.py               # SellerRepository
│   │   └── mappers/
│   │       ├── base.py             # DataMapper (ORM ↔ Pydantic)
│   │       └── mappers.py          # SellerMapper
│   │
│   ├── utils/
│   │   └── db_manager.py           # DBManager — контекстный менеджер БД
│   │
│   ├── tasks/
│   │   ├── celery_app.py           # Celery приложение
│   │   └── tasks.py                # Периодические задачи
│   │
│   └── migrations/                 # Alembic миграции
│       ├── env.py
│       └── versions/
│
├── .env                            # Секреты (в git не попадает!)
├── .env.example                    # Шаблон .env
├── docker-compose.yml              # PostgreSQL + Redis + сервис
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

---

## Как устроены слои

### 1. Collectors — HTTP-клиенты WB API

Коллектор — это класс, который умеет делать запросы к WB API. Каждый коллектор отвечает за свою группу эндпоинтов.

**Базовый клиент (`src/collectors/base.py`):**

```python
class WBApiClient:
    """Один экземпляр = один httpx.AsyncClient к одному хосту WB."""

    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url      # например https://discounts-prices-api.wildberries.ru
        self.token = token or settings.WB_API_TOKEN

    async def get(self, path, params=None) -> dict: ...
    async def post(self, path, json=None) -> dict: ...
    async def put(self, path, json=None) -> dict: ...
    async def patch(self, path, json=None) -> dict: ...
    async def delete(self, path, json=None) -> dict: ...
```

**Встроенная защита от ошибок:**
- `3 retry` при сетевых ошибках (таймаут, обрыв соединения)
- При `429 Too Many Requests` — автоматически ждёт 60 секунд и повторяет
- При `401 Unauthorized` — сразу бросает исключение (ретраить бессмысленно)

**Почему async?** WB API может отвечать медленно. Async позволяет делать много запросов параллельно, не блокируя сервер.

**Пример использования:**

```python
# Коллектор для цен
async with ProductsCollector() as c:
    goods = await c.prices.get_goods_list(limit=100)
    for item in goods.data.listGoods:
        print(f"{item.nmID}: цена {item.sizes[0].price / 100} руб")
```

---

### 2. Schemas — Валидация данных (Pydantic)

Схемы — это Python-классы, которые описывают структуру данных. Они решают две задачи:

1. **Валидируют ответ WB API** — если WB вернул что-то неожиданное, Pydantic поймает ошибку
2. **Документируют структуру** — сразу видно какие поля есть и какого они типа

```python
# src/schemas/products/prices.py
class GoodsItem(BaseModel):
    nmID: int            # артикул WB
    vendorCode: str      # ваш артикул
    discount: int        # скидка в %
    sizes: list[GoodsSize]

class GoodsSize(BaseModel):
    sizeID: int | None   # ID размера
    price: int | None    # цена в копейках (!)
    discountedPrice: int | None
```

> **Важно:** WB хранит цены в **копейках** × 100. Цена 3000 руб = `300000` в API.

---

### 3. Services — Бизнес-логика

Сервис координирует работу коллекторов и репозиториев. Именно здесь решается "что сделать с данными".

```python
class SellerService(BaseService):

    async def sync_seller_info(self) -> SellerInfo:
        # 1. Получить из WB API
        async with SellerCollector() as c:
            seller = await c.get_seller_info()

        # 2. Сохранить в БД
        async with self.db as db:
            result = await db.seller.upsert(seller)
            await db.commit()

        return result
```

**BaseService** принимает `DBManager` — если передан, сервис умеет работать с БД. Если нет — только запросы к API.

---

### 4. Repositories — Работа с базой данных

Репозиторий — тонкий слой над SQLAlchemy. Умеет: `get_filtered`, `get_one`, `add`, `edit`, `delete`.

```python
class SellerRepository(BaseRepository):
    model = SellerOrm

    async def upsert(self, seller: SellerInfo) -> SellerInfo:
        """Создать или обновить по sid (уникальный ID продавца WB)."""
        ...
```

---

### 5. API — FastAPI роутеры

Роутер принимает HTTP-запрос, вызывает сервис, возвращает ответ.

```python
@router.get("/prices/goods", response_model=GoodsListResponse)
async def get_goods(limit: int = Query(100), offset: int = Query(0)):
    return await PricesService().get_goods(limit=limit, offset=offset)
```

**Агрегация роутеров** — каждый модуль собирает sub-роутеры в `__init__.py`:

```python
# src/api/products/__init__.py
router = APIRouter(prefix="/products", tags=["02 — Products"])
router.include_router(prices_router)     # /products/prices/...
router.include_router(cards_router)      # /products/cards/...
router.include_router(warehouses_router) # /products/warehouses/...
```

---

## Модули (главы API)

### ✅ 01 — Общее (`/general`)

**Хост:** `common-api.wildberries.ru`, `user-management-api.wildberries.ru`

| Эндпоинт | Метод | Описание |
|---|---|---|
| `/general/ping` | GET | Проверить подключение к WB API |
| `/general/seller-info/sync` | POST | Получить инфо о продавце из WB и сохранить в БД |
| `/general/seller-info` | GET | Получить сохранённое инфо о продавце из БД |
| `/general/news` | GET | Новости портала продавцов |
| `/general/users` | GET | Список пользователей аккаунта ⚠️ |
| `/general/users/invite` | POST | Создать приглашение ⚠️ |
| `/general/users/access` | PUT | Изменить права доступа ⚠️ |
| `/general/users/{id}` | DELETE | Удалить пользователя ⚠️ |

⚠️ — требует `WB_PERSONAL_TOKEN` с правом "Управление пользователями"

---

### ✅ 02 — Работа с товарами (`/products`)

**Хосты:**
- `content-api.wildberries.ru` — справочники, ярлыки, карточки, медиа
- `discounts-prices-api.wildberries.ru` — цены и скидки
- `marketplace-api.wildberries.ru` — остатки и склады

#### Категории, предметы, характеристики (10 методов)

| Эндпоинт | Описание |
|---|---|
| GET `/products/directories/categories` | Все родительские категории (Одежда, Обувь...) |
| GET `/products/directories/subjects` | Предметы внутри категорий (Футболка, Платье...) |
| GET `/products/directories/subjects/{id}/charcs` | Характеристики предмета (размер, цвет, состав...) |
| GET `/products/directories/subjects/{id}/brands` | Бренды предмета |
| GET `/products/directories/colors` | Справочник цветов |
| GET `/products/directories/kinds` | Справочник полов |
| GET `/products/directories/countries` | Страны производства |
| GET `/products/directories/seasons` | Сезоны |
| GET `/products/directories/vat` | Ставки НДС |
| GET `/products/directories/tnved` | ТНВЭД-коды |

> **Примечание:** эти эндпоинты могут возвращать 401 — для работы с контентом нужен токен с правом "Контент" (бит 1), которого нет в текущем токене.

#### Ярлыки (5 методов)

Ярлыки — пользовательские метки для карточек товаров.

| Эндпоинт | Описание |
|---|---|
| GET `/products/tags` | Список всех ярлыков |
| POST `/products/tags` | Создать ярлык |
| PATCH `/products/tags/{id}` | Изменить ярлык |
| DELETE `/products/tags/{id}` | Удалить ярлык |
| POST `/products/tags/link` | Привязать ярлыки к карточке |

#### Карточки товаров (11 методов)

| Эндпоинт | Описание |
|---|---|
| POST `/products/cards` | Список карточек (с фильтрами и пагинацией) |
| GET `/products/cards/limits` | Лимиты создания карточек |
| GET `/products/cards/errors` | Карточки с ошибками создания |
| POST `/products/cards/trash` | Карточки в корзине |
| POST `/products/barcodes` | Генерация баркодов |

#### Цены и скидки (11 методов) ✅ Работает с текущим токеном

| Эндпоинт | Описание |
|---|---|
| GET `/products/prices/goods` | Все товары с ценами и скидками |
| GET `/products/prices/goods/sizes` | Цены по размерам конкретного артикула |
| GET `/products/prices/goods/quarantine` | Товары на карантине (заблокированные цены) |
| GET `/products/prices/history` | История загрузок цен |
| GET `/products/prices/history/goods` | Товары конкретной загрузки |
| GET `/products/prices/buffer` | Задачи в очереди на обработку |
| GET `/products/prices/buffer/goods` | Товары задачи в очереди |

#### Остатки и склады (10 методов) ✅ Работает с текущим токеном

| Эндпоинт | Описание |
|---|---|
| GET `/products/warehouses` | Склады продавца |
| GET `/products/warehouses/wb` | Офисы WB (223 точки по России) |
| POST `/products/warehouses/{id}/stocks` | Остатки на конкретном складе |

---

## Установка и запуск

### Требования

- Python 3.12+
- PostgreSQL 16 (или Docker)
- Redis 7 (или Docker)

### Шаг 1: Клонировать и установить зависимости

```bash
git clone https://github.com/devAsmodeus/wb-collector.git
cd wb-collector
pip install -r requirements.txt
```

### Шаг 2: Создать .env файл

```bash
cp .env.example .env
```

Отредактировать `.env`:

```dotenv
WB_API_TOKEN=eyJhbGci...  # Ваш токен WB API
WB_PERSONAL_TOKEN=        # Опционально: токен с правом управления пользователями

DB_HOST=localhost
DB_PORT=5432
DB_USER=wb_user
DB_PASS=wb_pass
DB_NAME=wb_collector

REDIS_HOST=localhost
REDIS_PORT=6379
```

### Шаг 3: Запустить PostgreSQL и Redis через Docker

```bash
docker-compose up -d postgres redis
```

Или если Docker не установлен — запустить вручную локально.

### Шаг 4: Применить миграции

```bash
alembic upgrade head
```

### Шаг 5: Запустить сервер

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Шаг 6: Открыть документацию API

Перейти на http://localhost:8000/docs

---

## Переменные окружения

| Переменная | Обязательно | Описание |
|---|---|---|
| `WB_API_TOKEN` | ✅ | Основной токен WB API (JWT) |
| `WB_PERSONAL_TOKEN` | ❌ | Персональный токен для управления пользователями |
| `DB_HOST` | ✅ | Хост PostgreSQL |
| `DB_PORT` | ✅ | Порт PostgreSQL (по умолчанию 5432) |
| `DB_USER` | ✅ | Пользователь БД |
| `DB_PASS` | ✅ | Пароль БД |
| `DB_NAME` | ✅ | Имя базы данных |
| `REDIS_HOST` | ✅ | Хост Redis |
| `REDIS_PORT` | ✅ | Порт Redis (по умолчанию 6379) |
| `MODE` | ❌ | Режим: LOCAL / DEV / PROD (по умолчанию LOCAL) |

### Как получить токен WB API

1. Войти на [seller.wildberries.ru](https://seller.wildberries.ru)
2. Настройки → Доступ к API → Создать новый токен
3. Выбрать нужные права (минимум: Цены и скидки, Статистика, Аналитика, Финансы)
4. Скопировать токен в `.env`

> **Токен действует 180 дней.** После истечения — создать новый и обновить `.env`.

---

## WB API: важные особенности

### Разные хосты для разных разделов

У WB нет единого API-сервера. Каждый раздел — отдельный поддомен:

| Раздел | Хост |
|---|---|
| Общее, продавец | `common-api.wildberries.ru` |
| Контент (карточки) | `content-api.wildberries.ru` |
| Цены и скидки | `discounts-prices-api.wildberries.ru` |
| Статистика | `statistics-api.wildberries.ru` |
| Аналитика | `seller-analytics-api.wildberries.ru` |
| Финансы | `finance-api.wildberries.ru` |
| Маркетплейс (FBW) | `marketplace-api.wildberries.ru` |
| Реклама | `advert-api.wildberries.ru` |
| Управление пользователями | `user-management-api.wildberries.ru` |

### Права доступа токена (scopes)

Токен WB содержит поле `s` — битовая маска прав. Текущий токен (`s=7934`):

| Бит | Право | Статус |
|---|---|---|
| 1 | Контент (карточки) | ❌ нет |
| 2 | Цены и скидки | ✅ есть |
| 4 | Статистика | ✅ есть |
| 8 | Маркетплейс FBS | ✅ есть |
| 16 | Продвижение | ✅ есть |
| 32 | Вопросы и отзывы | ✅ есть |
| 64 | Чат | ✅ есть |
| 128 | Финансы | ✅ есть |
| 256 | Поставки | ❌ нет |
| 512 | Расширенная аналитика | ✅ есть |
| 1024 | Тарифы | ✅ есть |
| 4096 | Управление пользователями | ✅ есть |

### Цены хранятся в копейках × 100

```python
# WB API возвращает: price = 300000
# Реальная цена: 300000 / 100 = 3000 руб
real_price = api_price / 100
```

### Rate Limits

WB API имеет ограничения на количество запросов. Базовый клиент автоматически:
- Ждёт 60 секунд при получении `429 Too Many Requests`
- Повторяет запрос до 3 раз при сетевых ошибках

---

## Скрипты

### `scripts/sync_docs.py` — Трекер документации

Запускается автоматически каждый день в 08:00 (Europe/Minsk). Алгоритм:
1. Скачивает все 13 YAML-файлов документации с `dev.wildberries.ru`
2. Считает SHA256-хеш каждого файла
3. Сравнивает с `docs/api/manifest.json`
4. Если что-то изменилось — делает семантический diff (какие эндпоинты добавились/удалились)
5. Отправляет уведомление в Telegram с описанием изменений
6. Делает `git commit` с обновлёнными файлами

```bash
# Запустить вручную (проверка прямо сейчас)
python scripts/sync_docs.py
```

### `scripts/test_products.py` — Тест API цен и складов

```bash
python scripts/test_products.py
```

Выводит:
- Первые 5 товаров с ценами и скидками
- Список складов продавца
- Количество офисов WB по России

### `scripts/decode_token.py` — Декодирование токена

Показывает содержимое JWT-токена (права, срок действия, ID продавца).

```bash
python scripts/decode_token.py
# Или передать токен явно:
python scripts/decode_token.py eyJhbGci...
```

### `scripts/check_servers.py` — Проверка доступности

Проверяет, отвечают ли все хосты WB API (`ping` к каждому).

```bash
python scripts/check_servers.py
```

---

## FAQ

**Q: Почему эндпоинты `/content/*` возвращают 401?**

A: Для работы с карточками товаров нужен токен с правом "Контент" (бит 1). В текущем токене этого права нет. Создайте новый токен с галочкой "Контент" на [seller.wildberries.ru](https://seller.wildberries.ru).

---

**Q: Как добавить новый модуль (например 07-FBW)?**

A: Следовать паттерну:
1. `src/schemas/fbw/` — создать схемы из YAML-документации
2. `src/collectors/fbw/` — реализовать HTTP-запросы
3. `src/services/fbw/` — бизнес-логика
4. `src/api/fbw/` — роутер
5. Подключить роутер в `src/main.py`

---

**Q: Почему не работает `alembic upgrade head`?**

A: PostgreSQL должен быть запущен. Проверьте:
```bash
docker-compose up -d postgres
# или проверьте что PostgreSQL запущен локально
```

---

**Q: Где смотреть логи?**

A: Сервер пишет логи в консоль. При запуске через `uvicorn --reload` все запросы и ошибки видны в терминале. В продакшене настройте `LOG_LEVEL` в конфиге.

---

**Q: Как часто WB обновляет данные в API?**

A: Зависит от раздела:
- Цены и остатки — в реальном времени
- Статистика заказов — задержка 1-4 часа
- Финансовые отчёты — задержка до 1 дня
- Аналитика — задержка 1-2 часа

---

**Q: Что такое `WB_PERSONAL_TOKEN`?**

A: WB различает два типа токенов:
- **Базовый токен** (`t: false` в JWT) — создаётся через "Доступ к API", работает для большинства задач
- **Персональный токен** (`t: true`) — создаётся через "Мои токены", нужен для управления пользователями аккаунта

Если `WB_PERSONAL_TOKEN` не задан, система автоматически использует `WB_API_TOKEN`.

---

## Разработка

### Добавление нового модуля

```
Глава в YAML → Схемы → Коллектор → Сервис → Роутер → main.py
```

### Запуск с hot-reload

```bash
uvicorn src.main:app --reload
```

### Создание миграции

```bash
# После изменения моделей в src/models/
alembic revision --autogenerate -m "add products table"
alembic upgrade head
```

### Линтер

```bash
ruff check src/
```
