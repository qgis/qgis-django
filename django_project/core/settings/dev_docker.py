# -*- coding: utf-8 -*-
from .dev import *  # noqa

DATABASES = {
    'default': {
        # Newer django versions may require you to use the postgis backed
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'qgis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
    }
}
