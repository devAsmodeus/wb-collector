"""
Python Tricks — Дэн Бейдер
Глава 1: Паттерны чистого Python
Интерактивный разбор с примерами
"""
import os
import time


# ─── Утилиты ─────────────────────────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\n  ↵  Нажми Enter чтобы продолжить...")

def header(title, subtitle=""):
    print("\n" + "═" * 60)
    print(f"  {title}")
    if subtitle:
        print(f"  {subtitle}")
    print("═" * 60)

def section(title):
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print('─' * 60)

def show_code(code):
    print()
    for line in code.strip().split('\n'):
        print(f"  {line}")
    print()

def run_demo(title, fn):
    print(f"\n  ▶  {title}")
    print("  " + "·" * 40)
    fn()
    print()

def menu(items):
    print()
    for i, item in enumerate(items, 1):
        print(f"  [{i}] {item}")
    print("  [0] Выход")
    print()
    while True:
        choice = input("  Выбор: ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(items):
            return int(choice)
        print("  Введи номер из списка")


# ─── Темы ────────────────────────────────────────────────────────────────────

def topic_assertions():
    clear()
    header("1. ASSERT — Утверждения", "Проверка инвариантов, а не обработка ошибок")

    section("Что такое assert")
    print("""
  assert <условие>, "Сообщение об ошибке"

  Если условие False → бросает AssertionError.
  Если условие True  → ничего не происходит.

  Главное правило: assert — для проверки того,
  что НИКОГДА не должно случиться.
  Не для валидации пользовательского ввода!
""")

    pause()
    section("Пример 1 — правильное использование")
    show_code("""
def apply_discount(price, discount):
    assert 0 <= discount <= 1, "Скидка должна быть от 0 до 1"
    return price * (1 - discount)
""")

    def demo1():
        def apply_discount(price, discount):
            assert 0 <= discount <= 1, "Скидка должна быть от 0 до 1"
            return price * (1 - discount)

        print(f"  apply_discount(100, 0.2)  → {apply_discount(100, 0.2)}")
        try:
            apply_discount(100, 1.5)
        except AssertionError as e:
            print(f"  apply_discount(100, 1.5) → AssertionError: {e}")

    run_demo("Запускаем", demo1)

    pause()
    section("⚠️  Ловушка — assert можно отключить!")
    show_code("""
# Запуск с флагом -O отключает ВСЕ assert:
# python -O script.py

# Поэтому НИКОГДА не пиши так:
def delete_user(user_id):
    assert user_id > 0, "ID должен быть > 0"  # ← может быть отключён!
    ...

# Пиши так — это всегда проверяется:
def delete_user(user_id):
    if user_id <= 0:
        raise ValueError("ID должен быть > 0")
    ...
""")
    pause()


def topic_commas():
    clear()
    header("2. ВИСЯЩИЕ ЗАПЯТЫЕ", "Маленький трюк, большая польза")

    section("Проблема без висящей запятой")
    show_code("""
# Добавляем 'Сергей' — легко забыть запятую после 'Мария'
names = ['Иван',
         'Мария'    # ← забыли запятую!
         'Сергей']

# Python молча склеит строки: 'МарияСергей' — баг!
""")

    def demo1():
        # Демонстрируем конкатенацию строк
        result = ['Иван', 'Мария' 'Сергей']
        print(f"  Результат: {result}")
        print(f"  Ожидали 3 элемента, получили {len(result)}!")
        print(f"  'Мария' + 'Сергей' = '{result[1]}'  ← баг!")

    run_demo("Что происходит без запятой:", demo1)

    pause()
    section("✅  Решение — висящая запятая")
    show_code("""
names = [
    'Иван',
    'Мария',
    'Сергей',   # ← запятая. Теперь добавлять новые строки безопасно
]
""")

    def demo2():
        names = [
            'Иван',
            'Мария',
            'Сергей',
        ]
        print(f"  Результат: {names}")
        print(f"  Элементов: {len(names)} ✓")

    run_demo("Правильный вариант:", demo2)

    pause()
    section("Работает везде: списки, словари, функции")
    show_code("""
# Словарь
user = {
    'name': 'Иван',
    'age': 30,
    'role': 'admin',  # ← запятая
}

# Аргументы функции
def create_user(
    name,
    age,
    role='user',   # ← запятая
):
    ...
""")
    pause()


def topic_context_managers():
    clear()
    header("3. CONTEXT MANAGERS", "Паттерн: открыть → использовать → закрыть")

    section("Проблема без with")
    show_code("""
# Плохо — если будет исключение, файл не закроется
f = open('file.txt', 'r')
data = f.read()       # ← а вдруг здесь ошибка?
f.close()             # ← тогда это не выполнится!
""")

    pause()
    section("✅  Решение — with statement")
    show_code("""
# Хорошо — файл закроется В ЛЮБОМ случае
with open('file.txt', 'r') as f:
    data = f.read()
# f.close() вызовется автоматически
""")

    def demo1():
        import tempfile, os
        # создаём временный файл
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        tmp.write("Привет из файла!")
        tmp.close()

        with open(tmp.name, 'r') as f:
            data = f.read()
            print(f"  Прочитали: '{data}'")
            print(f"  Файл открыт: {not f.closed}")
        print(f"  После with, файл закрыт: {f.closed} ✓")
        os.unlink(tmp.name)

    run_demo("Демо:", demo1)

    pause()
    section("Как работает изнутри — магические методы")
    show_code("""
class ManagedFile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):          # вызывается при входе в with
        self.file = open(self.name, 'r')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):   # вызывается при выходе
        self.file.close()
        return False  # False = не подавлять исключения

# Использование:
with ManagedFile('file.txt') as f:
    data = f.read()
""")

    pause()
    section("Проще — через @contextmanager")
    show_code("""
from contextlib import contextmanager

@contextmanager
def managed_file(name):
    f = open(name, 'r')
    try:
        yield f         # ← всё что до yield — это __enter__
    finally:
        f.close()       # ← всё что в finally — это __exit__

with managed_file('file.txt') as f:
    data = f.read()
""")

    def demo2():
        from contextlib import contextmanager

        @contextmanager
        def timer(label):
            start = time.monotonic()
            print(f"  ⏱  {label} — старт")
            yield
            elapsed = time.monotonic() - start
            print(f"  ⏱  {label} — финиш: {elapsed:.4f} сек")

        with timer("Долгая операция"):
            time.sleep(0.3)
            print(f"  Работаем...")

    run_demo("Свой context manager — таймер:", demo2)
    pause()


def topic_underscores():
    clear()
    header("4. ПОДЧЁРКИВАНИЯ И ДАНДЕРЫ", "Соглашения об именовании в Python")

    conventions = [
        ("_var",    "Внутренний",     "Не импортируется через 'import *'. Подсказка: не трогай."),
        ("__var",   "Приватный",      "Name mangling — Python переименует в _ClassName__var"),
        ("__var__", "Дандер",         "Магические методы Python. Не создавай свои!"),
        ("var_",    "Избегаем конф.", "Конфликт с ключевым словом: class_ = 'admin'"),
        ("_",       "Одноразовый",    "Значение не нужно. for _ in range(5):"),
    ]

    section("5 видов подчёркиваний")
    for name, title, desc in conventions:
        print(f"\n  {name:10}  →  {title}")
        print(f"             {desc}")

    pause()
    section("_var — внутренний (одно подчёркивание)")
    show_code("""
class User:
    def __init__(self):
        self.name = 'Иван'    # публичный
        self._email = '...'   # внутренний — "не трогай напрямую"

# Технически доступен, но это нарушение соглашения:
u = User()
print(u._email)  # работает, но так не принято
""")

    def demo1():
        class User:
            def __init__(self):
                self.name = 'Иван'
                self._email = 'ivan@example.com'

        u = User()
        print(f"  u.name   = {u.name}    ← публичный ✓")
        print(f"  u._email = {u._email}  ← 'внутренний', но доступен")

    run_demo("Демо:", demo1)

    pause()
    section("__var — name mangling (два подчёркивания)")
    show_code("""
class MyClass:
    def __init__(self):
        self.__secret = 42   # Python переименует в _MyClass__secret

obj = MyClass()
# obj.__secret          → AttributeError
# obj._MyClass__secret  → 42  (обходной путь, но зачем?)
""")

    def demo2():
        class MyClass:
            def __init__(self):
                self.__secret = 42

        obj = MyClass()
        try:
            _ = obj.__secret
        except AttributeError as e:
            print(f"  obj.__secret       → AttributeError ✓")
        print(f"  obj._MyClass__secret → {obj._MyClass__secret}")
        print(f"\n  Атрибуты объекта: {[a for a in dir(obj) if 'secret' in a]}")

    run_demo("Демо:", demo2)

    pause()
    section("_ — одноразовая переменная")
    show_code("""
# Не нужен счётчик — используй _
for _ in range(3):
    print("Привет!")

# Не нужны все значения при распаковке
x, _, z = (1, 2, 3)   # нужны только x и z

# В интерпретаторе _ = результат последней операции
>>> 1 + 2
3
>>> _
3
""")

    def demo3():
        print("  for _ in range(3): print('Привет!')")
        for _ in range(3):
            print(f"  Привет!")

        x, _, z = (10, 99, 30)
        print(f"\n  x, _, z = (10, 99, 30)")
        print(f"  x={x}, z={z}  (среднее значение проигнорировано)")

    run_demo("Демо:", demo3)
    pause()


def topic_strings():
    clear()
    header("5. ФОРМАТИРОВАНИЕ СТРОК", "Четыре способа — какой выбрать?")

    section("Все четыре способа")
    show_code("""
name = "Боб"
age  = 30

# 1. % — старый C-стиль
"Привет %s, тебе %d лет" % (name, age)

# 2. str.format() — лучше, но многословно
"Привет {}, тебе {} лет".format(name, age)
"Привет {name}, тебе {age} лет".format(name=name, age=age)

# 3. f-строки — лучший вариант (Python 3.6+)
f"Привет {name}, тебе {age} лет"
f"Через 10 лет тебе будет {age + 10}"  # можно выражения!

# 4. Template — для пользовательских шаблонов
from string import Template
t = Template("Привет $name")
t.substitute(name=name)
""")

    def demo1():
        name, age = "Боб", 30

        r1 = "Привет %s, тебе %d лет" % (name, age)
        r2 = "Привет {}, тебе {} лет".format(name, age)
        r3 = f"Привет {name}, тебе {age} лет"
        r4 = f"Через 10 лет тебе будет {age + 10}"

        print(f"  % format  : {r1}")
        print(f"  .format() : {r2}")
        print(f"  f-string  : {r3}")
        print(f"  выражение : {r4}")

    run_demo("Все варианты:", demo1)

    pause()
    section("f-строки — суперсилы")
    show_code("""
price = 1234567.89
pi    = 3.14159265

# Форматирование чисел
f"{price:,.2f}"       # → '1,234,567.89'
f"{pi:.2f}"           # → '3.14'
f"{42:08b}"           # → '00101010' (двоичное, 8 знаков)

# Отладка (Python 3.8+)
x = 42
f"{x = }"             # → 'x = 42'

# Выравнивание
f"{'Лево':<10}|"      # → 'Лево      |'
f"{'Центр':^10}|"     # → '  Центр   |'
f"{'Право':>10}|"     # → '     Право|'
""")

    def demo2():
        price = 1234567.89
        pi = 3.14159265
        x = 42

        print(f"  Цена:       {price:,.2f}")
        print(f"  Пи:         {pi:.2f}")
        print(f"  42 в bin:   {42:08b}")
        print(f"  Отладка:    {x = }")
        print(f"  Влево:      |{'текст':<12}|")
        print(f"  По центру:  |{'текст':^12}|")
        print(f"  Вправо:     |{'текст':>12}|")

    run_demo("Мощь f-строк:", demo2)

    pause()
    section("⚠️  Когда НЕ использовать f-строки")
    show_code("""
# Если шаблон приходит от пользователя — используй Template
# f-строки выполняют код! Это опасно с внешними данными.

# Опасно:
template = input("Введи шаблон: ")  # пользователь вводит: {os.system('rm -rf /')}
result = f"{template}"              # ← выполнит системную команду!

# Безопасно:
from string import Template
t = Template(input("Введи шаблон: "))
result = t.safe_substitute(name="Боб")  # safe_substitute не бросает ошибку
""")
    pause()


# ─── Итог главы ──────────────────────────────────────────────────────────────

def topic_summary():
    clear()
    header("📚  ИТОГ ГЛАВЫ", "Паттерны чистого Python — Дэн Бейдер")

    print("""
  ┌─────────────────────────────────────────────────────┐
  │                                                     │
  │  1. ASSERT        Только для инвариантов.           │
  │                   Не для валидации ввода!           │
  │                                                     │
  │  2. ЗАПЯТЫЕ       Висящая запятая в конце —         │
  │                   норма и защита от багов.          │
  │                                                     │
  │  3. WITH          Открыл — используй — закрой.      │
  │                   Ресурсы всегда освобождаются.     │
  │                                                     │
  │  4. ПОДЧЁРКИВАНИЯ  _var  __var  __var__  _  var_   │
  │                   Каждый вид — своё значение.       │
  │                                                     │
  │  5. F-СТРОКИ      Используй везде (Python 3.6+).   │
  │                   Template — если ввод от юзера.    │
  │                                                     │
  └─────────────────────────────────────────────────────┘
""")

    print("  💡  Дзен Python (import this):\n")
    import this
    pause()


# ─── Главное меню ────────────────────────────────────────────────────────────

TOPICS = [
    ("Assert — утверждения",         topic_assertions),
    ("Висящие запятые",              topic_commas),
    ("Context Managers (with)",      topic_context_managers),
    ("Подчёркивания и дандеры",      topic_underscores),
    ("Форматирование строк",         topic_strings),
    ("📚  Итог главы",               topic_summary),
]

def main():
    while True:
        clear()
        header(
            "Python Tricks — Дэн Бейдер",
            "Глава 1: Паттерны чистого Python"
        )
        print("\n  Выбери тему:\n")
        for i, (name, _) in enumerate(TOPICS, 1):
            print(f"  [{i}] {name}")
        print("  [0] Выход\n")

        choice = input("  Выбор: ").strip()
        if choice == '0':
            print("\n  Пока! 👋\n")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(TOPICS):
            _, fn = TOPICS[int(choice) - 1]
            fn()
        else:
            print("  Введи номер из списка")
            time.sleep(1)


if __name__ == "__main__":
    main()
