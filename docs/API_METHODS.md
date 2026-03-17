# WB Collector — Полный справочник методов API

> Всего: **268 методов**, **250 путей**, **13 глав WB API**  
> Документация OpenAPI: `http://localhost:8080/docs`  
> Сервер: `http://168.119.79.244:8080`

---

## 01 — General

Base path: `/general`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/general/seller` | Информация о продавце | General — Продавец |
| GET | `/general/seller/warehouses` | Склады продавца | General — Продавец |
| POST | `/general/seller/warehouses` | Создать склад | General — Продавец |
| GET | `/general/news` | Новости WB | General — Новости |
| GET | `/general/users` | Пользователи | General — Пользователи |
| POST | `/general/users` | Создать пользователя | General — Пользователи |
| PATCH | `/general/users` | Обновить пользователя | General — Пользователи |
| DELETE | `/general/users` | Удалить пользователя | General — Пользователи |

---

## 02 — Products (Контент)

Base path: `/products`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/products/cards` | Список карточек | Products — Карточки |
| POST | `/products/cards` | Создать карточку | Products — Карточки |
| PATCH | `/products/cards` | Обновить карточку | Products — Карточки |
| POST | `/products/cards/error/list` | Ошибки карточек | Products — Карточки |
| GET | `/products/cards/trash` | Карточки в корзине | Products — Карточки |
| POST | `/products/cards/trash/recover` | Восстановить из корзины | Products — Карточки |
| DELETE | `/products/cards/trash` | Удалить из корзины | Products — Карточки |
| GET | `/products/tags` | Список тегов | Products — Теги |
| POST | `/products/tags` | Создать тег | Products — Теги |
| PUT | `/products/tags/{id}` | Обновить тег | Products — Теги |
| DELETE | `/products/tags/{id}` | Удалить тег | Products — Теги |
| POST | `/products/tags/goods/add` | Добавить тег к товару | Products — Теги |
| GET | `/products/prices` | Цены и скидки | Products — Цены |
| POST | `/products/prices` | Установить цены | Products — Цены |
| POST | `/products/prices/discount` | Установить скидки | Products — Цены |
| POST | `/products/prices/discount/delete` | Удалить скидки | Products — Цены |
| GET | `/products/prices/history` | История цен | Products — Цены |
| GET | `/products/prices/task/{taskId}` | Статус задачи цен | Products — Цены |
| POST | `/products/prices/size` | Цены по размерам | Products — Цены |
| GET | `/products/warehouses` | Склады | Products — Склады |
| GET | `/products/warehouses/{warehouseId}` | Склад по ID | Products — Склады |
| GET | `/products/warehouses/coefficient` | Коэффициент склада | Products — Склады |
| GET | `/products/categories/subjects` | Предметы категорий | Products — Справочники |
| GET | `/products/categories/characteristics` | Характеристики | Products — Справочники |
| GET | `/products/categories/colors` | Цвета | Products — Справочники |
| GET | `/products/categories/kinds` | Виды (пол) | Products — Справочники |
| GET | `/products/categories/countries` | Страны | Products — Справочники |

---

## 03 — FBS (Сборка и доставка продавцом)

