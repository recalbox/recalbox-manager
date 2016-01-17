.. _Recalbox: http://recalbox.com
.. _recalbox-webconfig: https://github.com/MikaXII/recalbox-webconfig
.. _Django: https://www.djangoproject.com
.. _Foundation: http://foundation.zurb.com
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _virtualenv: http://www.virtualenv.org/
.. _psutil: https://pypi.python.org/pypi/psutil
.. _Dropzone.js: http://www.dropzonejs.com/

Recalbox manager Web interface
==============================

Like `recalbox-webconfig`_ this project aims to serve a web interface to manage some common `Recalbox`_ configurations but with `Django`_ instead of *Node.js*.

This is a full Django webapp project, meaning it's ready to launch when correctly installed.

Features
********

* Try to be the lightweight as possible (even if using Django):
    
  * Actually don't have any app models, so we never perform database request for anything;
  * Don't use Django site framework (to avoid database request);
  * Don't use compressor "on the fly" (like *django-assets* or *django-pipeline*) to avoid processing many files just to display static files tags. Instead ships allready compressed assets and switch to them in production environment;

* Hardly repose on Recalbox Manifest file to validate uploads;
* Web integration on top of `Foundation`_;
* Display system informations like CPU, Memory and disks usage;
* Read the Recalbox logs;
* Edit the Recalbox configuration file;
    
  * Option to backup the file before updating it;

* Manage (upload, delete) your roms by systems;
  
  * Only accept supported extensions for systems (from manifest);
  
* Manage (upload, delete) your bios files;

  * Only accept supported Bios file (from manifest);
  * MD5 checksum validation;

* Usage of `Dropzone.js`_ plugin for multiple-upload forms;
  

Install
*******

Common Linux system (development)
---------------------------------

Nothing special, it's just about to have PIP and `virtualenv`_ installed on your system, enter into your recalbox-manager directory, then use the Makefile action: ::

    make install

And voila, it's done.

But note this procedure is mostly for development purpose. See next section.

Recalbox system (production)
----------------------------

Recalbox system is assumed to be the production environment.

This is different because Recalbox don't have all libraries and tools common to Linux systems.

Before doing anything, ensure the Raspberry can access to the internet else configure your network interface and if needed dns resolving.

Go where you want to install the manager directory then type the following commands: ::

    wget -q -O - https://raw.githubusercontent.com/sveetch/recalbox-manager/master/deployment/install.sh | bash /dev/stdin --release=1.1.4.1

This will download an install script and automatically execute it to proceed to install. **This procedure is only for Recalbox systems that don't have the manager installed yet**, since Recalbox 3.3.0 beta15, the manager is allready installed at ``/usr/recalbox-manager``.

Actually the install script accept an additional argument to enable compatibility with Recalbox 3.2.11 (because it's actually the real last stable version). So to install recalbox-manager on Recalbox 3.2.11, add ``--compatible`` to the previous command.


Usage
*****

Basically, go into the recalbox-manager directory then use the following commands: ::

    bin/python manage.py runserver 0.0.0.0:8001

The runserver is not launched as a daemon or a background process, as soon as you stop the instance thread (using CTRL-C) the webserver is stopped.

**For production** you must use the right settings: ::

    bin/python manage.py runserver 0.0.0.0:80 --settings=project.settings_production --noreload

**For development**, you should active the environment and you may want to use the right settings with additional stuff: ::

    . bin/activate
    python manage.py runserver 0.0.0.0:8001 --settings=project.settings_development
    
Notes for development
*********************

#. Before doing anything (install or whatever), development requires additional tools : *Ruby*, *Node.js* and *npm*. Install them on your system;

#. To directly install the full development environment, just use ``make install-dev`` from the project root, it will install everything (use ``make clean`` before if you previously used the ``make install`` command) but the Compass stuff.

#. The ``pip-requirements/development.txt`` contains some additional packages;

#. You can install the project on common Linux system for development but you will need to reproduce the Recalbox file structure for Roms, Bios, Configuration file, log file, etc.. Or you can edit needed paths in project settings;

#. CSS are compiled from Compass sources, you will need to install the right Compass (use the shipped ``Gemfile`` file) and Foundation 5 (use the dedicated Makefile action) versions;

#. Python 2.7.9 is installed on Recalbox 3.2.11, so *pip* is near to be ready to use, just have to install it the first time. This will results to install ``pip==1.5.6``.

Assets
------

You need to install the required Grunt stuff to develop on assets, it should have been done with ``make install-dev``

Assets are managed in a JSON manifest ``project/assets.json`` that are used by Django template tags to know what asset to load in the pages. And the manifest is used also by Grunt tasks to optimize and build the asset files for production environment. 

In default and development environment loaded assets are not uglified or compressed to ease asset debugging.

When you did some changes (add, delete, change) on Javascript files, you will need to execute the following Grunt task: ::

    grunt uglify

And when you did some changes on CSS files (or when Compass rebuild CSS from your SCSS changes), you will need to execute the following Grunt task: ::

    grunt cssmin

Also to make continue development, you can use the watch task so every time Compass is making a recompile, cssmin will compress CSS: ::

    grunt watch

**Remember to execute theses tasks before commiting updates on assets.**

Notes for production
********************

Last tests on Recalbox 3.3.0 beta 6 and ``recalbox-manager==0.8.2`` was giving 2% CPU charge when Django instance is idle and can go to 17% when furiously reloading a page during 30seconds. Memory is allways stable around 80Mo and should probably don't go further. This was a naive benchmark just using ``top``.

Caveats
*******

* Python devel lib is not installed on Recalbox, this would prevent you to be able to install somes additional Python packages that require to compile some C code;

* Currently, webapp is served using the development server from Django. It's awful but at least the webapp should not have to response to many connections. This choice has been done to avoid loading a real web server on the Raspberry additionaly to the Django instance;

* UTC Timezone does not seems available for now, so have to set ``settings.TIME_ZONE`` to ``None`` and set ``settings.USE_TZ`` to ``False``;
