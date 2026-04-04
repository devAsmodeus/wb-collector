import os, re

for root, dirs, files in os.walk('/app/src'):
    for f in files:
        if not f.endswith('.py'):
            continue
        path = os.path.join(root, f)
        with open(path) as fp:
            content = fp.read()
        if 'schemas.fbs.orders' in content:
            matches = re.findall(r'from src\.schemas\.fbs\.orders import[^\n]+', content)
            for m in matches:
                print(f'{path[5:]}: {m.strip()}')
