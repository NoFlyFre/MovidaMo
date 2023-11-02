let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)

$(document).ready(function () {
  // Ottieni il riferimento all'elemento del toggle
  var toggle = $('#private-events-toggle');

  // Gestisci l'evento di cambio del toggle
  toggle.change(function () {
    // Ottieni il nuovo stato del toggle
    var isChecked = toggle.is(':checked');

    // Invia una richiesta AJAX per aggiornare il valore nel database
    $.ajax({
      url: 'update_private_events/',  // URL per l'endpoint di aggiornamento nel tuo server
      type: 'POST',
      headers: {
        'X-CSRFToken': csrfToken
      },
      data: {
        private_events: isChecked  // Passa il nuovo valore come parametro nella richiesta
      },
      success: function (response) {
        // Gestisci la risposta del server se necessario
        console.log(response);
      },
      error: function (xhr, status, error) {
        // Gestisci gli errori se necessario
        console.error(error);
      }
    });
  });
});

// Variabile di stato per il tooltip
var tooltipOpen = false;

// Funzione per aprire il tooltip
function openTooltip() {
  var tooltip = document.querySelector('.tooltip');
  tooltip.querySelector('.tooltiptext').style.opacity = '1';
  tooltipOpen = true;
}

// Funzione per chiudere il tooltip
function closeTooltip() {
  var tooltip = document.querySelector('.tooltip');
  tooltip.querySelector('.tooltiptext').style.opacity = '0';
  tooltipOpen = false;
}

// Gestore dell'evento di clic sul tooltip
function handleTooltipClick() {
  if (tooltipOpen) {
    closeTooltip();
  } else {
    openTooltip();
  }
}

// Chiude il tooltip quando si fa clic altrove sulla pagina
document.addEventListener('click', function (event) {
  var tooltip = document.querySelector('.tooltip');
  if (tooltip && !tooltip.contains(event.target)) {
    closeTooltip();
  }
});

var tooltipTrigger = document.querySelector('.tooltip img');
if (tooltipTrigger) {
    tooltipTrigger.addEventListener('click', handleTooltipClick);
}

$("#friend_request_btn").click(function() {
  console.log("Friend request button clicked");
  $.ajax({
      type: "POST",
      url: `/user/send_friend_request/${profileUsername}/`, // Assicurati di avere user_id disponibile
      headers: {
          'X-CSRFToken': getCookie('csrftoken')
      },
      success: function(response) {
          if(response.status === "success") {
              // Cambia l'aspetto del pulsante
              const sentRequestDiv = `
                  <div class="friend_request">
                      <button type="button" id="friend_request_btn">
                          <svg xmlns="http://www.w3.org/2000/svg" height="1em" viewBox="0 0 640 512"><!--! Font Awesome Free 6.4.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path d="M224 0a128 128 0 1 1 0 256A128 128 0 1 1 224 0zM178.3 304h91.4c20.6 0 40.4 3.5 58.8 9.9C323 331 320 349.1 320 368c0 59.5 29.5 112.1 74.8 144H29.7C13.3 512 0 498.7 0 482.3C0 383.8 79.8 304 178.3 304zM352 368a144 144 0 1 1 288 0 144 144 0 1 1 -288 0zm144-80c-8.8 0-16 7.2-16 16v64c0 8.8 7.2 16 16 16h48c8.8 0 16-7.2 16-16s-7.2-16-16-16H512V304c0-8.8-7.2-16-16-16z"/></svg>
                          Richiesta inviata
                      </button>
                  </div>`;
              $('.friend_request').replaceWith(sentRequestDiv);
          } else {
              // Gestisci eventuali errori
              alert("Errore nell'invio della richiesta di amicizia");
          }
      }
  });
});
