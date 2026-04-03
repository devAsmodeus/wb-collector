with open('/app/src/tasks/tasks.py') as f:
    lines = f.readlines()

in_products = False
for i, line in enumerate(lines):
    if 'sync.products.' in line and 'directories_subjects' in line:
        # Show 10 lines after last products task
        for j in range(i, min(i+15, len(lines))):
            print(f'{j+1}: {lines[j]}', end='')
        break
