import sys; sys.path.insert(0, '/app')
from src.tasks.celery_app import celery_app

beat = celery_app.conf.beat_schedule
keywords = ['product', 'card', 'price', 'tag', 'warehouse', 'director', 'categor', 'subject']

print("=== Products tasks in Beat ===")
found = False
for k, v in beat.items():
    if any(kw in k.lower() for kw in keywords):
        print(f"  {k}: {v['task']} @ {v['schedule']}")
        found = True
if not found:
    print("  [NONE FOUND]")

print("\n=== All beat tasks ===")
for k, v in sorted(beat.items()):
    print(f"  {k}: {v['task']}")
