$(document).ready(function() {
    // Quando viene selezionato un file tramite l'input nascosto
    $('#id_profile_picture').on('change', function() {
        var input = this;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                // Aggiorna l'immagine del profilo con il file selezionato
                $('.profile-image img').attr('src', e.target.result);
                // Invia il modulo per l'aggiornamento dell'immagine del profilo
                // Puoi utilizzare Ajax per inviare la richiesta al server e aggiornare il database
                // Ad esempio, utilizzando $.ajax() di jQuery
                // Inviare il file al server e gestire l'aggiornamento del database nel tuo view.py
                // Una volta completato l'aggiornamento, puoi mostrare una notifica o reindirizzare l'utente
            };
            reader.readAsDataURL(input.files[0]);
        }
    });

    // Quando l'elemento di modifica viene cliccato
    $('.edit-icon').on('click', function() {
        console.log('click');
        // Simula il click sull'input nascosto per l'upload dell'immagine del profilo
        $('#id_profile_picture').click();
    });
});


// Ottieni il nome utente corrente dal tuo contesto
var nomeUtente = document.getElementById("name-user").textContent;

// Imposta il valore iniziale del campo #id_first_name con il nome utente
document.getElementById('id_first_name').value = nomeUtente;