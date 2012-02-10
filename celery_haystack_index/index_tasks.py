from django.db.models.loading import get_model

from haystack import connections
from haystack.management.commands import update_index
from haystack.utils import get_identifier

from celery.task import Task, PeriodicTask
from celery.task import task
from celery.schedules import crontab

@task(default_retry_delay=5*60, max_retries=1)
def search_index_update(instance, **kwargs):
    logger = search_index_update.get_logger(**kwargs)
    try:
        search_index = (connections['default'].get_unified_index()\
                                              .get_index(instance.__class__))
        search_index.update_object(instance)
    except Exception, exc:
        logger.error(exc)
        search_index_update.retry(exc=exc)

@task(default_retry_delay=5*60, max_retries=1)
def search_index_delete(instance, **kwargs):
    logger = search_index_delete.get_logger(**kwargs)
    try:
        search_index = (connections['default'].get_unified_index()\
                                              .get_index(instance.__class__))
        search_index.remove_object(get_identifier(instance))
    except Exception, exc:
        logger.error(exc)
        search_index_delete.retry(exc=exc)

@task(default_retry_delay=5*60, max_retries=1)
def search_index_bulk_update(update_items, indexed_class, **kwargs):
    logger = search_index_bulk_update.get_logger(**kwargs)
    try:
        search_index = (connections['default'].get_unified_index()\
                                              .get_index(indexed_class))
        search_index.update_objects(update_items)
    except Exception, exc:
        logger.error(exc)
        search_index_bulk_update.retry(exc=exc)

@task(default_retry_delay=5*60, max_retries=1)
def search_index_bulk_delete(delete_query, indexed_class, **kwargs):
    logger = search_index_bulk_delete.get_logger(**kwargs)
    try:
        search_index = (connections['default'].get_unified_index()\
                                              .get_index(indexed_class))
        search_index.remove_objects(delete_query)
    except Exception, exc:
        logger.error(exc)
        search_index_bulk_delete.retry(exc=exc)

class SearchIndexUpdatePeriodicTask(PeriodicTask):
    routing_key = 'periodic.search.update_index'
    run_every = crontab(hour=4, minute=0)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting update index")
        # Run the update_index management command
        update_index.Command().handle()
        logger.info("Finishing update index")