Base path: `/fbs`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/fbs/passes` | Пропуска | Пропуска FBS |
| POST | `/fbs/passes` | Создать пропуск | Пропуска FBS |
| PATCH | `/fbs/passes` | Обновить пропуск | Пропуска FBS |
| DELETE | `/fbs/passes` | Удалить пропуск | Пропуска FBS |
| GET | `/fbs/passes/gates` | Ворота склада | Пропуска FBS |
| GET | `/fbs/orders` | Список заказов | Сборочные задания FBS |
| GET | `/fbs/orders/new` | Новые заказы | Сборочные задания FBS |
| GET | `/fbs/orders/status` | Статусы заказов | Сборочные задания FBS |
| POST | `/fbs/orders/status` | Обновить статусы | Сборочные задания FBS |
| GET | `/fbs/orders/stickers` | Стикеры заказов | Сборочные задания FBS |
| POST | `/fbs/orders/stickers` | Создать стикеры | Сборочные задания FBS |
| GET | `/fbs/orders/{orderId}/sticker` | Стикер заказа | Сборочные задания FBS |
| POST | `/fbs/orders/{orderId}/cancel` | Отмена заказа | Сборочные задания FBS |
| PATCH | `/fbs/orders/sgtin` | SGTIN заказа | Сборочные задания FBS |
| GET | `/fbs/meta/offices` | Склады FBS | Метаданные FBS |
| GET | `/fbs/meta/warehouses` | Склады WB | Метаданные FBS |
| GET | `/fbs/meta/boxes` | Типы упаковок | Метаданные FBS |
| GET | `/fbs/meta/statuses` | Статусы | Метаданные FBS |
| POST | `/fbs/meta/offices` | Создать склад | Метаданные FBS |
| PUT | `/fbs/meta/offices/{id}` | Обновить склад | Метаданные FBS |
| DELETE | `/fbs/meta/offices/{id}` | Удалить склад | Метаданные FBS |
| PATCH | `/fbs/meta/orders/{orderId}` | Мета заказа | Метаданные FBS |
| GET | `/fbs/supplies` | Поставки | Поставки FBS |
| POST | `/fbs/supplies` | Создать поставку | Поставки FBS |
| GET | `/fbs/supplies/{supplyId}` | Поставка по ID | Поставки FBS |
| DELETE | `/fbs/supplies/{supplyId}` | Удалить поставку | Поставки FBS |
| POST | `/fbs/supplies/{supplyId}/orders` | Добавить заказы | Поставки FBS |
| GET | `/fbs/supplies/{supplyId}/barcode` | Штрихкод поставки | Поставки FBS |
| GET | `/fbs/supplies/{supplyId}/stickers` | Стикеры поставки | Поставки FBS |
| PUT | `/fbs/supplies/{supplyId}/deliver` | Передать в доставку | Поставки FBS |
| GET | `/fbs/supplies/trbx` | Короба поставки | Поставки FBS |
| POST | `/fbs/supplies/trbx` | Создать короб | Поставки FBS |
| DELETE | `/fbs/supplies/trbx` | Удалить короб | Поставки FBS |
| GET | `/fbs/supplies/trbx/stickers` | Стикеры коробов | Поставки FBS |

---

## 04 — DBW (Доставка WB)

Base path: `/dbw`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/dbw/orders` | Список заказов DBW | Сборочные задания DBW |
| GET | `/dbw/orders/new` | Новые заказы | Сборочные задания DBW |
| GET | `/dbw/orders/{orderId}` | Заказ по ID | Сборочные задания DBW |
| POST | `/dbw/orders/{orderId}/cancel` | Отмена заказа | Сборочные задания DBW |
| GET | `/dbw/orders/stickers` | Стикеры заказов | Сборочные задания DBW |
| POST | `/dbw/orders/stickers` | Создать стикеры | Сборочные задания DBW |
| PATCH | `/dbw/orders/sgtin` | SGTIN заказа | Сборочные задания DBW |
| GET | `/dbw/orders/status` | Статусы заказов | Сборочные задания DBW |
| POST | `/dbw/orders/status` | Обновить статусы | Сборочные задания DBW |
| PATCH | `/dbw/orders/{orderId}/meta` | Мета заказа | Сборочные задания DBW |
| GET | `/dbw/meta/offices` | Склады DBW | Метаданные DBW |
| GET | `/dbw/meta/warehouses` | Склады WB | Метаданные DBW |
| GET | `/dbw/meta/statuses` | Статусы | Метаданные DBW |
| POST | `/dbw/meta/offices` | Создать склад | Метаданные DBW |
| PUT | `/dbw/meta/offices/{id}` | Обновить склад | Метаданные DBW |
| DELETE | `/dbw/meta/offices/{id}` | Удалить склад | Метаданные DBW |

