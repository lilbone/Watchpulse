#!/bin/bash
# ***************************************************************
# * Filename      : Watchpulse.cgi
# * Author        : Bohn Matthias
# * Date          : 12.01.2024
# ***************************************************************

# Dateiname für die Watchlist
WATCHLIST_FILE=watchlist.txt
# Dateiname für den Log-File
LOG_FILE=log.txt
# Maximale Anzahl der Zeilen im Log-File
MAX_LOG_LINES=100

# HTTP-Header setzen
echo -ne "Content-type: text/html; charset=utf-8\n\n"

# Querystring einlesen
read -r querystring

# Sicherere Verarbeitung der Eingabe und Logging
IFS='&' read -ra params <<< "$querystring"

for param in "${params[@]}"; do
  # Logge die Zeitstempel der Requests
  echo "Timestamp: $(date)" >> "$LOG_FILE"

  IFS='=' read -r key value <<< "$param"

  # Überprüfe, ob der Key und Value sinnvolle Werte haben
  case "$key" in
    "load_watchlist" | "addWatch" )
      # Füge hier weitere erlaubte Keys hinzu
      # Prüfe, ob der Wert nicht leer ist
      if [ -n "$value" ]; then
        declare "$key=$value"
        echo "Processing parameter: $param" >> "$LOG_FILE"
      else
        echo "Error: Value for key $key is empty." >> "$LOG_FILE"
      fi
      ;;

    *)
      # Unerlaubter Key 
      echo "Error: Invalid key $key." >> "$LOG_FILE"
      exit 1  # Programm beenden
      ;;
  esac
done

# Wenn HTTP_ADDWATCH auf "true" gesetzt ist, füge den Eintrag zur Watchlist hinzu
if [[ "$(echo "$HTTP_ADDWATCH")" == "true" ]]; then
  # Logge den empfangenen addWatch-Request und die Daten
  echo "Received addWatch request. Data: $addWatch" >> "$LOG_FILE"
  echo "#STARTFILM"
  echo "$addWatch"
  echo "#ENDFILM"
fi >> "$WATCHLIST_FILE"

# Beschränke die Anzahl der Zeilen im Log-File auf MAX_LOG_LINES
if [ "$(wc -l < "$LOG_FILE")" -gt "$MAX_LOG_LINES" ]; then
  # Lösche die ältesten Zeilen, um die Anzahl zu begrenzen
  sed -i "1,$(($(wc -l < "$LOG_FILE") - $MAX_LOG_LINES + 1))d" "$LOG_FILE"
fi

