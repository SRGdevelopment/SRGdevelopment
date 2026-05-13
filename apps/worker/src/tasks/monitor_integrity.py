from celery import shared_task


@shared_task(name="monitor_integrity")
def monitor_integrity() -> str:
    # Placeholder task for periodic fairness/compliance checks.
    return "integrity monitor executed"
