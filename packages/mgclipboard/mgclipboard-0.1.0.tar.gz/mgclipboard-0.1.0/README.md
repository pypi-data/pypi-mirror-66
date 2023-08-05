MgClipboard
============

Clipboard middleware for Papermerge DMS [Papermerge DMS](https://github.com/ciur/papermerge).
Designed as Django reusable app.

## Usage

Install it::
    
    pip install mgclipboard

Add app to INSTALLED_APPS in settings.py::

    INSTALLED_APP = (
    ...
    'papermerge.clipboard',
    ...
    )

Add it to MIDDLEWARE list::

    MIDDLEWARE = [
        ...
        # papermerge.middleware.clipboard must be AFTER
        # * django.contrib.sessions.middleware
        # * django.contrib.auth.middleware
        'papermerge.middleware.clipboard.ClipboardMiddleware'
        ...
    ]


