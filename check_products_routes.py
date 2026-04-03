import os, re

for root, dirs, files in os.walk('/app/src/api/products'):
    for f in sorted(files):
        if not f.endswith('.py') or f == '__init__.py':
            continue
        path = os.path.join(root, f)
        layer = root.split('/')[-1]
        with open(path) as fp:
            lines = fp.readlines()
        
        controller_path = ''
        for line in lines:
            m = re.search(r'path\s*=\s*["\']([^"\']*)["\']', line)
            if m:
                controller_path = m.group(1)
                break
        
        for i, line in enumerate(lines):
            if any(d in line for d in ['@get(', '@post(', '@put(', '@delete(', '@patch(']):
                method = re.search(r'@(\w+)\(', line)
                method = method.group(1).upper() if method else '?'
                route = ''
                for j in range(i, min(i+3, len(lines))):
                    m2 = re.search(r'''["'](\/[^"']*)["']''', lines[j])
                    if m2:
                        route = m2.group(1)
                        break
                full = controller_path + route if route != controller_path else controller_path
                print(f'[{layer}/{f}] {method} {full}')