---

## 05 — DBS (Доставка продавцом)

Base path: `/dbs`

| Метод | Путь | Описание | Тег | Deprecated |
|-------|------|----------|-----|-----------|
| GET | `/dbs/orders` | Список заказов | Сборочные задания DBS | |
| GET | `/dbs/orders/new` | Новые заказы | Сборочные задания DBS | |
| GET | `/dbs/orders/{orderId}` | Заказ по ID | Сборочные задания DBS | |
| POST | `/dbs/orders/{orderId}/cancel` | Отмена | Сборочные задания DBS | |
| GET | `/dbs/orders/stickers` | Стикеры | Сборочные задания DBS | |
| POST | `/dbs/orders/stickers` | Создать стикеры | Сборочные задания DBS | |
| GET | `/dbs/orders/status` | Статусы | Сборочные задания DBS | |
| POST | `/dbs/orders/status` | Обновить статусы | Сборочные задания DBS | |
| PATCH | `/dbs/orders/status/deliver` | Статус доставки | Сборочные задания DBS | |
| PATCH | `/dbs/orders/status/receive` | Статус получения | Сборочные задания DBS | |
| PATCH | `/dbs/orders/status/reject` | Отклонить заказ | Сборочные задания DBS | |
| GET | `/dbs/orders/courier` | Данные курьера | Сборочные задания DBS | |
| PATCH | `/dbs/orders/{orderId}/meta` | Мета заказа | Сборочные задания DBS | |
| GET | `/dbs/orders/{orderId}/chauffeur` | Водитель | Сборочные задания DBS | |
| POST | `/dbs/orders/{orderId}/chauffeur` | Назначить водителя | Сборочные задания DBS | |
| GET | `/dbs/orders/phone` | Телефон покупателя | Сборочные задания DBS | |
| GET | `/dbs/orders/delivery-address` | Адрес доставки | Сборочные задания DBS | |
| PATCH | `/dbs/orders/dispatch-number` | Номер отправки | Сборочные задания DBS | |
| GET | `/dbs/orders/track-number` | Трек-номер | Сборочные задания DBS | |
| GET | `/dbs/meta/offices` | Склады DBS | Метаданные DBS | |
| GET | `/dbs/meta/warehouses` | Склады WB | Метаданные DBS | |
| GET | `/dbs/meta/statuses` | Статусы | Метаданные DBS | |
| POST | `/dbs/meta` | Обновить мета (bulk) | Метаданные DBS | |
| GET | `/dbs/meta/{orderId}` | Мета заказа | Метаданные DBS | |
| PUT | `/dbs/meta/imei` | IMEI заказа | Метаданные DBS | ⚠️ |
| PUT | `/dbs/meta/uin` | UIN заказа | Метаданные DBS | ⚠️ |
| PUT | `/dbs/meta/gtin` | GTIN заказа | Метаданные DBS | ⚠️ |
| PUT | `/dbs/meta/sgtin` | SGTIN заказа | Метаданные DBS | ⚠️ |
| DELETE | `/dbs/meta/imei/{orderId}` | Удалить IMEI | Метаданные DBS | ⚠️ |
| DELETE | `/dbs/meta/uin/{orderId}` | Удалить UIN | Метаданные DBS | ⚠️ |
| DELETE | `/dbs/meta/gtin/{orderId}` | Удалить GTIN | Метаданные DBS | ⚠️ |
| DELETE | `/dbs/meta/sgtin/{orderId}` | Удалить SGTIN | Метаданные DBS | ⚠️ |

---

## 06 — Самовывоз (Click & Collect)

Base path: `/pickup`

Аналогично DBS — 28 методов, 12 deprecated. Полный список: `/docs`.

---

## 07 — FBW (Fulfilment by WB)

