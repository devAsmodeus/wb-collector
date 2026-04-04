new_task = """

# ---------------------------------------------------------------------------
# (06) Pickup — Incremental (added by audit)
# ---------------------------------------------------------------------------

@celery_app.task(
    name="sync.pickup.orders_incremental",
    bind=True,
    autoretry_for=(Exception,),
    default_retry_delay=60,
    retry_kwargs={"max_retries": 3},
)
def sync_pickup_orders_incremental(self):
    from src.services.pickup.sync.orders import PickupOrdersSyncService
    async def _run():
        async with DBManager() as db:
            result = await PickupOrdersSyncService().sync_incremental(db.session)
        logger.info("[sync.pickup.orders_incremental] Synced: %d orders", result.get("synced", 0))
        return result
    return run_async(_run())
"""

with open("/app/src/tasks/tasks.py", "a") as f:
    f.write(new_task)
print("Done")
