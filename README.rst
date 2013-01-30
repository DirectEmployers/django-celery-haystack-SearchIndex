django-haystack celery powered SearchIndex - DirectEmployers Association Fork
=============================================================================

This is a simple queued SearchIndex implementation using celery to power the queue. This is not just a drop in Django app - but you can probably just copy the classes in and use them relatively quickly.

Some notes
----------

1. In general we don't put instances on the queue - only references to them - otherwise queues grow or instances have changed by the time they are taken off the queue.

Dependencies
------------

Not sure why you'd be looking at this if you didn't already use these...but here you go:

 * django-haystack (https://github.com/toastdriven/django-haystack, http://haystacksearch.org/)
 * celery (https://github.com/ask/celery)
 *


Copyright and License
---------------------
All DirectEmployers additions are copyright (C) 2012-2013, DirectEmployers Foundation and are provided .  This project is provided under
a triple license that allows you to select the license that is best for your needs. You may choose from:

- The GNU GPL v2.0
- The GNU GPL v3.0
- The MIT License

You can read the licenses in the licenses directory.

THe license for non-modified Django-haystack code is unchanged from the original.

More information
----------------
Information about DirectEmployers Foundation can be found at http://directemployersfoundation.org