Base path: `/fbw`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| POST | `/fbw/acceptance/options` | Опции приёмки | Информация для формирования поставок |
| GET | `/fbw/acceptance/warehouses` | Склады FBW | Информация для формирования поставок |
| GET | `/fbw/acceptance/transit-tariffs` | Транзитные тарифы | Информация для формирования поставок |
| POST | `/fbw/supplies` | Список поставок | Информация о поставках |
| GET | `/fbw/supplies/{ID}` | Поставка по ID | Информация о поставках |
| GET | `/fbw/supplies/{ID}/goods` | Товары поставки | Информация о поставках |
| GET | `/fbw/supplies/{ID}/package` | Упаковка поставки | Информация о поставках |

---

## 08 — Маркетинг (Promotion)

Base path: `/promotion`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/promotion/promotion/count` | Количество кампаний | Кампании |
| GET | `/promotion/adverts` | Список кампаний | Кампании |
| POST | `/promotion/bids/min` | Минимальные ставки | Кампании |
| GET | `/promotion/bids/recommendations` | Рекомендации ставок | Кампании |
| GET | `/promotion/subjects` | Предметы кампаний | Создание кампаний |
| POST | `/promotion/nms` | Артикулы для кампаний | Создание кампаний |
| POST | `/promotion/campaign` | Создать кампанию | Создание кампаний |
| GET | `/promotion/campaign/delete` | Удалить кампанию | Управление кампаниями |
| POST | `/promotion/campaign/rename` | Переименовать | Управление кампаниями |
| GET | `/promotion/campaign/start` | Запустить | Управление кампаниями |
| GET | `/promotion/campaign/pause` | На паузу | Управление кампаниями |
| GET | `/promotion/campaign/stop` | Завершить | Управление кампаниями |
| PUT | `/promotion/auction/placements` | Места размещения | Управление кампаниями |
| PATCH | `/promotion/bids` | Обновить ставки | Управление кампаниями |
| PATCH | `/promotion/auction/nms` | Обновить артикулы | Управление кампаниями |
| GET | `/promotion/balance` | Баланс кабинета | Финансы |
| GET | `/promotion/budget` | Бюджет кампании | Финансы |
| POST | `/promotion/budget/deposit` | Пополнить бюджет | Финансы |
| GET | `/promotion/upd` | УПД | Финансы |
| GET | `/promotion/payments` | История платежей | Финансы |
| POST | `/promotion/normquery/stats` | Статистика кластеров v0 | Поисковые кластеры |
| POST | `/promotion/normquery/bids/get` | Ставки кластеров | Поисковые кластеры |
| POST | `/promotion/normquery/bids` | Установить ставки | Поисковые кластеры |
| DELETE | `/promotion/normquery/bids` | Удалить ставки | Поисковые кластеры |
| POST | `/promotion/normquery/minus/get` | Минус-слова | Поисковые кластеры |
| POST | `/promotion/normquery/minus` | Установить минус | Поисковые кластеры |
| POST | `/promotion/normquery/list` | Список кластеров | Поисковые кластеры |
| POST | `/promotion/normquery/stats/v1` | Статистика кластеров v1 | Поисковые кластеры |
| GET | `/promotion/fullstats` | Полная статистика | Статистика |
| POST | `/promotion/stats` | Статистика (детально) | Статистика |
| GET | `/promotion/media/count` | Кол-во медиакампаний | Медиа |
| GET | `/promotion/media/adverts` | Список медиакампаний | Медиа |
| GET | `/promotion/media/advert` | Медиакампания по ID | Медиа |
| GET | `/promotion/promotions/` | Список акций | Календарь акций |
| GET | `/promotion/promotions/details` | Детали акции | Календарь акций |
| GET | `/promotion/promotions/nomenclatures` | Товары акции | Календарь акций |
| POST | `/promotion/promotions/upload` | Загрузить в акцию | Календарь акций |

---

## 09 — Коммуникации

Base path: `/communications`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/communications/new-feedbacks-questions` | Новые отзывы/вопросы | Отзывы |
| GET | `/communications/questions/count-unanswered` | Неотвеченные вопросы | Вопросы |
| GET | `/communications/questions/count` | Статистика вопросов | Вопросы |
| GET | `/communications/questions/` | Список вопросов | Вопросы |
| PATCH | `/communications/questions/` | Ответить на вопрос | Вопросы |
| GET | `/communications/questions/{id}` | Один вопрос | Вопросы |
| GET | `/communications/feedbacks/count-unanswered` | Необработанные отзывы | Отзывы |
| GET | `/communications/feedbacks/count` | Статистика отзывов | Отзывы |
| GET | `/communications/feedbacks/` | Список отзывов | Отзывы |
| POST | `/communications/feedbacks/answer` | Ответить на отзыв | Отзывы |
| PATCH | `/communications/feedbacks/answer` | Редактировать ответ | Отзывы |
| POST | `/communications/feedbacks/return` | Запрос возврата | Возвраты |
| GET | `/communications/feedbacks/{id}` | Один отзыв | Отзывы |
| GET | `/communications/feedbacks/archive` | Архив отзывов | Возвраты |
| GET | `/communications/pins/` | Закреплённые отзывы | Закреплённые отзывы |
| POST | `/communications/pins/` | Закрепить отзыв | Закреплённые отзывы |
| DELETE | `/communications/pins/` | Открепить отзыв | Закреплённые отзывы |
| GET | `/communications/pins/count` | Кол-во закреплённых | Закреплённые отзывы |
| GET | `/communications/pins/limits` | Лимиты | Закреплённые отзывы |
| GET | `/communications/chat/chats` | Список чатов | Чат с покупателями |
| GET | `/communications/chat/events` | События чата | Чат с покупателями |
| POST | `/communications/chat/message` | Отправить сообщение | Чат с покупателями |
| GET | `/communications/chat/download/{id}` | Скачать файл | Чат с покупателями |
| GET | `/communications/claims/` | Претензии | Возвраты |
| PATCH | `/communications/claims/` | Обработать претензию | Возвраты |

