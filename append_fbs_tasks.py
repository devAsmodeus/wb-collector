new_tasks = """

# ---------------------------------------------------------------------------
# (03) FBS — Incremental + Passes + Supplies (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.fbs.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_orders_incremental(self):
    from src.services.fbs.sync.orders import FbsOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.fbs.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())


@celery_app.task(
    name="sync.fbs.passes_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_passes_full(self):
    from src.services.fbs.sync.passes import FbsPassesSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsPassesSyncService().sync_passes(db.session)
        logger.info("[sync.fbs.passes_full] Synced: %d passes", result.get("synced", 0))
        return result
    return run_async(_run())


@celery_app.task(
    name="sync.fbs.supplies_full",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_fbs_supplies_full(self):
    from src.services.fbs.sync.supplies import FbsSuppliesSyncService
    async def _run():
        async with DBManager() as db:
            result = await FbsSuppliesSyncService().sync_supplies(db.session)
        logger.info("[sync.fbs.supplies_full] Synced: %d supplies", result.get("synced", 0))
        return result
    return run_async(_run())
"""

with open("/app/src/tasks/tasks.py", "a") as f:
    f.write(new_tasks)
print("Done")
