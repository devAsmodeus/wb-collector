# Расписание Celery-задач

Все задачи запускаются через Celery Beat. Таймзона: `Europe/Minsk`.

## Запуск

```bash
# Worker (обработчик задач)
celery -A src.tasks.celery_app worker --loglevel=info --concurrency=4

# Beat (планировщик)
celery -A src.tasks.celery_app beat --loglevel=info
```

## Сводка расписания

### Каждые 15 минут — заказы
| Задача | Cron | Описание |
|--------|------|----------|
| sync.fbs.orders_full | */15 * * * * | Заказы FBS |
| sync.dbw.orders_full | */15 * * * * | Заказы DBW |
| sync.dbs.orders_full | */15 * * * * | Заказы DBS |
| sync.pickup.orders_full | */15 * * * * | Заказы Самовывоз |

### Каждые 30 минут — коммуникации
| Задача | Cron | Описание |
|--------|------|----------|
| sync.communications.feedbacks_full | 7,37 * * * * | Отзывы |
| sync.communications.questions_full | 12,42 * * * * | Вопросы |
| sync.communications.claims_full | 17,47 * * * * | Жалобы |

### Каждый час — товары
| Задача | Cron | Описание |
|--------|------|----------|
| sync.products.cards_full | 5 * * * * | Карточки товаров |
| sync.products.prices_full | 10 * * * * | Цены и скидки |

### Каждые 3 часа — маркетинг
| Задача | Cron | Описание |
|--------|------|----------|
| sync.promotion.campaigns_full | 20 */3 * * * | Рекламные кампании |
| sync.promotion.stats_full | 25 */3 * * * | Статистика кампаний |

### Раз в сутки — отчёты (03:00–03:45)
| Задача | Cron | Описание |
|--------|------|----------|
| sync.reports.stocks | 0 3 * * * | Остатки на складах |
| sync.reports.orders | 15 3 * * * | Отчёт по заказам |
| sync.reports.sales | 30 3 * * * | Отчёт по продажам |
| sync.finances.full | 45 3 * * * | Финансовый отчёт |

### Раз в сутки — тарифы (04:00–04:09)
| Задача | Cron | Описание |
|--------|------|----------|
| sync.tariffs.commissions | 0 4 * * * | Комиссии по категориям |
| sync.tariffs.box | 3 4 * * * | Тарифы коробов |
| sync.tariffs.pallet | 6 4 * * * | Тарифы паллет |
| sync.tariffs.supply | 9 4 * * * | Тарифы поставок |

### Раз в сутки — справочники (04:15–04:30)
| Задача | Cron | Описание |
|--------|------|----------|
| sync.products.directories_categories | 15 4 * * * | Категории товаров |
| sync.products.directories_subjects | 17 4 * * * | Предметы товаров |
| sync.products.tags_full | 20 4 * * * | Теги товаров |
| sync.products.warehouses_full | 25 4 * * * | Склады продавца |
| sync.promotion.calendar_full | 30 4 * * * | Промоакции WB |

### Раз в сутки — общее (05:00–05:10)
| Задача | Cron | Описание |
|--------|------|----------|
| sync.general.seller_full | 0 5 * * * | Информация о продавце |
| sync.general.news_full | 5 5 * * * | Новости (полная) |
| sync.general.news_incremental | 10 5 * * * | Новости (инкрементальная) |

## Retry-политика

Все задачи имеют:
- **max_retries:** 3
- **default_retry_delay:** 60 секунд (фиксированный)
- **autoretry_for:** Exception (любая ошибка)

Дополнительно в collectors/base.py:
- 3 retry при сетевых ошибках (2с x номер попытки)
- 60с пауза при 429 Too Many Requests
- Rate limiting по интервалам из WB API документации
