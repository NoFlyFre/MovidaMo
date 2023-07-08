function handleImageSelect(event) {
    const input = event.target;
    
    if (input.files && input.files[0]) {
      const reader = new FileReader();

      // Legge il file immagine e aggiorna l'anteprima dell'immagine
      reader.onload = function(e) {
        $('#image-real').attr('src', e.target.result);
                // Invia il modulo per l'aggiornamento dell'immagine del profilo
                // Puoi utilizzare Ajax per inviare la richiesta al server e aggiornare il database
                // Ad esempio, utilizzando $.ajax() di jQuery
                // Inviare il file al server e gestire l'aggiornamento del database nel tuo view.py
                // Una volta completato l'aggiornamento, puoi mostrare una notifica o reindirizzare l'utente
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

  // Aggiunge un listener all'input file per gestire l'evento di selezione dell'immagine
  const imageInput = document.getElementById('id_image');
  imageInput.addEventListener('change', handleImageSelect);