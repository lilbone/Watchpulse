// Dieser Code wird ausgeführt, wenn die Webseite vollständig geladen ist
window.onload = () => {
  let myAjax;
  let c1;
  let isRequestPending = false;

  // Funktion, um Daten von der OMDB-API abzurufen
  async function fetchOMDBData(movieTitle, type) {
    const apiKey = '62b9f284';
    let apiUrl;
    if (movieTitle.startsWith("tt")) {
      apiUrl = `http://www.omdbapi.com/?apikey=${apiKey}&i=${encodeURIComponent(movieTitle)}&type=${encodeURIComponent(type)}`;
    } else {
      apiUrl = `http://www.omdbapi.com/?apikey=${apiKey}&t=${encodeURIComponent(movieTitle)}&type=${encodeURIComponent(type)}`;
    }

    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Fehler beim Abrufen der Daten von OMDB:', error);
    }
  }

  // Elemente im HTML-Dokument abrufen
  const searchName = document.getElementById("search-name");
  const searchResult = document.getElementById("search-result");
  const searchType = document.getElementById("search-type");
  let omdbData;

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
    movieInfo.innerHTML = `<h2>${omdbData.Title}</h2><p>Year: ${omdbData.Year}</p><form id="form-add-watch" method="POST" action="` + url + `"><label for="my-rating">Deine Bewertung:</label>
    <input type="range" id="my-rating" name="my-rating" min="0" max="10" step="1" list="values" oninput="rangeValue.innerText = this.value"><datalist id="values"><option value="0" label="0"></option><option value="1" label="1"></option><option value="2" label="2"></option><option value="3" label="3"></option><option value="4" label="4"></option><option value="5" label="5" selected></option><option value="6" label="6"></option><option value="7" label="7"></option><option value="8" label="8"></option><option value="9" label="9"></option><option value="10" label="10"></option></datalist><p id="rangeValue">5</p><input type="submit" id="form-add-watch-submit" value="Add to Watches"></form>`;
    searchResult.appendChild(movieInfo);

    // Event-Listener für das Hinzufügen eines Films zu den beobachteten Filmen
    const formAddWatch = document.getElementById("form-add-watch");
    formAddWatch.addEventListener("submit", async (e) => {
      e.preventDefault();
      omdbData.myRating = document.getElementById("my-rating").value;

      console.log("Daten vor dem Senden: \n" + JSON.stringify(omdbData));
      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "addWatch": "true",
          },
          body: JSON.stringify(omdbData),
        });

        if (response.ok) {
          console.log("Film zu den beobachteten Filmen hinzugefügt!");
        } else {
          throw new Error("Netzwerkantwort war nicht in Ordnung.");
        }
      } catch (error) {
        console.error("Fehler:", error);
      }
    });
  });

  // Starte die Update-Sequenz im Intervall
  start();

  // Funktion für die Update-Sequenz
  function start() {
    setInterval(() => update("0"), 1000);
  }

  // Funktion, um Filme zu aktualisieren
  function update(block) {
    if (!isRequestPending) {
      isRequestPending = true;

      // Daten vom Server abrufen
      fetch(url, {
        method: "POST",
        headers: {
          "Content-type": "application/x-www-form-urlencoded",
        },
        body: "a_request=" + block,
      })
        .then((response) => response.text())
        .then((jsonData) => {
          // Container im HTML löschen
          const c1 = document.getElementById('c1');
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

          isRequestPending = false;
        })
        .catch((error) => {
          console.error("Fehler:", error);
        });
    }
  }
};
