# WB Collector — Эндпоинты API

> Swagger UI: `http://localhost:8080/docs`  
> Всего эндпоинтов: ~300 (WB прокси + sync + db)

---

## 01 — General `/general`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/general/sync/seller/full` | Синхронизировать данные продавца |
| POST | `/general/sync/seller/incremental` | Инкрементальная синхронизация |
| POST | `/general/sync/news/full` | Все новости (Celery, ~3-5 мин) |
| POST | `/general/sync/news/incremental` | Только новые новости |
| POST | `/general/sync/users/full` | Список пользователей |
| POST | `/general/sync/users/incremental` | Только новые пользователи |
| POST | `/general/sync/rating/full` | Рейтинг продавца |
| POST | `/general/sync/rating/incremental` | Инкрементальный рейтинг |
| POST | `/general/sync/subscriptions/full` | Подписки (Джем) |
| POST | `/general/sync/subscriptions/incremental` | Инкрементальные подписки |

### DB
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/general/db/seller` | Данные продавца из БД |
| GET | `/general/db/news` | Новости из БД |
| GET | `/general/db/users` | Пользователи из БД |
| GET | `/general/db/rating` | Рейтинг из БД |
| GET | `/general/db/subscriptions` | Подписки из БД |

### WB прокси
| Метод | Путь |
|-------|------|
| GET | `/general/wb/ping` |
| GET | `/general/wb/seller` |
| GET | `/general/wb/news` |
| GET | `/general/wb/users` |
| POST | `/general/wb/users/invite` |
| PUT | `/general/wb/users/access` |
| DELETE | `/general/wb/users/{user_id}` |
| GET | `/general/wb/rating` |
| GET | `/general/wb/subscriptions` |

---

## 02 — Products `/products`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/products/sync/cards/full` | Все карточки товаров |
| POST | `/products/sync/cards/incremental` | Только обновлённые карточки |
| POST | `/products/sync/prices/full` | Все цены |
| POST | `/products/sync/prices/incremental` | Только изменённые цены |
| POST | `/products/sync/tags/full` | Теги |
| POST | `/products/sync/tags/incremental` | Инкрементальные теги |
| POST | `/products/sync/warehouses/full` | Склады продавца |
| POST | `/products/sync/warehouses/incremental` | Инкрементальные склады |
| POST | `/products/sync/directories/categories` | Категории |
| POST | `/products/sync/directories/categories/incremental` | Новые категории |
| POST | `/products/sync/directories/subjects` | Предметы |
| POST | `/products/sync/directories/subjects/incremental` | Новые предметы |

### DB
| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/products/db/cards` | Карточки из БД |
| GET | `/products/db/cards/{nm_id}` | Карточка по nmID |
| GET | `/products/db/prices` | Цены из БД |
| GET | `/products/db/prices/{nm_id}` | Цена по nmID |
| GET | `/products/db/tags` | Теги из БД |
| GET | `/products/db/warehouses` | Склады из БД |
| GET | `/products/db/directories/categories` | Категории из БД |
| GET | `/products/db/directories/subjects` | Предметы из БД |

---

## 03 — FBS `/fbs`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/fbs/sync/orders/full` | Все заказы FBS |
| POST | `/fbs/sync/orders/incremental` | Новые заказы (каждые 15 мин) |
| POST | `/fbs/sync/passes/full` | Пропуска |
| POST | `/fbs/sync/passes/incremental` | Новые пропуска |
| POST | `/fbs/sync/supplies/full` | Поставки FBS |
| POST | `/fbs/sync/supplies/incremental` | Новые поставки |

### DB
| Метод | Путь |
|-------|------|
| GET | `/fbs/db/orders` |
| GET | `/fbs/db/passes` |
| GET | `/fbs/db/supplies` |

---

## 04 — DBW `/dbw`

### Sync
| Метод | Путь |
|-------|------|
| POST | `/dbw/sync/orders/full` |
| POST | `/dbw/sync/orders/incremental` |

### DB
| Метод | Путь |
|-------|------|
| GET | `/dbw/db/orders` |

---

## 05 — DBS `/dbs`

### Sync
| Метод | Путь |
|-------|------|
| POST | `/dbs/sync/orders/full` |
| POST | `/dbs/sync/orders/incremental` |

### DB
| Метод | Путь |
|-------|------|
| GET | `/dbs/db/orders` |

---

## 06 — Pickup `/pickup`

### Sync
| Метод | Путь |
|-------|------|
| POST | `/pickup/sync/orders/full` |
| POST | `/pickup/sync/orders/incremental` |

### DB
| Метод | Путь |
|-------|------|
| GET | `/pickup/db/orders` |

---

## 07 — FBW `/fbw`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/fbw/sync/supplies/full` | Все поставки FBW |
| POST | `/fbw/sync/supplies/incremental` | Новые поставки |
| POST | `/fbw/sync/supplies/supply-goods` | Товары по всем поставкам |
| POST | `/fbw/sync/warehouses/full` | Склады WB |
| POST | `/fbw/sync/warehouses/incremental` | Новые склады |
| POST | `/fbw/sync/transit-tariffs/full` | Тарифы транзита |
| POST | `/fbw/sync/transit-tariffs/incremental` | Новые тарифы |

