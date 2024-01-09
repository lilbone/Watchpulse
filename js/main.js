window.onload = () => {
  let myAjax;
  let c1;
  let isRequestPending = false;

  async function fetchOMDBData(movieTitle, type) {
    const apiKey = '62b9f284';
    const apiUrl = `http://www.omdbapi.com/?apikey=${apiKey}&t=${encodeURIComponent(movieTitle)}&type=${encodeURIComponent(type)}`;

    try {
      const response = await fetch(apiUrl);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Fehler beim Abrufen der Daten von OMDB:', error);
    }
  }

  const searchName = document.getElementById("search-name");
  const searchResult = document.getElementById("search-result");
  const searchType = document.getElementById("search-type");
  let omdbData;
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

    const movieInfo = document.createElement("div");
    movieInfo.classList.add("container");
    movieInfo.innerHTML = `<h2>${omdbData.Title}</h2><p>Year: ${omdbData.Year}</p><form id="form-add-watch" method="POST" action="` + url +`"><label for="my-rating">Deine Bewertung:</label>
    <input type="range" id="my-rating" name="my-rating" min="0" max="10" step="1" list="values" oninput="rangeValue.innerText = this.value"><datalist id="values"><option value="0" label="0"></option><option value="1" label="1"></option><option value="2" label="2"></option><option value="3" label="3"></option><option value="4" label="4"></option><option value="5" label="5" selected></option><option value="6" label="6"></option><option value="7" label="7"></option><option value="8" label="8"></option><option value="9" label="9"></option><option value="10" label="10"></option></datalist><p id="rangeValue">5</p><input type="submit" id="form-add-watch-submit" value="Add to Watches"></form>`;
    searchResult.appendChild(movieInfo);

    const formAddWatch = document.getElementById("form-add-watch");
    formAddWatch.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData();
      omdbData.myRating = document.getElementById("my-rating").value;
      formData.append("movieData", omdbData);
      const data = Object.fromEntries(formData.entries());
      console.log(omdbData);
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          alert("Movie added to Watches!");
        })
        .catch(error => {
          console.error("Error:", error);
        });
    });
  });
 /*  <form id="form" method="post" action="$SCRIPT_NAME">
    <div class="form-row">
      <label class="form-element" for="form-name">Name:</label>
      <div class="form-element">
        <input class="input-name" id="form-name" type="text" name="name" value="$sender">
      </div>
    </div>
  </form> */

  start();                  // start after loading HTML

  function start() {
    myAjax = new XMLHttpRequest();        // new AJAX object
    //myAjax.onreadystatechange = setInterval(readAjax, 2000);   // start readAjax when response is ready
    setInterval(update("0"), 1000);             // run update() every second
    //update("0");
    myAjax.onreadystatechange = function () {
      if (myAjax.readyState == 4 && myAjax.status == 200) {
        readAjax(); // Rufe die Funktion auf
        myAjax.onreadystatechange = null; // Setze onreadystatechange auf null, um zukünftige Aufrufe zu verhindern
      }
    };
  }


  // Filme Laden

  function update(block) {
    if (!isRequestPending) {
      isRequestPending = true;

      myAjax.open("POST", url, true);
      myAjax.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      myAjax.send("a_request=" + block);
    }
  }

  function readAjax() {
    if (myAjax.readyState == 4 && myAjax.status == 200) {
      c1 = document.getElementById('c1');

      // Leere das Element, bevor neue Daten hinzugefügt werden
      c1.innerHTML = "";

      const jsonData = myAjax.responseText.trim().split('\n');
      console.log(jsonData);
      for (let i = 0; i < jsonData.length; i++) {
        const movieData = JSON.parse(jsonData[i]);

        // Erstelle ein neues div für jeden Film
        const movieDiv = document.createElement("div");
        movieDiv.className = "movie-item";

        // Füge das Bild hinzu
        const posterImg = document.createElement("img");
        posterImg.src = movieData.Poster;
        movieDiv.appendChild(posterImg);

        // Füge die Daten hinzu
        const imdbRating = movieData.Ratings.find(rating => rating.Source === "Internet Movie Database");

        const movieInfo = document.createElement("div");
        movieInfo.innerHTML = `<h2>${movieData.Title}</h2><h3>Rating: ${imdbRating.Value}</h3><p>Year: ${movieData.Year}</p><p>${movieData.Plot}</p><br><p>Genre: ${movieData.Genre}</p><p>Director: ${movieData.Director}</p><p>Actors: ${movieData.Actors}</p>`;
        movieDiv.appendChild(movieInfo);

        // Füge das Film-Div dem Hauptelement hinzu
        c1.appendChild(movieDiv);
      }

      //c1.scrollTop = c1.scrollHeight;
      isRequestPending = false; // Setze die Variable zurück, wenn die Anfrage abgeschlossen ist
      update("b");
    }
  }

};