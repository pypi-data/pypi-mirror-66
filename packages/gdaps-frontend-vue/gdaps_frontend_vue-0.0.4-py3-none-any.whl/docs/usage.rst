.. usage:

Usage
=====

Initializing the frontend
-------------------------

.. code-block:: bash

    ./manage.py initfrontend

This creates a /frontend/ directory in the project root, and installs a Vue.js frontend application there. The type of frontend depends on what you have selected in `GDAPS["FRONTEND_ENGINE"]`: Vue, PySide are available ATM.

Vue.js
    It is recommended to install vue globally, you can do that with
    ``yarn global add @vue/cli @vue/cli-service-global``.
    GDAPS tries to do that for you when you call ``./manage.py initfrontend``.

Now you can start ``yarn serve`` (or ``npm run serve``, depending on your choice)
in the frontend directory. This starts
a development web server that bundles the frontend app using webpack
automatically. You then need to start Django using
``./manage.py runserver`` as usual to enable the Django backend. GDAPS manages
all the needed background tasks to transparently enable hot-reloading
when you change anything in the frontend source code now.

Frontend plugins
----------------

Django itself provides a template engine, so you could
use templates in your GDAPS apps to build the frontend parts too. But templates are not always the desired way to go. Since a few years, Javascript SPAs (Single Page Applications) have come up and promise fast, responsive software.

But: a SPA mostly is written as monolithic block. All tutorials that describe Django as backend recommend building the Django server modular, but it should serve only as API, namely REST or GraphQL.
This API then should be consumed by a monolithic Javascript frontend, built by webpack etc.
At least I didn't find anything else on the internet. So I created my own solution:

GDAPS is a plugin system. It provides backend plugins (Django apps). But using ``gdaps.frontend``, each
GDAPS app can use a *frontend* directory which contains an installable module, that is automatically installed when the app is added to the system.

When the ``gdaps.frontend`` app is activated in
``INSTALLED_APPS``, the ``startplugin`` management command is extended by a frontend part: When a new plugin is created, a *frontend/myproject-plugin-fooplugin* directory wth some boilerplate files in that plugin is
created. The ``index.js`` file is the plugin entry point for the frontend.

So all you have to do is:

#. Add ``gdaps.frontend`` to ``INSTALLED_APPS`` (before ``gdaps``)
#. Call ``./manage.py initfrontend``, if you haven't already
#. Call ``./manage.py startplugin fooplugin``
#. start ``yarn serve`` in the *frontend* directory
#. start Django server using ``./manage.py runserver``

To remove a plugin from the frontend, just remove the backend part (remove it from INSTALLED_APPS or uninstall it using pip) and call ``manage.py syncplugins`` afterwords. It will take care of the database models, and the npm/yarn uninstallation of the frontend part.

Creating plugins
----------------

When ``gdaps-frontend-vue`` is installed, you can create plugins using a Django management command as usual:

.. code-block::bash

    ./manage.py startplugin fooplugin

This command asks a few questions, creates a basic Django app in the plugin path chosen in ``PluginManager.find_plugins()``. It provides useful defaults as well as a setup.py/setup.cfg file.
Additionally, it creates a frontend directory which then can be consumed by your frontend.
