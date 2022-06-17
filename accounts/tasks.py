from celery import shared_task


@shared_task(name='sync_db')
def sync_db():
    pass
