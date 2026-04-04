with open('/app/src/tasks/tasks.py') as f:
    content = f.read()
for line in content.split('\n'):
    if 'fbs' in line.lower() or 'passes' in line.lower() or 'supplies' in line.lower():
        print(line.strip())
