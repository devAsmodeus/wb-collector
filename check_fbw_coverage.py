import yaml

with open('/app/docs/api/07-orders-fbw.yaml') as f:
    spec = yaml.safe_load(f)

print("=== YAML: все эндпоинты ===")
for path, methods in spec.get('paths', {}).items():
    for method in ['get', 'post', 'put', 'patch', 'delete']:
        if method in methods:
            summary = methods[method].get('summary', '')
            print(f"  {method.upper():6} {path}  # {summary}")

import os

print("\n=== API роуты (реализованы) ===")
for root, dirs, files in os.walk('/app/src/api/fbw'):
    for f in sorted(files):
        if f.endswith('.py') and f != '__init__.py':
            path = os.path.join(root, f)
            with open(path) as fp:
                lines = fp.readlines()
            section = root.split('/')[-1]
            for i, line in enumerate(lines):
                for verb in ['@get(', '@post(', '@put(', '@patch(', '@delete(']:
                    if verb in line:
                        route = line.strip()
                        # find path string
                        import re
                        m = re.search(r'["\']([^"\']+)["\']', route)
                        rpath = m.group(1) if m else '?'
                        # find method name on next lines
                        for j in range(i+1, min(i+5, len(lines))):
                            if 'async def ' in lines[j]:
                                mname = lines[j].strip().split('(')[0].replace('async def ', '')
                                break
                        else:
                            mname = '?'
                        print(f"  {verb[1:-1].upper():6} /fbw/{section}{rpath}  -> {mname}")

print("\n=== Sync сервисы ===")
for root, dirs, files in os.walk('/app/src/services/fbw/sync'):
    for f in sorted(files):
        if f.endswith('.py') and f != '__init__.py':
            path = os.path.join(root, f)
            with open(path) as fp:
                methods = [l.strip() for l in fp if 'async def ' in l and not l.strip().startswith('#')]
            names = [m.split('(')[0].replace('async def ', '') for m in methods]
            print(f"  {f}: {names}")

print("\n=== DB статистика ===")
# Check row counts via model
