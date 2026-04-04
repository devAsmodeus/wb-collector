with open('/app/src/api/fbw/wb/supplies.py') as f:
    content = f.read()

# Fix Parameter(False, ...) -> Parameter(default=False, ...)
import re
fixed = re.sub(
    r'Parameter\(False,\s*query=',
    'Parameter(default=False, query=',
    content
)
fixed = re.sub(
    r'Parameter\(1000,\s*query=',
    'Parameter(default=1000, query=',
    fixed
)
fixed = re.sub(
    r'Parameter\(0,\s*query=',
    'Parameter(default=0, query=',
    fixed
)

with open('/app/src/api/fbw/wb/supplies.py', 'w') as f:
    f.write(fixed)

# Count fixes
n = content.count('Parameter(False,') + content.count('Parameter(1000,') + content.count('Parameter(0,')
print(f"Fixed {n} Parameter() calls")

# Check package 500
with open('/app/src/api/fbw/wb/supplies.py') as f: c = f.read()
idx = c.find('package')
print("\nPackage handler:")
print(c[idx:idx+300])
