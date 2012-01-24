from django.db.models import signals
from celery_haystack_index.signals import solr_bulk_change

from haystack import indexes
from haystack.utils import get_identifier

from celery_haystack_index.index_tasks import search_index_update,
search_index_delete, search_index_bulk_update, search_index_bulk_delete


class QueuedSearchIndex(indexes.SearchIndex):
    """A ``SearchIndex`` subclass that enqueues updates for later processing."""
    # We override the built-in _setup_* methods to connect the enqueuing operation.

    def assemble_dispatch_uid(self, method):
        return '.'.join([self.__module__, self.__class__.__name__,
                        method.__func__.__name__])

    def _setup_save(self):
        signals.post_save.connect(
            self.enqueue_save, 
            sender=self.get_model(),
            dispatch_uid=self.assemble_dispatch_uid(self._setup_save))

    def _setup_delete(self):
        signals.post_delete.connect(
            self.enqueue_delete, 
            sender=self.get_model(),
            dispatch_uid=self.assemble_dispatch_uid(self._setup_delete))

    def _teardown_save(self):
        signals.post_save.disconnect(self.enqueue_save, sender=self.get_model())

    def _teardown_delete(self):
        signals.post_delete.disconnect(self.enqueue_delete, 
                                       sender=self.get_model())

    def enqueue_save(self, instance, **kwargs):
        search_index_update.delay(instance) 

    def enqueue_delete(self, instance, **kwargs):
        search_index_delete.delay(instance)

class BulkQueuedSearchIndex(indexes.SearchIndex):
    """A ``SearchIndex`` subclass that enqueues updates for later processing."""
    # We override the built-in _setup_* methods to connect the enqueuing
    # operation.

    def assemble_dispatch_uid(self, method):
        return '.'.join([self.__module__, self.__class__.__name__,
                        method.__func__.__name__])

    def _setup_save(self):
        solr_bulk_change.connect(
            self.enqueue_bulk_change, 
            dispatch_uid=self.assemble_dispatch_uid(self._setup_save))

    def _teardown_save(self):
        solr_bulk_change.disconnect(self.enqueue_bulk_change)

    def enqueue_bulk_change(self, update_items=None, delete_query=None, **kwargs):
        if update_items:
            search_index_bulk_update.delay(update_items)
        if delete_query:
            search_index_bulk_delete.delay(delete_query)