---

## 10 — Тарифы

Base path: `/tariffs`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/tariffs/tariffs/commission` | Комиссии по категориям | Комиссии |
| GET | `/tariffs/tariffs/seller` | Стоимость возврата | Стоимость возврата продавцу |
| GET | `/tariffs/tariffs/box` | Тарифы: короба | Тарифы на остаток |
| GET | `/tariffs/tariffs/pallet` | Тарифы: паллеты | Тарифы на остаток |
| GET | `/tariffs/tariffs/supply` | Коэффициенты складов | Тарифы на поставку |

---

## 11 — Аналитика

Base path: `/analytics`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| POST | `/analytics/analytics/funnel/products` | Воронка по товарам | Воронка продаж |
| POST | `/analytics/analytics/funnel/products/history` | История воронки | Воронка продаж |
| POST | `/analytics/analytics/funnel/grouped/history` | Сгруппированная история | Воронка продаж |
| POST | `/analytics/analytics/nm-report` | Создать CSV-отчёт | Аналитика продавца CSV |
| GET | `/analytics/analytics/nm-report` | Список задач | Аналитика продавца CSV |
| POST | `/analytics/analytics/nm-report/retry` | Повторить задачу | Аналитика продавца CSV |
| GET | `/analytics/analytics/nm-report/file/{id}` | Скачать CSV | Аналитика продавца CSV |
| POST | `/analytics/analytics/search/report` | Отчёт поисковых запросов | Поисковые запросы |
| POST | `/analytics/analytics/search/groups` | Группы запросов | Поисковые запросы |
| POST | `/analytics/analytics/search/details` | Детализация запросов | Поисковые запросы |
| POST | `/analytics/analytics/search/texts` | Тексты запросов | Поисковые запросы |
| POST | `/analytics/analytics/search/orders` | Заказы из поиска | Поисковые запросы |
| POST | `/analytics/analytics/stocks/groups` | Остатки по группам | История остатков |
| POST | `/analytics/analytics/stocks/products` | Остатки по артикулам | История остатков |
| POST | `/analytics/analytics/stocks/sizes` | Остатки по размерам | История остатков |
| POST | `/analytics/analytics/stocks/offices` | Остатки по складам | История остатков |

---

## 12 — Отчёты

Base path: `/reports`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/reports/reports/stocks` | Остатки на складах | Основные отчёты |
| GET | `/reports/reports/orders` | Заказы | Основные отчёты |
| GET | `/reports/reports/sales` | Продажи и возвраты | Основные отчёты |
| POST | `/reports/reports/excise` | Маркированные товары | Маркировка |
| GET | `/reports/reports/warehouse-remains` | Создать задачу остатков | Отчёт об остатках |
| GET | `/reports/reports/warehouse-remains/tasks/{id}/status` | Статус задачи | Отчёт об остатках |
| GET | `/reports/reports/warehouse-remains/tasks/{id}/download` | Скачать отчёт | Отчёт об остатках |
| GET | `/reports/reports/penalties/measurements` | Штрафы за обмеры | Удержания |
| GET | `/reports/reports/measurements/warehouse` | Данные обмеров | Удержания |
| GET | `/reports/reports/deductions` | Удержания | Удержания |
| GET | `/reports/reports/antifraud` | Антифрод | Удержания |
| GET | `/reports/reports/labeling` | Товары с маркировкой | Маркировка |
| GET | `/reports/reports/acceptance` | Создать задачу приёмки | Операции при приёмке |
| GET | `/reports/reports/acceptance/tasks/{id}/status` | Статус задачи | Операции при приёмке |
| GET | `/reports/reports/acceptance/tasks/{id}/download` | Скачать отчёт | Операции при приёмке |
| GET | `/reports/reports/paid-storage` | Создать задачу хранения | Платное хранение |
| GET | `/reports/reports/paid-storage/tasks/{id}/status` | Статус задачи | Платное хранение |
| GET | `/reports/reports/paid-storage/tasks/{id}/download` | Скачать отчёт | Платное хранение |
| GET | `/reports/reports/region-sale` | Продажи по регионам | Продажи по регионам |
| GET | `/reports/reports/brand/brands` | Бренды | Доля бренда |
| GET | `/reports/reports/brand/parent-subjects` | Категории для доли | Доля бренда |
| GET | `/reports/reports/brand/share` | Доля бренда | Доля бренда |
| GET | `/reports/reports/hidden/blocked` | Заблокированные товары | Скрытые товары |
| GET | `/reports/reports/hidden/shadowed` | Частично скрытые | Скрытые товары |
| GET | `/reports/reports/returns` | Возвраты товаров | Возвраты |

