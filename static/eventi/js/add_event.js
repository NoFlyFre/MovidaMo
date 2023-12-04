$(document).ready(function () {
    // Riferimento all'elemento del toggle e al campo di input del link dei biglietti
    var toggle = $('#id_enable_sell');
    var ticketLinkFieldWrapper = $('#id_tickets_link'); // Assumi che il campo tickets_link sia avvolto in un div con questa classe
    var labelTicketsUrl = $('#label-tickets-url')

    // Funzione per aggiornare la visibilità del campo del link dei biglietti
    function updateTicketLinkVisibility() {
        if (toggle.is(':checked')) {
            ticketLinkFieldWrapper.hide(); // Nasconde solo il campo del link dei biglietti
            labelTicketsUrl.hide();
        } else {
            ticketLinkFieldWrapper.show(); // Mostra solo il campo del link dei biglietti
            labelTicketsUrl.show();
        }
    }

    // Evento di cambio del toggle
    toggle.change(function () {
        updateTicketLinkVisibility(); // Aggiorna la visibilità ogni volta che il toggle cambia
    });

    // Chiamata iniziale per impostare la visibilità in base allo stato iniziale del toggle
    updateTicketLinkVisibility();
});

$(document).ready(function () {
    // Riferimento all'elemento del toggle e al campo di input del link dei biglietti
    var toggle = $('#enable-tickets');
    var ticketWrapper = $('.link-field'); // Assumi che il campo tickets_link sia avvolto in un div con questa classe
    var ticketLinkFieldWrapper = $('#id_tickets_link'); // Assumi che il campo tickets_link sia avvolto in un div con questa classe
    var labelTicketsUrl = $('#label-tickets-url')


    // Funzione per aggiornare la visibilità del campo del link dei biglietti
    function updateTicketLinkVisibility() {
        if (toggle.is(':checked')) {
            ticketWrapper.show(); // Nasconde solo il campo del link dei biglietti

        } else {
            ticketWrapper.hide(); // Mostra solo il campo del link dei biglietti
            ticketLinkFieldWrapper.hide();
            labelTicketsUrl.hide();
        }
    }

    // Evento di cambio del toggle
    toggle.change(function () {
        updateTicketLinkVisibility(); // Aggiorna la visibilità ogni volta che il toggle cambia
    });

    // Chiamata iniziale per impostare la visibilità in base allo stato iniziale del toggle
    updateTicketLinkVisibility();
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


  $(document).ready(function() {
    // Quando il custom file upload viene cliccato
    $('.custum-file-upload').on('click', function() {
        // Simula il click sull'input nascosto per l'upload dell'immagine
        $('#id_image').click();
    });

    // Quando viene selezionato un file tramite l'input nascosto per l'immagine
    $('#id_image').on('change', function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                // Imposta lo sfondo del custom file upload con l'immagine selezionata
                $('.custum-file-upload').css({
                    'background-image': 'url(' + e.target.result + ')',
                    'background-size': 'cover', // questo farà in modo che l'immagine copra tutto lo sfondo, mantenendone le proporzioni
                    'background-position': 'center center', // centra l'immagine
                    'background-repeat': 'no-repeat' // impedisce la ripetizione dell'immagine
                });
                
            };
            reader.readAsDataURL(input.files[0]);
        }
    });
});

  
  
  
  
  
  