#!/bin/bash

CHAT_FILE=watchlist.txt

echo -ne "Content-type: text/html; charset=utf-8\n\n"

read -r querystring

# Sicherere Verarbeitung der Eingabe und logging
IFS='&' read -ra params <<< "$querystring"
for param in "${params[@]}"; do
  echo "Query-Paramter: $querystring" >> log.txt
  IFS='=' read -r key value <<< "$param"
  declare "$key=$value"
done

if [[ "$(echo "$HTTP_ADDWATCH")" == "true" ]]
then
  echo "Received addWatch request. Data: $querystring" >> log.txt
  echo "#STARTFILM"
  echo "$querystring"
  echo "#ENDFILM"
fi >> $CHAT_FILE

if [[ -n $a_request ]]; then
  [[ $a_request = b ]] && inotifywait -e modify "$CHAT_FILE" > /dev/null 2>&1

  while read -r line; do
    if [[ "$line" =~ ^\#STARTFILM ]]; then
      unset message
      while read -r line; do
        [[ "$line" =~ ^\#ENDFILM ]] && break
        message+="${line}"
      done

      # Sicherer Output nur von XML-Daten
      echo "$message"
    fi
  done < "$CHAT_FILE"
else

cat << EOF
<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <title>Watch Pulse</title>
    <link href="/css/main.css" rel="stylesheet">
    <link href="/css/0.css" rel="stylesheet">
    <link href="/css/576.css" rel="stylesheet">
    <link href="/css/768.css" rel="stylesheet">
    <link href="/css/992.css" rel="stylesheet">
    <link href="/css/1200.css" rel="stylesheet">
</head>

<body>
  <header>
    <nav>
      <div class="navbar">
        <div class="container nav-container">
            <input class="checkbox" type="checkbox" name="" id="" />
            <div class="hamburger-lines">
              <span class="line line1"></span>
              <span class="line line2"></span>
              <span class="line line3"></span>
            </div>  
          <div class="logo">
            <a href="#"><img src="/logo_watch-pulse.png" alt="Watch Pulse Logo"></a>
          </div>
          <div class="menu-items">
            <li><a href="#">Home</a></li>
            <li><a href="#my-watches">My Watches</a></li>
            <li><a href="#add-watches">New Watch</a></li>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <section id="home" class="section vh-90">
      <div class="container t-center">
        <h1>Watch Pulse<br><span>Dein persönlicher Film- und Serienbegleiter!</span></h1>
        <h2>Tauche ein in die Welt des Entertainments mit Watch Pulse<br>Unsere App ermöglicht es dir, all deine gesehenen Filme und Serien an einem Ort zu verwalten.<br><br>Behalte den Überblick über deine persönlichen Bewertungen, entdecke neue Inhalte und gestalte deine Watchlist ganz nach deinem Geschmack.</h2>
      </div>
    </section>

    <section id="my-watches" class="section vh-100">
      <div class="container t-center">
        <h1>My Watches</h1>
        <h2>Hier findest du deine Watches</h2>
        <div class="ajax-content" id="c1">
        </div>
      </div>
    </section>

    <section id="add-watches" class="section vh-100">
      <div class="container t-center">
        <h1>Search your Watch</h1>
        <div id="search-film">
          <label for="search-type">Type:</label>
          <select id="search-type">
            <option value="movie">Movie</option>
            <option value="series">Series</option>
            <option value="episode">Episode</option>
          </select>
          <label for="search-name">Name / IMBd-Nr.:</label>
          <input id="search-name" type="text" name="name">
        </div>
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
