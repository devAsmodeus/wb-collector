import base64, json, sys

token = sys.argv[1] if len(sys.argv) > 1 else ""
if not token:
    token = "***REDACTED***"

payload = token.split(".")[1]
payload += "=" * (4 - len(payload) % 4)
data = json.loads(base64.urlsafe_b64decode(payload))
print(json.dumps(data, indent=2, ensure_ascii=False))

s = data.get("s", 0)
print(f"\ns = {s}  (binary: {s:016b})")

# Битовая маска скоупов WB API (из документации)
SCOPES = {
    1:    "Контент",
    2:    "Аналитика",
    4:    "Цены и скидки",
    8:    "Маркетплейс (FBS)",
    16:   "Статистика",
    32:   "Продвижение (реклама)",
    64:   "Вопросы и отзывы",
    128:  "Чат с покупателями",
    256:  "Поставки",
    512:  "Финансы",
    1024: "Аналитика расширенная",
    2048: "Тарифы",
    4096: "Управление пользователями",
}

print("\nРазрешения токена:")
for bit, name in SCOPES.items():
    mark = "OK" if (s & bit) else "--"
    print(f"  [{mark}] {name} (bit {bit})")
