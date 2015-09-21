.. _Recalbox: http://recalbox.com
.. _recalbox-webconfig: https://github.com/MikaXII/recalbox-webconfig
.. _Django: https://www.djangoproject.com
.. _Foundation: http://foundation.zurb.com
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs
.. _virtualenv: http://www.virtualenv.org/
.. _psutil: https://pypi.python.org/pypi/psutil

Recalbox manager Web interface
==============================

Like `recalbox-webconfig`_ this project aims to serve a web interface to manage some common `Recalbox`_ configurations but with `Django`_ instead of *Node.js*.

This is a full Django webapp project, meaning it's ready to launch when correctly installed.

Features
********

* Try to be the lightweight as possible (..but using Django..);
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
  

Install
*******

Common Linux system
-------------------

Nothing special, it's just about to have PIP and `virtualenv`_ installed on your system, enter into your recalbox-manager directory, then use the Makefile action: ::

    make install

And voila, it's done.

But note this procedure is mostly for development purpose. See next section.

Recalbox system
---------------

Recalbox system is assumed to be the production environment.

This is different because Recalbox don't have all the common libraries and tools installed on a common Linux system.

Before doing anything, ensure the Raspberry can access to the internet else configure your network interface and if needed dns resolving.

Get the project repository, enter in its directory then type the following commands: ::

    python -m ensurepip
    pip install virtualenv
    wget https://github.com/sveetch/recalbox-manager/archive/0.8.3.zip
    unzip 0.8.3.zip
    cd recalbox-manager-0.8.3/
    virtualenv --system-site-packages .
    bin/pip install -r requirements.txt
    bin/python manage.py migrate
    bin/python manage.py runserver 0.0.0.0:8001

The first two lines would be needed only the first time. The last line init a dummy database (into file ``db.sqlite3``) that is not really used for now.

Finally, because Git is not available on Recalbox, you should get the repository on your PC before, transfer it to your recalbox and then continue on it with the commands.

Some explanations, line by line:

#. Install Pip;
#. Install virtualenv;
#. Directly download last stable release;
#. Decompress downloaded archive;
#. Enter recalbox-manager directory;
#. Initialize the virtual environment, it will inherits from the Python system packages to be able to use installed `psutil`_ if any;
#. Install dependancies using PIP;
#. Initialize a dummy database (into file ``db.sqlite3``) that is not really used, but required;
#. Run the server on all IP interface with port 8001 and default settings (``settings.py``);

Usage
*****

::

    . bin/activate
    python manage.py runserver 0.0.0.0:8001

You should also use the option ``--noreload`` at the last command end if you don't plan to develop on this project.
    
Notes for development
*********************

#. Use the ``requirements.development.txt`` instead of ``requirements.txt``, it contains additional packages needed for development;

#. Launch the webserver using the settings file for development: ::

       python manage.py runserver 0.0.0.0:8001 --settings=project.settings_development

#. You can install the project on common Linux system for development but you will need to reproduce the Recalbox file structure for Roms, Bios, Configuration file, log file, etc.. Or you can edit needed paths in project settings;

#. CSS are compiled from Compass sources, you will need to install the right Compass (use the shipped ``Gemfile`` file) and Foundation 5 (use the dedicated Makefile action) versions;

#. Python 2.7.9 is installed on Recalbox 3.2.11, so *pip* is near to be ready to use, just have to install it the first time. This will results to install ``pip==1.5.6``.

#. Python devel lib is not installed but will be may be needed to install some packages from eggs (actually not needed);

#. UTC Timezone does not seems available, have to set settings.TIME_ZONE to None and set settings.USE_TZ to False and so it start with a dummy project freshly created from startproject Django command;

Notes for production
********************

#. Launch the webserver using the settings file for production: ::

       bin/python manage.py runserver 0.0.0.0:80 --settings=project.settings_production

#. The server can take some times to fully initialize (something like 10s) the first time;

#. Currently the webapp is served using the development server from Django. It is strongly advised to not use it in production, but this should be fine as the webapp should not have to response to many connections because it's not a website on internet. This choice has been done to avoid to load a real web server on the Raspberry;

#. Last tests on Recalbox 3.3.0 beta 6 and recalbox-manager==0.8.2 was giving 2% CPU charge when Django instance is idle and can go to 17% when furiously reloading a page during 30seconds. Memory is allways stable around 80Mo and should probably don't go further. This is a naive benchmark just using ``top``.

