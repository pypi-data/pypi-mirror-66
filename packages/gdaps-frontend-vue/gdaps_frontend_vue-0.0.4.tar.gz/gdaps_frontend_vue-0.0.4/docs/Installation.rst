Installation
============

For GDAPS install see https://gdaps.readthedocs.org.

Install **gdaps-frontend-vue** in your Python virtual environment:

.. code-block:: bash

    pip install gdaps-frontend-vue

This will automatically install the package, including necessary dependencies, like webpack_loader.

Next, ``webpack_loader`` must be added to ``INSTALLED_PLUGINS``:

.. code-block:: python

    # settings.py

    from gdaps.pluginmanager import PluginManager

    INSTALLED_APPS = [
        # ... standard Django apps and GDAPS
        # this must be placed *before* gdaps as it overrides gdaps' managemant commands:
        "gdaps.frontend"
        "gdaps",
        "webpack_loader",
    ]
    INSTALLED_APPS += PluginManager.find_plugins("myproject.plugins")

Now, to satisfy webpack-loader, add a section to settings.py:

.. code-block:: python

    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, "frontend", 'webpack-stats.json'),
        }
    }

This is because django(-webpack-loader) needs to find the info file webpack creates at
each compile, so that files can be recognized by django's reloading mechanism.

You should already have :ref:`added GDAPS' URL path <gdaps:url_support>`:

.. code-block:: python

    # urls.py
    from gdaps.pluginmanager import PluginManager

    urlpatterns = PluginManager.urlpatterns() + [
        # ... add your fixed URL patterns here, like "admin/", etc.
    ]

Now you can initialize the frontend with

.. code-block:: bash

    ./manage.py initfrontend

This creates a basic boilerplate (previously created with 'vue create' and calls *yarn install* to
install the needed javascript packages.
