/* ################################################################
 Filename      : main.js
 Author        : Bohn Matthias
 Date          : 12.01.2024
################################################################ */
// Dieser Code wird ausgeführt, wenn die Webseite vollständig geladen ist
window.onload = () => {
  // Deklaration von Variablen
  let myAjax;
  let c1;
  let isRequestPending = false;
  let omdbData;

  // Elemente im HTML-Dokument abrufen
  const searchName = document.getElementById("search-name");
  const searchResult = document.getElementById("search-result");
  const searchType = document.getElementById("search-type");

  // Funktion, um Daten von der OMDB-API abzurufen
  async function fetchOMDBData(movieTitle, type) {
    // API-Key für den Zugriff auf die OMDB-API
    const apiKey = '62b9f284';
    let apiUrl;

    // Aufbau der API-URL abhängig vom Filmtitel bzw. der IMDB-ID
    if (movieTitle.startsWith("tt")) {
      apiUrl = `http://www.omdbapi.com/?apikey=${apiKey}&i=${encodeURIComponent(movieTitle)}&type=${encodeURIComponent(type)}`;
    } else {
      apiUrl = `http://www.omdbapi.com/?apikey=${apiKey}&t=${encodeURIComponent(movieTitle)}&type=${encodeURIComponent(type)}`;
    }

    try {
      // Fetch-Anfrage an die OMDB-API senden
      const response = await fetch(apiUrl);
      // JSON-Daten der Antwort extrahieren
      const data = await response.json();
      return data;
    } catch (error) {
      // Fehlerbehandlung bei der Anfrage an die OMDB-API
      console.error('Fehler beim Abrufen der Daten von OMDB:', error);
    }
  }

  // Event-Listener für Änderungen im Suchfeld
  searchName.addEventListener("change", async (e) => {
    // Verwende die Funktion und speichere das Ergebnis in einer Variable
    searchResult.innerHTML = "";
    omdbData = await fetchOMDBData(e.target.value, searchType.value);
    // Überprüfe das Ergebnis
    console.log(omdbData);

    // Füge das Bild hinzu
    const posterImg = document.createElement("img");
    posterImg.src = omdbData.Poster;
    searchResult.appendChild(posterImg);

    // Erstelle ein Container-Div für Filminformationen
    const movieInfo = document.createElement("div");
    movieInfo.classList.add("container");
    movieInfo.innerHTML = `<h2>${omdbData.Title}</h2><p>Year: ${omdbData.Year}</p><p>Genre: ${omdbData.Genre}</p><form id="form-add-watch" method="POST" action="` + url + `"><label for="my-rating">Deine Bewertung:</label>
    <input type="range" id="my-rating" name="my-rating" min="0" max="10" step="1" list="values" oninput="rangeValue.innerText = this.value"><p id="rangeValue">5</p><input type="submit" id="form-add-watch-submit" value="Add to Watches"></form>`;
    searchResult.appendChild(movieInfo);

    // Event-Listener für das Hinzufügen eines Films zu den beobachteten Filmen
    const formAddWatch = document.getElementById("form-add-watch");
    formAddWatch.addEventListener("submit", async (e) => {
      e.preventDefault();
      omdbData.myRating = document.getElementById("my-rating").value;

      console.log("Daten vor dem Senden: \n" + JSON.stringify(omdbData));
      try {
        // Fetch-Anfrage an den Server senden
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "addWatch": "true",
          },
          body: "addWatch=" + JSON.stringify(omdbData),
        });

        if (response.ok) {
          console.log("Film zu den beobachteten Filmen hinzugefügt!");
        } else {
          throw new Error("Netzwerkantwort war nicht in Ordnung.");
        }
      } catch (error) {
        // Fehlerbehandlung bei der Fetch-Anfrage an den Server
        console.error("Fehler:", error);
      }
    });
  });

  // Starte die Update-Sequenz im Intervall
  start();

  // Funktion für die Update-Sequenz
  function start() {
    // Intervall für die Update-Sequenz festlegen
    const genre = document.getElementById("filter");
    setInterval(() => update(genre.value), 1000);
    //update("all");
  }

  // Funktion, um Filme zu aktualisieren
  function update(block) {
    // Prüfen, ob bereits eine Anfrage aussteht
    if (!isRequestPending) {
      isRequestPending = true;

      // Daten vom Server abrufen
      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/x-www-form-urlencoded",
        },
        body: "load_watchlist=" + block,
      })
        .then((response) => response.text())
        .then((jsonData) => {
          // Container im HTML löschen
          const c1 = document.getElementById('show-watchlist');
          c1.innerHTML = "";

          // JSON-Daten verarbeiten und Filme anzeigen
          jsonData.trim().split('\n').forEach((data) => {
            const movieData = JSON.parse(data);

            const movieDiv = document.createElement("div");
            movieDiv.className = "movie-item";

            const posterImg = document.createElement("img");
            posterImg.src = movieData.Poster;
            movieDiv.appendChild(posterImg);

            const imdbRating = movieData.Ratings.find(rating => rating.Source === "Internet Movie Database");

            const movieInfo = document.createElement("div");
            movieInfo.className = "movie-info";
            movieInfo.innerHTML = `<h2>${movieData.Title}</h2><h3>Deine Bewertung: ${movieData.myRating}/10</h3><h4>IMDb-BEWERTUNG: ${imdbRating.Value}</h4><p>Year: ${movieData.Year}</p><p>${movieData.Plot}</p><br><p>Genre: ${movieData.Genre}</p><p>Director: ${movieData.Director}</p><p>Actors: ${movieData.Actors}</p>`;
            movieDiv.appendChild(movieInfo);

            c1.appendChild(movieDiv);
          });

          // Anfrage-Status aktualisieren
          isRequestPending = false;
        })
        .catch((error) => {
          // Fehlerbehandlung bei der Fetch-Anfrage an den Server
          // Container im HTML löschen
          const c1 = document.getElementById('show-watchlist');
          c1.innerHTML = "";

          // Meldung ausgeben wenn kein Watch gefunden wird
          const errorMessage = document.createElement("p");
          errorMessage.id = "error-message";
          errorMessage.textContent = "Mit diesem Filter ist kein Watch vorhanden!";
          c1.appendChild(errorMessage);
          console.log("Mit diesem Filter ist kein Watch vorhanden!");
          //console.log("Fehler:", error);
          isRequestPending = false;
        });
    }
  }
};
