with open('/app/src/collectors/fbw/supplies.py') as f:
    content = f.read()

old = 'return FBWPackageQR.model_validate(data if isinstance(data, dict) else {"file": data})'
new = 'return FBWPackageQR.model_validate(data if isinstance(data, (dict, list)) else {"file": data})'

if old in content:
    content = content.replace(old, new)
    with open('/app/src/collectors/fbw/supplies.py', 'w') as f:
        f.write(content)
    print("Fixed collector")
else:
    print("Not found, checking...")
    for i, line in enumerate(content.split('\n')):
        if 'FBWPackageQR' in line:
            print(f"Line {i}: {repr(line)}")
