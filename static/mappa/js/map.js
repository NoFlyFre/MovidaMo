
mapboxgl.accessToken =
    "pk.eyJ1Ijoibm9mbHlmcmUiLCJhIjoiY2xoamZ5eGFmMGI5ZzNyb3h0ZDN0NjhhcSJ9.qq8uvd4j2EwUInsWlaJ7eQ";
var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/dark-v10",
    center: [10.9254, 44.6471], // Coordinate di Modena
    zoom: 12,
});

// Initialize the geolocate control.
var geolocate = new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true,
    },
    trackUserLocation: true,
    showUserHeading: true,
    fitBoundsOptions: {
        maxZoom: 12,
    },
});

// Add the control to the map.
map.addControl(geolocate);

map.on("load", function () {
    geolocate.on("geolocate", function (e) {
        // Posizione utente ottenuta con successo
        console.log("Geolocated:", e.coords);
    });

    geolocate.on("error", function (e) {
        // Errore nella geolocalizzazione, utilizza la posizione di Modena come fallback
        console.log("Geolocation error:", e.error);
        map.setCenter([10.9254, 44.6471]);
    });

    geolocate.trigger(); // Attiva automaticamente la geolocalizzazione


    // Array dei marker
    var markers = [];

    // Itera sugli eventi e crea i marker
    eventi.forEach(function (evento) {
        var lat = evento.fields.mappa_lat;
        var lng = evento.fields.mappa_long;

        var el = document.createElement("div");
        el.className = "marker";
        el.setAttribute("data-event-id", evento.pk);
        el.style.backgroundColor = "#fccd22";
        el.style.width = "20px";
        el.style.height = "20px";
        el.style.border = "2px solid #1e275c";
        el.style.borderRadius = "50%";
        el.style.boxShadow =
            "0px 0px 2.2px rgba(0, 0, 0, 0.073),0px 0px 5.3px rgba(0, 0, 0, 0.105),0px 0px 10px rgba(0, 0, 0, 0.13),0px 0px 17.9px rgba(0, 0, 0, 0.155),0px 0px 33.4px rgba(0, 0, 0, 0.187),0px 0px 80px rgba(0, 0, 0, 0.26)";

        var marker = new mapboxgl.Marker(el).setLngLat([lng, lat]).addTo(map);

        el.markerInstance = marker; // here's where I add the marker instance to the DOM element

        markers.push(marker);

        el.addEventListener("click", e => {

            // here's where I can use the "markerInstance" I added earlier to then expose the getLngLat
            let coords = e.target.markerInstance.getLngLat();

            let adjustedCoords = {
                lng: coords.lng,
                lat: coords.lat - 0.003
            };

            //tell the map to center on the marker coordinates
            map.flyTo({
                center: adjustedCoords,
                speed: 1,
                zoom: 14,
            });
        });

        el.addEventListener("click", e => {

            changeMarkerColor(e);

            console.log("Clicked:", e.target.getAttribute("data-event-id"));
            hideEventCard();
            let eventId = e.target.getAttribute("data-event-id");

            // Ferma la propagazione dell'evento per evitare che venga considerato un click sulla mappa
            e.stopPropagation();

            // Mostra la card corrispondente all'evento selezionato
            showEventCard(eventId);

        });

        // Crea i limiti dei marker
        var bounds = new mapboxgl.LngLatBounds();
        markers.forEach(function (marker) {
            bounds.extend(marker.getLngLat());
        });

        // Aggiungi la posizione della geolocalizzazione ai limiti
        if (geolocate && geolocate.options && geolocate.options.position) {
            bounds.extend(geolocate.options.position);
        }


        function changeMarkerColor(e) {
            // Rimuovi lo stile dai marker precedenti
            markers.forEach(marker => {
                marker.getElement().style.backgroundColor = "#fccd22";
                marker.getElement().style.borderWidth = "2px";
                marker.getElement().style.borderStyle = "solid";
                marker.getElement().style.borderColor = "#1e275c";
                marker.getElement().style.width = "20px";
                marker.getElement().style.height = "20px";
                marker.getElement().style.transform = "scale(1)";
            });

            // Aggiungi lo stile al marker corrente
            let markerElement = e.target.markerInstance.getElement();
            markerElement.style.backgroundColor = "#1e275c";  // Esempio: Cambia colore di sfondo a rosso
            markerElement.style.borderWidth = "2px";  // Esempio: Aumenta lo spessore del bordo a 3px
            markerElement.style.borderStyle = "solid";  // Esempio: Cambia lo stile del bordo a tratteggiato
            markerElement.style.borderColor = "#fccd22";  // Esempio: Cambia il colore del bordo a nero
            markerElement.style.width = "30px";  // Esempio: Aumenta la larghezza del marker a 30px
            markerElement.style.height = "30px";  // Esempio: Aumenta l'altezza del marker a 30px
            markerElement.style.transform = "scale(1.5)";  // Esempio: Ingrandisci il marker al 150%
        }

        function resetMarkerColor() {
            markers.forEach(marker => {
                marker.getElement().style.backgroundColor = "#fccd22";
                marker.getElement().style.borderWidth = "2px";
                marker.getElement().style.borderStyle = "solid";
                marker.getElement().style.borderColor = "#1e275c";
                marker.getElement().style.width = "20px";
                marker.getElement().style.height = "20px";
                marker.getElement().style.transform = "scale(1)";

            });
        }

        function showEventCard(eventId) {
            // Recupera l'elemento HTML della card corrispondente all'ID dell'evento
            let card = document.getElementById("event_" + eventId);

            // Mostra la card
            card.style.display = "flex";
        }

    
        map.on("click", function (e) {
            console.log("Clicked:", e.lngLat);
            // Nascondi la card corrispondente all'evento selezionato
            hideEventCard();
            resetMarkerColor();
            // Controlla se ci sono solo uno o nessun marker
            if (markers.length <= 1) {
                console.log("marker:" + markers.length);
                // Zooma più indietro
                map.fitBounds(bounds, { padding: 100, maxZoom: 13 });
            } else {
                // Rimpicciolisci la mappa per mostrare tutti i marker e la posizione di geolocalizzazione
                map.fitBounds(bounds, { padding: 100 });
            }
        });

        map.on("dragstart", function (e) {
            console.log("Clicked:", e.lngLat);
            // Nascondi la card corrispondente all'evento selezionato
            hideEventCard();
            resetMarkerColor();
            // Controlla se ci sono solo uno o nessun marker
        });

        function hideEventCard() {
            // Nascondi la card
            var cards = document.querySelectorAll(".card");

            // Itera su ogni elemento e nascondilo
            cards.forEach(function (card) {
                card.style.display = "none";
            });
        }




    });
});