---

## 13 — Финансы

Base path: `/finances`

| Метод | Путь | Описание | Тег |
|-------|------|----------|-----|
| GET | `/finances/finances/balance` | Баланс продавца | Баланс |
| GET | `/finances/finances/report` | Финансовый отчёт | Финансовые отчёты |
| GET | `/finances/finances/documents/categories` | Категории документов | Документы |
| GET | `/finances/finances/documents` | Список документов | Документы |
| GET | `/finances/finances/documents/download` | Скачать документ | Документы |
| POST | `/finances/finances/documents/download/all` | Скачать все документы | Документы |

---

## ⚠️ Deprecated endpoints

В модулях DBS и Самовывоз есть 24 deprecated эндпоинта (помечены в OpenAPI).  
Они работают, но WB рекомендует использовать новые аналоги с bulk-операциями.

---

## 🔒 Ограничения токена

Текущий токен `s=7934` имеет скоупы:

| Модуль | Доступ |
|--------|--------|
| Analytics | ✅ |
| Prices/Discounts | ✅ |
| Marketplace FBS | ✅ |
| Statistics | ✅ |
| Promotion | ✅ |
| Q&A / Chat | ✅ |
| Finance | ✅ |
| Content (Products) | ❌ |
| Supplies (FBW) | ❌ |

---

*Последнее обновление: 2026-03-17 | commit `60c3cf4`*
