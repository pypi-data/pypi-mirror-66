Gdaps-Frontend-Vue Plugin
================================

When the ``gdaps.frontend`` app is activated in
``INSTALLED_APPS``, the ``startplugin`` management command must be extended by a frontend part like `gdaps-frontend-vue`: When a new plugin is created, it creates a *frontend/myproject-plugin-fooplugin* directory wth some boilerplate files in that plugin.

Install
-------
As prerequisite, it is recommended to install vue globally, you can do that with
``yarn global add @vue/cli @vue/cli-service-global`` (GDAPS tries to do that during the `initfrontend` call).

Now execute

```bash

./manage.py initfrontend

```


This will install a full Vue.js frontend (using Vue CLI). You can start ``yarn serve`` (or ``npm run serve``, depending on your choice) in the frontend directory afterwords. You then need to start Django using
``./manage.py runserver`` as usual to enable the Django backend. GDAPS manages
all the needed background tasks to transparently enable hot-reloading
when you change anything in the frontend source code now.
