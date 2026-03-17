import yaml, glob

files = sorted(glob.glob('C:/Python/wb-collector/docs/api/*.yaml'))
for fpath in files[9:]:  # 10-13
    with open(fpath, encoding='utf-8') as f:
        doc = yaml.safe_load(f)
    counts = {}
    for path, methods in doc.get('paths', {}).items():
        for method, info in methods.items():
            if isinstance(info, dict):
                t = info.get('tags', ['?'])[0]
                counts[t] = counts.get(t, 0) + 1
    total = sum(counts.values())
    name = fpath.split('/')[-1]
    print(f'\n=== {name} ({total} ep) ===')
    for t, c in sorted(counts.items()):
        print(f'  {t}: {c}')
