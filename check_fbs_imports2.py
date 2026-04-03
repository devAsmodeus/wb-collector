import re

files = [
    '/app/src/collectors/fbs/orders.py',
    '/app/src/api/fbs/wb/meta.py',
    '/app/src/api/fbs/wb/orders.py',
    '/app/src/services/fbs/wb/orders.py',
    '/app/src/schemas/fbs/__init__.py',
]

needed = set()
for f in files:
    with open(f) as fp:
        content = fp.read()
    m = re.search(r'from src\.schemas\.fbs\.orders import \((.*?)\)', content, re.DOTALL)
    if m:
        names = [n.strip() for n in m.group(1).split(',') if n.strip()]
        for n in names:
            needed.add(n)
        print(f'{f.split("/")[-1]}: {names}')
    else:
        m2 = re.search(r'from src\.schemas\.fbs\.orders import (.+)', content)
        if m2:
            names = [n.strip() for n in m2.group(1).split(',')]
            for n in names:
                needed.add(n)
            print(f'{f.split("/")[-1]}: {names}')

print('\nAll needed:', sorted(needed))
