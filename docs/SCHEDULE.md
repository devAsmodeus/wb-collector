# Расписание Celery Beat

Часовой пояс: **Europe/Minsk (GMT+3)**

## Запуск

```bash
# Worker
docker compose exec celery_worker celery -A src.tasks.celery_app worker --loglevel=info

# Beat (планировщик)
docker compose exec celery_beat celery -A src.tasks.celery_app beat --loglevel=info
```

---

## Ночное окно (03:00 – 05:30) — тяжёлые задачи

| Время | Задача | Описание |
|-------|--------|----------|
| 03:00 | `sync.reports.stocks` | Остатки (отчёт) |
| 03:15 | `sync.reports.orders` | Заказы (отчёт) |
| 03:30 | `sync.reports.sales` | Продажи (отчёт) |
| 03:45 | `sync.finances.full` | Финансовый отчёт |
| 04:00 | `sync.tariffs.commissions` | Тарифы — комиссии |
| 04:00 | `sync.fbw.supplies_full` | Поставки FBW |
| 04:03 | `sync.tariffs.box` | Тарифы — короб |
| 04:06 | `sync.tariffs.pallet` | Тарифы — паллет |
| 04:09 | `sync.tariffs.supply` | Тарифы — поставка |
| 04:10 | `sync.fbw.supply_goods` | Товары поставок FBW |
| 04:20 | `sync.fbw.warehouses_full` | Склады FBW |
| 04:25 | `sync.fbw.transit_tariffs_full` | Тарифы транзита FBW |
| 04:30 | `sync.promotion.calendar_full` | Календарь акций |
| 04:35 | `sync.fbs.supplies_full` | Поставки FBS |
| 04:40 | `sync.fbs.passes_full` | Пропуска FBS |
| 05:00 | `sync.general.seller_full` | Данные продавца |
| 05:00 | `sync.analytics.funnel_full` | Воронка продаж |
| 05:05 | `sync.general.news_full` | Новости (Celery, пагинация) |
| 05:10 | `sync.general.news_incremental` | Инкрементальные новости |
| 05:10 | `sync.analytics.stocks_full` | Остатки по группам |
| 05:15 | `sync.general.users_full` | Пользователи |
| 05:20 | `sync.analytics.search_full` | Поисковые запросы |

---

## Еженедельные (воскресенье)

| Время | Задача | Описание |
|-------|--------|----------|
| 04:15 | `sync.products.directories_categories` | Категории |
| 04:17 | `sync.products.directories_subjects` | Предметы |
| 04:20 | `sync.products.tags_full` | Теги |

---

## Частые задачи

| Интервал | Задача | Описание |
|----------|--------|----------|
| каждые 5 мин (:05) | `sync.products.cards_incremental` | Новые карточки |
| каждые 15 мин | `sync.fbs.orders_full` | Заказы FBS |
| каждые 15 мин | `sync.dbw.orders_full` | Заказы DBW |
| каждые 15 мин | `sync.dbs.orders_full` | Заказы DBS |
| каждые 15 мин | `sync.pickup.orders_full` | Заказы самовывоза |
| каждые 30 мин | `sync.products.prices_incremental` | Цены |
| каждые 30 мин | `sync.fbw.supplies_incremental` | Новые поставки FBW |
| каждые 30 мин | `sync.analytics.funnel_incremental` | Воронка (инкрементальная) |
| каждые 30 мин | `sync.analytics.stocks_incremental` | Остатки (инкрементальные) |
| каждые 30 мин | `sync.analytics.search_incremental` | Поиск (инкрементальный) |
| :07 и :37 | `sync.communications.feedbacks_full` | Отзывы |
| :12 и :42 | `sync.communications.questions_full` | Вопросы |
| :17 и :47 | `sync.communications.claims_full` | Претензии |
| :20 каждые 3 ч | `sync.promotion.campaigns_full` | Кампании |
| :25 каждые 3 ч | `sync.promotion.stats_full` | Статистика кампаний |

---

## Системные

| Время | Задача | Описание |
|-------|--------|----------|
| 08:00 | `sync.docs.wb_api` | Обновление YAML-документации WB API |

---

## Примечания

- **Тяжёлые задачи** (`reports`, `finances`, `news full`) возвращают `task_id` — выполняются асинхронно
- **Rate limit WB**: при 429 worker автоматически ждёт 60 секунд и повторяет
- **Retry**: 3 попытки с интервалом 60 секунд для каждой задачи
- **DBW/DBS/Pickup**: задачи запускаются, но WB возвращает 400 (схемы доставки не подключены к аккаунту) — это ожидаемо
