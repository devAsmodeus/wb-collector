with open('/app/src/tasks/tasks.py') as f:
    content = f.read()
for line in content.split('\n'):
    if 'sync.products' in line:
        print(line.strip())