# Falls load_watchlist vorhanden ist, benutze inotifywait, um auf Änderungen zu warten
if [[ -n $load_watchlist ]]; then
  echo "load_watchlist is present. Value: $load_watchlist" >> "$LOG_FILE"
  [[ $load_watchlist = b ]] && inotifywait -e modify "$WATCHLIST_FILE" > /dev/null 2>&1

  # Durchlaufe die Watchlist und extrahiere Filme
  while read -r line; do
    if [[ "$line" =~ ^\#STARTFILM ]]; then
      echo "Found film entry in the watchlist." >> "$LOG_FILE"
      unset message
      while read -r line; do
        [[ "$line" =~ ^\#ENDFILM ]] && break
        message+="${line}"
      done

      echo "Film data: $message" >> "$LOG_FILE"

      genres=$(echo "$message" | jq -r '.Genre')
      IFS=', ' read -ra movie_genres <<< "$genres"
      match_found=false

      # Jetzt enthält die Variable genre_array die Genres als Elemente eines Arrays.
      # Sie können über das Array iterieren und jedes Genre ausgeben, um zu überprüfen, ob es korrekt ist.
      echo "Genre array for the current film: ${movie_genres[@]}" >> "$LOG_FILE"

      # Überprüfe, ob der übergebene Genre-Wert "all" ist oder in den Genres des Films enthalten ist
      for genre in "${movie_genres[@]}"; do
        case "$load_watchlist" in
          "all")
            match_found=true
            ;;
          $genre)
            match_found=true
            ;;
        esac
      done

      if [ "$match_found" == true ]; then
        echo "Film matched the requested genre. Outputting film data." >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
        echo "$message"
      else
        echo "Film did not match the requested genre. Skipping output." >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
      fi
    fi
  done < "$WATCHLIST_FILE"
else

cat << EOF
<!DOCTYPE html>
<html lang="de">

<head>
    <!-- Meta-Tags für Dokumenteigenschaften und Responsive Design -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">

    <!-- Titel des Dokuments -->
    <title>Watch Pulse</title>

    <!-- Favicon für verschiedene Plattformen -->
    <link rel="apple-touch-icon" sizes="180x180" href="/media/favicon_io/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/media/favicon_io/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/media/favicon_io/favicon-16x16.png">
    <link rel="manifest" href="/media/favicon_io/site.webmanifest">

    <!-- Stylesheets für verschiedene Bildschirmgrößen -->
    <link href="/css/main.css" rel="stylesheet">
    <link href="/css/0.css" rel="stylesheet">
    <link href="/css/576.css" rel="stylesheet">
    <link href="/css/768.css" rel="stylesheet">
    <link href="/css/992.css" rel="stylesheet">
    <link href="/css/1200.css" rel="stylesheet">
</head>

<body>
  <!-- Header mit Navigationsleiste -->
  <header>
    <nav>
      <div class="navbar">
        <!-- Container für Navigationsleiste -->
        <div class="container nav-container">
            <!-- Checkbox für das Hamburger-Menü -->
            <input class="checkbox" type="checkbox" name="" id="" />
            <!-- Hamburger-Menü-Symbole -->
            <div class="hamburger-lines">
              <span class="line line1"></span>
              <span class="line line2"></span>
              <span class="line line3"></span>
            </div>  
          <!-- Logo-Bereich mit Link zur Startseite -->
          <div class="logo">
            <a href="#"><img src="/media/logo_watch-pulse.png" alt="Watch Pulse Logo"></a>
          </div>
          <!-- Menüpunkte -->
          <div class="menu-items">
            <li><a href="#">Home</a></li>
            <li><a href="#my-watches">My Watches</a></li>
            <li><a href="#add-watches">New Watch</a></li>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <!-- Hauptinhalt der Seite -->
  <main>
    <!-- Sektion für die Startseite -->
    <section id="home" class="section vh-90">
      <!-- Container für den Inhalt -->
      <div class="container t-center">
        <!-- Überschrift und Untertitel für die Startseite -->
        <h1>Watch Pulse<br><span>Dein persönlicher Film- und Serienbegleiter!</span></h1>
        <h2>Tauche ein in die Welt des Entertainments mit Watch Pulse<br>Unsere App ermöglicht es dir, all deine gesehenen Filme und Serien an einem Ort zu verwalten.<br><br>Behalte den Überblick über deine persönlichen Bewertungen, entdecke neue Inhalte und gestalte deine Watchlist ganz nach deinem Geschmack.</h2>
      </div>
    </section>

    <!-- Sektion für die Anzeige der Watchlist -->
    <section id="my-watches" class="section vh-100">
      <!-- Container für den Inhalt -->
      <div class="container t-center">
        <!-- Überschrift und Untertitel für die Watchlist -->
        <h1>My Watches</h1>
        <div id="my-watches-filter">
          <h2>Hier findest du deine Watches</h2>
          <!-- Dropdown für den Filter -->
          <div class="center-filter">
            <label for="filter">Filter:</label>
            <select id="filter">
              <option value="all">Alle</option>
              <option value="Action">Action</option>
              <option value="Crime">Crime</option>
              <option value="Drama">Drama</option>
              <option value="Fantasy">Fantasy</option>
              <option value="Horror">Horror</option>
              <option value="Mystery">Mystery</option>
              <option value="Romance">Romance</option>
              <option value="Sci-Fi">Science Fiction</option>
              <option value="Thriller">Thriller</option>
              <option value="Adventure">Adventure</option>
            </select>
          </div>
        </div>
        <!-- Ajax-Content-Bereich für dynamische Inhalte -->
        <div class="ajax-content" id="show-watchlist">
        </div>
      </div>
    </section>

    <!-- Sektion für die Suche nach Filmen/Serien -->
    <section id="add-watches" class="section vh-100">
      <!-- Container für den Inhalt -->
      <div class="container t-center">
        <!-- Überschrift und Eingabebereich für die Suche -->
        <h1>Search your Watch</h1>
        <div id="search-film">
          <!-- Dropdown für den Typ (Movie, Series, Episode) -->
          <label for="search-type">Type:</label>
          <select id="search-type">
            <option value="movie">Movie</option>
            <option value="series">Series</option>
            <option value="episode">Episode</option>
          </select>
          <!-- Eingabefeld für den Namen oder die IMBd-Nummer -->
          <label for="search-name">Name / IMBd-Nr.:</label>
          <input id="search-name" type="text" name="name">
        </div>
        <!-- Bereich für die Anzeige der Suchergebnisse -->
        <div id="search-result">
        </div>
      </div>
    </section>
    
  </main>

  <script>
  "use strict";

  var url = "$SCRIPT_NAME";

EOF
   cat js/main.js
cat << EOF
  </script>
</body>

</html>
EOF
fi
