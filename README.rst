.. _Recalbox: http://recalbox.com
.. _recalbox-webconfig: https://github.com/MikaXII/recalbox-webconfig
.. _Django: https://www.djangoproject.com
.. _Foundation: http://foundation.zurb.com
.. _autobreadcrumbs: https://github.com/sveetch/autobreadcrumbs

Recalbox Manager Web Interface
==============================

Genauso wie `recalbox-webconfig`_ ist dieses Projekt eine Web-Schnittstelle, um allgemeine `Recalbox`_ Einstellungen zu verwalten, aber im Gegensatz zu *Node.js* mit `Django`_.

Dies ist ein komplettes Django Webapp Projekt, was bedeutet wenn es richtig installiert wurde, ist es bereit zum Start.

Eigenschaften
*************

* Versucht so vereinfacht wie möglich zu sein;
* Beruht strikt auf der Recalbox-Manifest-Datei zur Berechtigung von Uploads;
* Web-Integration basierend auf `Foundation`_;
* Lesen der Recalbox-Einträge (Logs);
* Bearbeitung der Recalbox Konfigurations-Datei;
    
  * Option zur Sicherung der Datei, bevor sie aktualisiert wird;

* Verwalte (Hochladen, Löschen) Deine Roms nach Systemen;
  
  * Nur unterstützte Erweiterungen der Systeme werden akzeptiert (von manifest);
  
* Verwalte (Hochladen, Löschen) Deine BIOS Dateien;

  * Nur unterstütze BIOS-Dateien werden akzeptiert (von manifest);
  * MD5 Checksummen Überprüfung;
  

Installation
************

Gängiges Linux System
-------------------

Nichts Spezielles, es sollten PIP und virtualenv auf Deinem System installiert sein, dann benutz Makefile: ::

    make install

Und voila, es ist vollbracht.

Recalbox System
---------------

Dies ist ein wenig anders, weil Recalbox nicht alle gängigen Bibliotheken und Werkzeuge besitzt, wie ein Linux System.

Bevor irgendwas gemacht wird, muss sichergestellt werden, das der RPI Zugang zum Internet hat, andernfalls richte Deinen Internet Zugang ein und falls erforderlich DNS-Auflösung.

Hole Dir das "project repository", gehe in dessen Verzeichnis und führe folgende Befehle aus: ::

    python -m ensurepip
    pip install virtualenv
    virtualenv --no-site-packages .
    bin/pip install -r requirements.txt

Die ersten beiden Zeilen werden nur beim ersten Mal benötigt.

Abschliessend, weil Git auf Recalbox nicht verfügbar ist, solltest Du Dir davor das Repository auf den PC holen, übertrage es auf Deine Recalbox und fahre dann mit den Befehlen fort.

Verwendung
**********

::

    source bin/activate
    python manage.py runserver 0.0.0.0:8001

Du solltest auch die Option ``--noreload`` am Ende vom letzten Befehl benutzen, wenn Du nicht vorhast an diesem Projekt mit zu entwickeln.
    
Entwicklungshinweise
*********************

#. Für die Entwicklung, kannst Du das Projekt auf gängige Linux-Systeme installieren, aber es ist erforderlich die Recalbox Dateistruktur für Roms, BIOS, Konfigurationsdatei, Protokolldatei, etc. zu reproduzieren. Oder Du kannst die benötigten Pfade in den Projekt-Einstellungen bearbeiten;

#. CSS wird mit "Compass Sources" kompiliert, Du musst den richtigen "Compass" installieren (verwende die `` mitgelieferte Gemfile`` -Datei) und Foundation 5 Version. (Benutze die zugewiesene "Makefile" Aktion);

#. Python 2.7.9 ist auf Recalbox 3.2.11 installiert, also ist *pip* fast bereit zur Nutzung, es muss beim ersten Mal nur noch installiert werden. Es wird mit ``pip==1.5.6`` installiert.

#. "Python devel lib" ist nicht installiert, aber es wird vielleicht gebraucht um einige Pakete von "eggs" zu installieren (momentan nicht benötigt);

#. UTC Zeitzone scheint nicht verfügbar zu sein, muss eingestellt werden. TIME_ZONE auf None und USE_TZ auf False. Es wird ein Dummy-Projekt gestartet, frisch erstellt vom startproject Django Befehl;

