MgClipboard
============

Clipboard middleware for Papermerge DMS [Papermerge DMS](https://github.com/ciur/papermerge).
Designed as Django reusable app.

## Installation

Install it using pip::
    
    pip install mgclipboard

Add app to INSTALLED_APPS in settings.py::

    INSTALLED_APP = (
    ...
    'mgclipboard',
    ...
    )

Add it to MIDDLEWARE list::

    MIDDLEWARE = [
        ...
        # AFTER
        # * django.contrib.sessions.middleware
        # * django.contrib.auth.middleware
        'mgclipboard.middleware.ClipboardMiddleware'
        ...
    ]

mgclipboard.middleware is dependent on django.contrib.sessions and django.contrib.auth middleware. Thus, dependencies must be included first in MIDDLEWARE list.


