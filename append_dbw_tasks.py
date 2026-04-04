new_task = """

# ---------------------------------------------------------------------------
# (04) DBW — Incremental (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.dbw.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_dbw_orders_incremental(self):
    from src.services.dbw.sync.orders import DbwOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await DbwOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.dbw.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())
"""

with open("/app/src/tasks/tasks.py", "a") as f:
    f.write(new_task)
print("Done")
