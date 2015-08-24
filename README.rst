.. _Recalbox: http://recalbox.com
.. _recalbox-webconfig: https://github.com/MikaXII/recalbox-webconfig
.. _Django: https://www.djangoproject.com
.. _Foundation: http://foundation.zurb.com
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs

Recalbox manager Web interface
==============================

Like `recalbox-webconfig`_ this project aims to serve a web interface to manage some common `Recalbox`_ configurations but with `Django`_ instead of *Node.js*.

This is a full Django webapp project, meaning it's ready to launch when correctly installed.

Features
********

* Try to be the lightweight as possible;
* Web integration on top of `Foundation`_;
* Read the Recalbox logs;
* Edit the Recalbox configuration file;
* Manage (upload, delete) your roms by systems;
* Manage your bios files;
* Hardly repose on Recalbox Manifest file to valid uploads;

Install
*******

Common Linux system
-------------------

Nothing special, it's just about to have PIP and virtualenv installed on your system, then use the Makefile action: ::

    make install

And voila, it's done.

Recalbox system
---------------

This is different because Recalbox don't have all the common libraries and tools installed as on Linux system.

Before doing anything, ensure the rpi can access to the internet else configure your network interface and if needed dns resolving.

Get the project repository, enter in its directory then type the following commands: ::

    python -m ensurepip
    pip install virtualenv
    virtualenv --no-site-packages .
    bin/pip install -r requirements.txt

The first two lines would be needed only the first time.

Finally, because Git is not available on Recalbox, you should get the repository on your PC before, transfer it to your recalbox and then continue on it with the commands.

Usage
*****

::

    source bin/activate
    python manage.py runserver 0.0.0.0:8001
    
Development notes
*****************

#. You can install the project on common Linux system for development but you will need to reproduce the Recalbox file structure for Roms, Bios, Configuration file, log file, etc..

#. CSS are compiled from Compass sources, you will need to install the right Compass (use the shipped ``Gemfile`` file) and Foundation 5 (use the dedicated Makefile action) versions;

#. Python 2.7.9 is installed on Recalbox 3.2.11, so *pip* is near to be ready to use;

#. UTC Timezone does not seems available, have to set settings.TIME_ZONE to None and set settings.USE_TZ to False and so it start with a dummy project freshly created from startproject Django command;

#. Python devel lib is not installed but will be may be needed to install some packages from eggs (actually not needed);

PIP
---

Python 2.7.9 is installed on Recalbox 3.2.11, so *pip* is near to be ready to use, just have to install it the first time.

    
This will results to install ``pip==1.5.6``.
