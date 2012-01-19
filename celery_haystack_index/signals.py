from django.dispatch import Signal

solr_bulk_update = Signal(providing_args=[update_items])

solr_bulk_delete = Signal(providing_args=[delete_query])

solr_bulk_change = Signal(providing_args=[update_items, delete_query])
