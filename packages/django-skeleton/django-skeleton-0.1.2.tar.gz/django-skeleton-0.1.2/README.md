# django-skeleton


A template repository of Django admin features and style enhancements. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "skeleton" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'skeleton',
    ]

2. Include the skeleton URLconf in your project urls.py like this::

    path('admin/', include('skeleton.urls')),

3. Run ``python manage.py migrate`` to create the skeleton models.

4. Start the development server and visit `http://127.0.0.1:8000/admin/`.