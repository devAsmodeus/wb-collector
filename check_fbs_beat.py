import sys; sys.path.insert(0, '/app')
from src.tasks.celery_app import celery_app
beat = celery_app.conf.beat_schedule
for k, v in sorted(beat.items()):
    if 'fbs' in k.lower():
        print(f"{k}: {v['task']} @ {v['schedule']}")
