History
=======

Version 1.1.4.1 - 2015/12/22
----------------------------

* Updated PO and french translation;
* Minor improvement on some CSS stuff;

Version 1.1.4 - 2015/12/21
--------------------------

* Added CPU temperature in monitoring using ACPI thermal API, close #38;
* Notify about missing system bios in rom list view, close #50;

Version 1.1.3 - 2015/12/19
--------------------------

* Updated Manifest to add zip extensions on some systems, related to #44 and #46;
* Granted ``bin`` extension for roms on Atari2600 system;
* Updated basic pip requirement file to fix Django version on 1.8.x for now;
* Fixed Makefile action ``install`` to use the right pip requirement file path;
* Added a global page footer containing the manager version, close #45;
* Only display supported extensions for knowed rom systems from manifest, for unknow system ddirs don't filter on file extension, close #40;
* Unmount ``/admin/`` because it's useless and may give back some ressources;
* Naive fix to avoid throwing exception on bad encoded filename in rom list view, just ignore it and continue. Related to #39;

Version 1.1.1 - 2015/11/01
--------------------------

* Cleaning deprecated stuff in assets_cartographer;
* Minor changes on url/texts in homepage;
* Added missing translation blocks;
* Updated PO and french translation;

Version 1.1.0 - 2015/10/17
--------------------------

* Better 'manager_frontend' structure, cleaning some minor things, close #34;
* Added ``asset_tag``;
* Dont show 'available systems' form if all systems allready exist, close #35;
* Moved 'Recalbox manifest' stuff into ``project.recalbox_manifest``, removed manifest loading from settings in profit of loading from ``urls.py``;

Version 1.0.2 - 2015/10/16
--------------------------

* Fixed CRLF caracters when editing recalbox config, close #31;
* Fixed not packaged assets with production settings;
* Refactored asset management to use persistent manifest registry (avoid to load JSON manifest file on every request) and move it to its own embedded app to ``project.assets_cartographer``, close #33;
* Open Virtual gamepad link into a new window/tab;
* Fixed Dropzone assets, close #32;
* Moved Python requirements to ``pip-requirements`` directory and refactored them for backward compatible with Recalbox versions without ``psutil`` yet;
* Added automatic deployment bash script in ``deployment/install.sh``, update Readme install procedure;

Version 1.0.1 - 2015/10/14
--------------------------

* Fixed wrong port for Virtual gamepad to 8080 (instead of 8081);

Version 1.0.0 - 2015/10/11
--------------------------

* Added Dropzone.js asset;
* Added all machinary to enabled Dropzone on rom upload;

Version 0.9.0 - 2015/10/03
--------------------------

* Added django migration command to makefile action ``install``;
* Added makefile action ``install-dev`` to install additional stuff for development;
* Added makefile action ``assets`` to build optimized assets (like for before committing asset changes);
* Moved ``psutil`` dependancies in basic ``requirements.txt``;
* Don't load anymore the whole Foundation components, only the used ones (win ~80ko on assets);
* Added homemade Asset management:
    
  * Centralized asset definition in a manifest file in ``project/assets.json``;
  * Use a template tag to read asset manifest to know what files to load for stylesheets and Javascripts assets;
  * Added Grunt stuff to use the asset manifest to build their optimized version for production;

Version 0.8.4 - 2015/09/26
--------------------------

* Updated dev requirements to ``django-icomoon==0.2``;
* Added ``hostname`` var to ``SITE`` in template context;
* Updated webfont;
* Added link to Recalbox 'virtual gamepad' app on homepage, close #24;
* Update README.rst;
* Minor fix in readme for runserver command for production;


Version 0.8.3 - 2015/09/21
--------------------------

* Updated package url in README
* Fixed Config edition error, close #18;
* Removed deprecated setting ``TEMPLATE_DEBUG``, close #20;
* Moved system information to its own view to avoid loading time on homepage, close #19;
* Fixed missing Foundation Javascripts assets, close #21;


Version 0.8.2 - 2015/09/20
--------------------------

* Fixed Rom systems grid using flexbox;
* Dont display System infos part on homepage if ``psutil`` is not installed;
* Added ``settings.RECALBOX_PSUTIL_CPU_INTERVAL`` to define time blocking interval to watch for cpu usage;

Version 0.8.1 - 2015/09/20
--------------------------

* Updated PO for last translatable string;
* Updated french PO;

Version 0.8.0 - 2015/09/20
--------------------------

* Added requirement file for development and Recalbox 3.3.0 beta5;
* Added ``django-icomoon usage`` for development;
* Added settings_production.py to use port 80 in production environment, close #13;
* Added safe usage of ``psutil`` library in homepage to display system infos, close #16;
* Removed Django contrib ``Site framework`` usage because we don``t use it anymore, related to #6;

Version 0.7.1 - 2015/09/06
--------------------------

* Finally finded a proper way to find host ip
* Added some settings so we can fix some host infos, related to #13
* Continued on system infos mining but disabled it (seems a fail)
* Added flexbox stuff in scss


Version 0.7.0 - 2015/09/06
--------------------------

* Added translated link to Recalbox wiki, #14;
* Removed template context variable ``SITE.domain`` usage in skeleton, #13;
* Updated Readme to include a line about migration on install, #12;
* Added settings_development and moved debug_toolbar instructions into this new settings env, #11;
* Updated PO files;
* Started to get system infos to display on homepage;
* Fix syntax error in German PO file, compile PO;
* Added German PO file;

Version 0.6.0 - 2015/08/31
--------------------------

* Parse the XML manifest within settings, close #3;
* Added XML manifest parser and (temporary?) ship the XML file for issue #3

Version 0.5.0 - 2015/08/31
--------------------------

* Refactored bios list and rom list views to include a delete form and the upload form in the same views, this close #1;

Version 0.4.5 - 2015/08/28
--------------------------

* Filled french PO file, compiled PO files, close #8;

Version 0.4.0 - 2015/08/27
--------------------------

* Enable i18n, make all texts translatable, create PO files for en and fr language this is for issue #8,  still have to fill the PO fr;

Version 0.3.0 - 2015/08/26
--------------------------

* Add option to backup config file before saving close #7;

Version 0.2.0 - 2015/08/25
--------------------------

* Add form config to edit Recalbox configuration #7;

Version 0.1.0 - 2015/08/24
--------------------------

* Add ``__init__.py`` file to contain project version;
