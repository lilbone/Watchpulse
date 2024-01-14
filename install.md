# Watch Pulse WebApp Install

## Installation von jq unter Linux

Führe die folgenden Befehle aus, um `jq` auf einem Linux-System zu installieren:

```bash
sudo apt update
sudo apt install -y jq
```

## Installation von git unter Linux

Führe die folgenden Befehle aus, um `git` auf einem Linux-System zu installieren:

```bash
sudo apt update
sudo apt install git
```

## Apache2-Konfiguration

Installation von Apache2

```bash
sudo apt update
sudo apt install apache2 
```

Füge die folgende Konfiguration zu den Directories zur `/etc/apache2/apache2.conf` hinzu, um den Zugriff auf das Verzeichnis der CGI-Skripte zu ermöglichen:

```apache
<Directory "/usr/lib/cgi-bin/Watchpulse">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

Füge die folgende Konfiguration zur `/etc/apache2/sites-available/000-default.conf` hinzu, um den Zugriff auf das Verzeichnis der CGI-Skripte zu ermöglichen:

```apache
<VirtualHost *:80>
    # ...

    DocumentRoot /lib/cgi-bin/Watchpulse

    # ...

    ScriptAlias /cgi-bin/ "/lib/cgi-bin/Watchpulse/"
    AddHandler cgi-script .cgi .pl .js

    <Directory "/lib/cgi-bin/Watchpulse/">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Require all granted
    </Directory>

</VirtualHost>
```

Nach den Änderungen muss der Apache Server neu gestartet werden:

```bash
service apache2 restart
```

## Dateien von Git herunterladen

Lade die Watch-Pulse Dateien in deinen Projekt-Ordner herunter

```bash
cd /lib/cgi-bin/
sudo git clone https://github.com/lilbone/Watchpulse.git
```

Anschließend musst du noch den Benutzer anpassen:

```bash
sudo chown -R www-data:www-data /lib/cgi-bin/Watchpulse
sudo chmod -R +x /lib/cgi-bin/Watchpulse
```
