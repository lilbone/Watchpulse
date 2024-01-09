#!/bin/bash

CHAT_FILE=chat2.txt

echo -ne "Content-type: text/html; charset=utf-8\n\n"

read querystring
eval "${querystring//&/;}"
                                         # colors for chatmember display
color=( "#ff0000" "#00ff00" "#0000ff" "#ffff00" "#00ffff" "#ff00ff" \
        "#ff8000" "#80ff00" "#00ff80" "#0080ff" "#8000ff" "#ff0080" )

'if [[ -n $submit ]]                      # append new message to file
'then
'  sender="$(echo -e ${name//%/\\x} | tr '+' ' ')"
'  date +"#TIMESTAMP %F %T "
'  echo -e "#SENDER $sender"
'  echo "#STARTMESSAGE"
'  echo -e "${message//%/\\x}" | tr '+' ' ' | tr -d '#'
'  echo "#ENDMESSAGE"
'fi >> $CHAT_FILE'
if [[ -n $submit ]]; then
  sender="$(echo -e ${name//%/\\x} | tr '+' ' ')"
  date +"#TIMESTAMP %F %T "
  echo -e "#SENDER $sender"
  echo "#STARTMESSAGE"
  echo -e "${message//%/\\x}" | tr '+' ' ' | tr -d '#'
  echo "#ENDMESSAGE"
fi >> $CHAT_FILE

if [[ -n $a_request ]]; then
  # Response to AJAX-request
  # Block response until file modify...
  [[ $a_request = b ]] && inotifywait -e modify "$CHAT_FILE" > /dev/null 2>&1

  while read -r line; do
    if [[ "$line" =~ ^\#STARTFILM ]]; then
      unset message
      while read -r line; do
        [[ "$line" =~ ^\#ENDFILM ]] && break
        message+="${line}"
      done

      # Output only XML data
      echo $message
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
    <style>
EOF
   cat css/main.css
   cat css/0.css
   cat css/576.css
   cat css/768.css
   cat css/992.css
   cat css/1200.css
cat << EOF
    </style>
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
            <h1>Wach Pulse</h1>
          </div>
          <div class="menu-items">
            <li><a href="#">Home</a></li>
            <li><a href="#">My Watches</a></li>
            <li><a href="#">New Watch</a></li>
          </div>
        </div>
      </div>
    </nav>
  </header>

  <main>
    <div id="home" class="section vh-90">
      <div class="container t-center">
        <h1>Wilkommen bei Watch Pulse<br>Deinem persönlichen Film- und Serienbegleiter!</h1>
        <h2>Tauche ein in die Welt des Entertainments mit Watch Pulse<br>Unsere App ermöglicht es dir, all deine gesehenen Filme und Serien an einem Ort zu verwalten.<br><br>Behalte den Überblick über deine persönlichen Bewertungen, entdecke neue Inhalte und gestalte deine Watchlist ganz nach deinem Geschmack.</h2>
      </div>
    </div>
    <div id="my-watches" class="section vh-100">
      <div class="container t-center">
        <h1>My Watches</h1>
        <h2>Hier findest du deine gespeicherten Inhalte</h2>
        <div class="ajax-content" id="c1">
        </div>
      </div>
    </div>
    <div id="add-watches" class="section vh-80">
      <div class="container t-center">
        <h1>Search your Watch</h1>
        <div id="search-film">
          <label for="search-type">Type:</label>
          <select id="search-type">
            <option value="movie">Movie</option>
            <option value="series">Series</option>
            <option value="episode">Episode</option>
          </select>
          <label for="search-name">Name:</label>
          <input id="search-name" type="text" name="name">
        </div>
        <div id="search-result">
        </div>
      </div>
    </div>
    
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
