# Мониторинг WB Collector

Продакшен-стек: **Grafana + Loki + Prometheus + Promtail**

---

## Содержание

1. [Общая схема](#общая-схема)
2. [Компоненты](#компоненты)
3. [Как работает сбор логов](#как-работает-сбор-логов)
4. [Как работает сбор метрик](#как-работает-сбор-метрик)
5. [Запуск](#запуск)
6. [Grafana: дашборды](#grafana-дашборды)
7. [Метрики приложения](#метрики-приложения)
8. [Добавление своих метрик](#добавление-своих-метрик)
9. [Алерты](#алерты)

---

## Общая схема

```
┌─────────────────────────────────────────────────────────────────┐
│  wb-collector (FastAPI)                                         │
│                                                                 │
│  • Каждое событие → logger.info("...")                          │
│  • Каждый запрос к WB API → счётчики и гистограммы             │
│  • Эндпоинт /metrics отдаёт все метрики в формате Prometheus    │
└────────────┬────────────────────────┬───────────────────────────┘
             │ stdout (JSON)          │ HTTP GET /metrics
             ↓                        ↓
┌────────────────────┐   ┌────────────────────────────────────────┐
│  Docker Engine     │   │  Prometheus                            │
│                    │   │                                        │
│  Пишет stdout      │   │  Каждые 15 сек опрашивает /metrics     │
│  контейнера в      │   │  Хранит метрики 30 дней                │
│  свой json-log     │   │  Порт: 9090                            │
└────────┬───────────┘   └──────────────────┬─────────────────────┘
         │                                  │
         ↓                                  │
┌────────────────────┐                      │
│  Promtail          │                      │
│                    │                      │
│  Читает логи через │                      │
│  Docker socket     │                      │
│  Парсит JSON       │                      │
│  Добавляет лейблы  │                      │
└────────┬───────────┘                      │
         │ push                             │
         ↓                                  │
┌────────────────────┐                      │
│  Loki              │                      │
│                    │                      │
│  Хранилище логов   │                      │
│  Хранит 30 дней    │                      │
│  Порт: 3100        │                      │
└────────┬───────────┘                      │
         │                                  │
         └──────────────┬───────────────────┘
                        ↓
         ┌──────────────────────────────────┐
         │  Grafana                         │
         │                                  │
         │  Дашборд 1: Метрики (Prometheus) │
         │  Дашборд 2: Логи (Loki)          │
         │  Порт: 3000                      │
         └──────────────────────────────────┘
```

---

## Компоненты

### Prometheus
**Что делает:** Собирает числовые метрики — счётчики, гистограммы, gauges.

**Принцип:** Pull-модель. Prometheus сам приходит к приложению каждые 15 секунд и спрашивает: "Какие у тебя метрики?" Приложение отвечает через эндпоинт `/metrics`.

**Что хранит:**
- Сколько HTTP-запросов пришло на каждый эндпоинт
- Время ответа (p50, p95, p99)
- Сколько раз WB API вернул 429/401/500
- Сколько товаров собрано по каждому модулю

**Порт:** `9090` → http://localhost:9090

---

### Loki
**Что делает:** Хранит текстовые логи. Аналог Elasticsearch, но намного легче.

**Принцип:** Push-модель. Logи не хранятся в файлах — Promtail читает их из Docker и отправляет в Loki.

**Ключевая особенность:** Loki **не индексирует** содержимое логов (в отличие от Elasticsearch). Он индексирует только **лейблы** (container, level, service). Это делает его быстрым и дешёвым по памяти. Поиск по тексту работает через grep по сжатым чанкам.

**Порт:** `3100`

---

### Promtail
**Что делает:** Агент сбора логов. Читает логи контейнеров и отправляет в Loki.

**Как читает Docker-логи:** Подключается к `/var/run/docker.sock` (Docker socket). Получает список всех контейнеров с лейблом `com.docker.compose.project=wb-collector`, подписывается на их stdout/stderr.

**Что делает с каждой строкой лога:**
1. Получает строку из Docker: `{"timestamp":"2026-03-16T15:00:00","level":"INFO","message":"Собрано 100 товаров","logger":"src.collectors.products.prices"}`
2. Парсит JSON — извлекает поля `level`, `logger`, `message`, `timestamp`
3. Добавляет лейблы: `container=wb_app`, `service=app`, `level=INFO`
4. Отправляет в Loki

---

### Grafana
**Что делает:** Визуализация. Один интерфейс для логов и метрик.

**Datasources (источники данных):**
- `Prometheus` — для метрик (графики, счётчики, гистограммы)
- `Loki` — для логов (live-лента, поиск, фильтрация)

**Автоматическая настройка:** При первом запуске Grafana автоматически подключает оба источника данных и загружает готовый дашборд (через `provisioning`).

**Порт:** `3000` → http://localhost:3000  
**Логин:** `admin` / `admin` (настраивается в `.env`)

---

## Как работает сбор логов

### 1. Приложение логирует в JSON

`src/logging_config.py` настраивает Python-логирование так, чтобы каждая строка была валидным JSON:

```python
# Обычный вызов в коде
logger.info("Собрано товаров", extra={"module": "prices", "count": 100})

# Что реально пишется в stdout:
{
  "timestamp": "2026-03-16T15:00:00",
  "level": "INFO",
  "logger": "src.collectors.products.prices",
  "message": "Собрано товаров",
  "module": "prices",
  "count": 100
}
```

Почему JSON? Потому что Promtail умеет его парсить и превращать поля в лейблы. Это позволяет в Grafana делать запросы вида:
```
{service="app", level="ERROR"}
```
Вместо того чтобы grep'ать по тексту.

### 2. Docker сохраняет stdout

Docker Engine автоматически перехватывает всё что пишет контейнер в stdout и сохраняет в:
```
/var/lib/docker/containers/<container_id>/<container_id>-json.log
```

### 3. Promtail читает через socket

Promtail монтирует Docker socket (`/var/run/docker.sock`) и получает события о новых строках логов от всех контейнеров проекта.

### 4. Loki хранит, Grafana показывает

Логи в Grafana можно смотреть через **Explore** или на дашборде в панели "Логи (ERROR / WARNING)".

**Запрос в Loki (LogQL):**
```logql
# Все логи приложения
{service="app"}

# Только ошибки
{service="app", level="ERROR"}

# Ошибки модуля prices
{service="app", level="ERROR"} |= "prices"

# Поиск по тексту
{service="app"} |= "rate_limit"
```

---

## Как работает сбор метрик

### 1. /metrics эндпоинт

При запуске FastAPI автоматически регистрирует эндпоинт `/metrics`. Когда Prometheus его опрашивает, получает что-то вроде:

```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{handler="/products/prices/goods",method="GET",status_code="200"} 42

# HELP wb_api_requests_total Всего запросов к WB API
# TYPE wb_api_requests_total counter
wb_api_requests_total{host="discounts-prices-api.wildberries.ru",method="GET",status="200"} 15

# HELP wb_api_response_seconds Время ответа WB API
# TYPE wb_api_response_seconds histogram
wb_api_response_seconds_bucket{host="discounts-prices-api.wildberries.ru",endpoint="/api/v2/list/goods/filter",le="0.25"} 10
wb_api_response_seconds_bucket{...le="0.5"} 14
```

### 2. Кастомные метрики в коллекторах

В `src/metrics.py` определены метрики. В `src/collectors/base.py` они заполняются автоматически при каждом HTTP-запросе к WB API:

```python
# Это происходит в base.py автоматически при каждом запросе:
WB_API_REQUESTS.labels(host="discounts-prices-api.wildberries.ru", method="GET", status="200").inc()
WB_API_RESPONSE_TIME.labels(host="...", endpoint="/api/v2/list/goods/filter").observe(0.3)
```

### 3. Запросы в Prometheus (PromQL)

```promql
# RPS на /metrics (запросов в секунду за последнюю минуту)
rate(http_requests_total{job="wb-collector"}[1m])

# 95-й перцентиль времени ответа WB API
histogram_quantile(0.95, rate(wb_api_response_seconds_bucket[5m]))

# Количество 429 за последний час
sum(increase(wb_rate_limit_hits_total[1h]))

# Успешность сбора данных (в %)
rate(wb_collection_runs_total{status="success"}[5m])
/ rate(wb_collection_runs_total[5m]) * 100
```

---

## Запуск

```bash
# Запустить всё (приложение + БД + мониторинг)
docker-compose up -d

# Только мониторинг (если приложение запущено отдельно)
docker-compose up -d prometheus loki promtail grafana
```

**Адреса после запуска:**

| Сервис | URL | Логин |
|---|---|---|
| WB Collector API | http://localhost:8000/docs | — |
| Grafana | http://localhost:3000 | admin / admin |
| Prometheus | http://localhost:9090 | — |
| Loki | http://localhost:3100 | — |

---

## Grafana: дашборды

Дашборд **WB Collector** загружается автоматически при первом запуске.

### Панели дашборда

| Панель | Тип | Что показывает |
|---|---|---|
| HTTP Запросы к API (rps) | Graph | Нагрузка на наш API по методам и эндпоинтам |
| Время ответа API (p95) | Graph | 95-й перцентиль времени ответа |
| WB API — Запросы по хосту | Graph | Сколько запросов к каждому хосту WB |
| WB API — Время ответа (p95) | Graph | Насколько быстро отвечает каждый хост WB |
| Rate Limit Hits (429) | Stat | Счётчик с цветовой индикацией (зелёный/красный) |
| Ошибки WB API | Stat | Общее кол-во ошибок за час |
| Сбор данных — запуски | Graph | Успешные и неуспешные запуски коллекторов |
| Собрано записей | Bar gauge | Сколько записей собрано за 24ч по модулям |
| Логи (ERROR/WARNING) | Logs | Live-лента логов с фильтрацией |

---

## Метрики приложения

Все метрики определены в `src/metrics.py`:

### WB API метрики

| Метрика | Тип | Лейблы | Описание |
|---|---|---|---|
| `wb_api_requests_total` | Counter | host, method, status | Всего запросов к WB API |
| `wb_api_errors_total` | Counter | host, error_type | Ошибки по типу (rate_limit, unauthorized, timeout, server_error) |
| `wb_api_response_seconds` | Histogram | host, endpoint | Время ответа WB API |
| `wb_rate_limit_hits_total` | Counter | host | Кол-во 429 ответов |

### Метрики коллектора

| Метрика | Тип | Лейблы | Описание |
|---|---|---|---|
| `wb_collection_runs_total` | Counter | module, status | Запуски коллекторов (success/error) |
| `wb_collection_items_total` | Counter | module | Собрано записей |
| `wb_collection_duration_seconds` | Histogram | module | Время работы коллектора |
| `wb_last_collection_timestamp` | Gauge | module | Unix timestamp последнего успешного сбора |

### HTTP метрики (автоматические)

Генерируются `prometheus-fastapi-instrumentator`:

| Метрика | Описание |
|---|---|
| `http_requests_total` | Кол-во запросов по handler/method/status |
| `http_request_duration_seconds` | Время ответа (гистограмма) |
| `http_requests_inprogress` | Запросы в обработке прямо сейчас |

---

## Добавление своих метрик

```python
# 1. Объявить метрику в src/metrics.py
MY_METRIC = Counter("wb_my_metric_total", "Описание", labelnames=["label1"])

# 2. Использовать в коллекторе или сервисе
from src.metrics import MY_METRIC, record_collection
import time

async def collect_prices():
    start = time.monotonic()
    items = await prices_collector.get_goods_list()
    duration = time.monotonic() - start

    # Зафиксировать результат одной строкой
    record_collection(module="prices", items_count=len(items), duration_seconds=duration)
```

---

## Алерты

Grafana умеет отправлять алерты в Telegram когда что-то идёт не так.

**Настройка алертов в Grafana:**

1. Открыть Grafana → Alerting → Contact Points
2. Добавить Telegram: указать Bot Token и Chat ID
3. Создать правило на панели "Rate Limit Hits":
   - Условие: `sum(increase(wb_rate_limit_hits_total[5m])) > 5`
   - Действие: отправить в Telegram

**Рекомендуемые алерты:**

| Алерт | Условие | Серьёзность |
|---|---|---|
| Много 429 от WB | rate_limit_hits > 5 за 5 мин | Warning |
| Ошибки авторизации | unauthorized ошибок > 0 | Critical |
| Коллектор упал | collection success rate < 50% | Critical |
| WB API медленный | p95 response > 10 сек | Warning |
| Нет сбора данных | last_collection > 2 часов назад | Warning |
