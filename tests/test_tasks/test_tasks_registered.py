"""Test that all Celery tasks are properly registered."""
import pytest


def test_all_tasks_importable():
    """All task functions should be importable."""
    from src.tasks.tasks import (
        sync_general_seller_full,
        sync_general_news_full,
        sync_general_news_incremental,
        sync_products_cards_full,
        sync_products_prices_full,
        sync_products_tags_full,
        sync_products_warehouses_full,
        sync_products_directories_categories,
        sync_products_directories_subjects,
        sync_fbs_orders_full,
        sync_dbw_orders_full,
        sync_dbs_orders_full,
        sync_pickup_orders_full,
        sync_promotion_campaigns_full,
        sync_promotion_stats_full,
        sync_promotion_calendar_full,
        sync_communications_feedbacks_full,
        sync_communications_questions_full,
        sync_communications_claims_full,
        sync_tariffs_commissions,
        sync_tariffs_box,
        sync_tariffs_pallet,
        sync_tariffs_supply,
        sync_reports_stocks,
        sync_reports_orders,
        sync_reports_sales,
        sync_finances_full,
    )
    assert sync_general_seller_full is not None


def test_tasks_have_retry_config():
    """All tasks should have autoretry_for configured."""
    from src.tasks import tasks
    import inspect

    task_funcs = [
        obj for name, obj in inspect.getmembers(tasks)
        if hasattr(obj, 'name') and hasattr(obj, 'max_retries')
    ]

    for task in task_funcs:
        assert task.max_retries == 3, f"Task {task.name} should have max_retries=3, got {task.max_retries}"


def test_beat_schedule_count():
    """Beat schedule should have 25 entries (one per sync endpoint)."""
    from src.tasks.celery_app import celery_app
    schedule = celery_app.conf.beat_schedule
    assert len(schedule) == 25, f"Expected 25 scheduled tasks, got {len(schedule)}"