### DB
| Метод | Путь |
|-------|------|
| GET | `/fbw/db/supplies` |
| GET | `/fbw/db/supplies/{supply_id}` |
| GET | `/fbw/db/supplies/{supply_id}/goods` |
| GET | `/fbw/db/warehouses` |
| GET | `/fbw/db/transit-tariffs` |

---

## 08 — Promotion `/promotion`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/promotion/sync/campaigns/full` | Все кампании |
| POST | `/promotion/sync/campaigns/incremental` | Новые кампании |
| POST | `/promotion/sync/stats/full` | Статистика кампаний (Celery) |
| POST | `/promotion/sync/stats/incremental` | Новая статистика |
| POST | `/promotion/sync/calendar/full` | Календарь акций |
| POST | `/promotion/sync/calendar/incremental` | Новые акции |

### DB
| Метод | Путь |
|-------|------|
| GET | `/promotion/db/campaigns` |
| GET | `/promotion/db/stats` |
| GET | `/promotion/db/calendar` |

---

## 09 — Communications `/communications`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/communications/sync/feedbacks/full` | Все отзывы (30 дней) |
| POST | `/communications/sync/feedbacks/incremental` | Новые отзывы |
| POST | `/communications/sync/questions/full` | Все вопросы |
| POST | `/communications/sync/questions/incremental` | Новые вопросы |
| POST | `/communications/sync/claims/full` | Все претензии |
| POST | `/communications/sync/claims/incremental` | Новые претензии |
| POST | `/communications/sync/chats/full` | Чаты покупателей |
| POST | `/communications/sync/chats/incremental` | Новые чаты |

### DB
| Метод | Путь |
|-------|------|
| GET | `/communications/db/feedbacks` |
| GET | `/communications/db/questions` |
| GET | `/communications/db/claims` |
| GET | `/communications/db/chats` |

---

## 10 — Tariffs `/tariffs`

### Sync
| Метод | Путь | Данных в БД |
|-------|------|------------|
| POST | `/tariffs/sync/commissions/full` | ~7391 |
| POST | `/tariffs/sync/commissions/incremental` | — |
| POST | `/tariffs/sync/box/full` | ~83 |
| POST | `/tariffs/sync/box/incremental` | — |
| POST | `/tariffs/sync/pallet/full` | ~91 |
| POST | `/tariffs/sync/pallet/incremental` | — |
| POST | `/tariffs/sync/supply/full` | ~6705 |
| POST | `/tariffs/sync/supply/incremental` | — |

### DB
| Метод | Путь |
|-------|------|
| GET | `/tariffs/db/commissions` |
| GET | `/tariffs/db/box` |
| GET | `/tariffs/db/pallet` |
| GET | `/tariffs/db/supply` |

---

## 11 — Analytics `/analytics`

### Sync
| Метод | Путь |
|-------|------|
| POST | `/analytics/sync/funnel/full` |
| POST | `/analytics/sync/funnel/incremental` |
| POST | `/analytics/sync/stocks/full` |
| POST | `/analytics/sync/stocks/incremental` |
| POST | `/analytics/sync/search/full` |
| POST | `/analytics/sync/search/incremental` |

### DB
| Метод | Путь |
|-------|------|
| GET | `/analytics/db/funnel` |
| GET | `/analytics/db/stocks` |
| GET | `/analytics/db/search` |

---

## 12 — Reports `/reports`

### Sync (все тяжёлые — через Celery, возвращают `task_id`)
| Метод | Путь |
|-------|------|
| POST | `/reports/sync/stocks/full` |
| POST | `/reports/sync/stocks/incremental` |
| POST | `/reports/sync/orders/full` |
| POST | `/reports/sync/orders/incremental` |
| POST | `/reports/sync/sales/full` |
| POST | `/reports/sync/sales/incremental` |

### DB
| Метод | Путь | Данных в БД |
|-------|------|------------|
| GET | `/reports/db/stocks` | ~719 |
| GET | `/reports/db/orders` | ~400,057 |
| GET | `/reports/db/sales` | ~79,102 |

---

## 13 — Finances `/finances`

### Sync
| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/finances/sync/full` | Полная выгрузка (Celery, возвращает `task_id`) |
| POST | `/finances/sync/incremental` | Только новые записи |

### DB
| Метод | Путь | Данных в БД |
|-------|------|------------|
| GET | `/finances/db` | ~1,034,759 |

---

## Формат ответов DB-эндпоинтов

```json
{
  "data": [...],
  "total": 1234,
  "limit": 100,
  "offset": 0
}
```

## Формат ответов sync-эндпоинтов

```json
{ "synced": 150 }
```

Для Celery (тяжёлые задачи):
```json
{ "task_id": "uuid", "status": "queued" }
```
