from django.db.models import signals

from haystack import indexes
from haystack.utils import get_identifier

from index_tasks import search_index_update, search_index_delete


class QueuedSearchIndex(indexes.SearchIndex):
    """A ``SearchIndex`` subclass that enqueues updates for later processing."""
    # We override the built-in _setup_* methods to connect the enqueuing operation.

    def assemble_dispatch_uid(self, method):
        return '.'.join([self.__module__, self.__class__.__name__,
                        method.__func__.__name__])

    def _setup_save(self):
        signals.post_save.connect(
            self.enqueue_save, sender=self.get_model(),
            dispatch_uid=self.assemble_dispatch_uid(self._setup_save))

    def _setup_delete(self):
        signals.post_delete.connect(
            self.enqueue_delete, sender=self.get_model(),
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
