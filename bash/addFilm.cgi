#!/bin/bash

CHAT_FILE=chat2.txt

read -r POST_DATA
if [[ -n $POST_DATA ]]
then
  echo "POST-DATA received: $POST_DATA"  # Hier wird der Text in der Kommandozeile ausgegeben
  echo -e "#STARTFILM"
  echo -e "$POST_DATA"
  echo "#ENDFILM"
fi >> $CHAT_FILE
