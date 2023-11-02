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

// Aggiunge l'evento di clic al tooltip
var tooltipTrigger = document.querySelector('.tooltip img');
tooltipTrigger.addEventListener('click', handleTooltipClick);