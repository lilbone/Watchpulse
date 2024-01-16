#!/bin/bash
# ***************************************************************
# * Filename      : addWatch.cgi
# * Author        : Bohn Matthias
# * Date          : 15.01.2024
# ***************************************************************

# Dateiname für die Watchlist
WATCHLIST_FILE=watchlist.txt
# Dateiname für den Log-File
LOG_FILE=log.txt

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
    "addWatch" )
      # Überprüfe, ob der Wert nicht leer ist
      if [ -n "$value" ]; then
        # Überprüfe, ob der Wert ein gültiges JSON ist
        if jq -e . >/dev/null 2>&1 <<< "$value"; then
          declare "$key=$value"
          echo "Processing parameter: $param" >> "$LOG_FILE"
        else
          echo "Error: Value for key $key is not valid JSON." >> "$LOG_FILE"
          exit 1  # Programm beenden
        fi
      else
        echo "Error: Value for key $key is empty." >> "$LOG_FILE"
        exit 1  # Programm beenden
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
  echo "Add Data to WATCHLIST_FILE" >> "$LOG_FILE"
  echo "" >> "$LOG_FILE"
  # Schreibe die Daten für einen neuen Watch in die watchlist-Datei
  echo "#STARTFILM"
  echo "$addWatch"
  echo "#ENDFILM"
fi >> "$WATCHLIST_FILE"
