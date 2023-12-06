$(document).ready(function () {
    $('.header_image').click(function () {
        if ($(this).hasClass('fullscreen')) {
            // Animate header
            gsap.to('.header_image', {
                height: '32%',
                duration: 0.5,
            });
            // Hide fullscreen image
            $(this).removeClass('fullscreen');
        } else {
            // Animate header
            gsap.to('.header_image', {
                height: 'auto',
                duration: 0.5,
            });
            // Show fullscreen image
            $(this).addClass('fullscreen');
        }
    });

    // Aggiungi un click event listener sulla X
    $('.back').click(function (event) {
        // Ferma la propagazione del click event alla parent element
        event.stopPropagation();
        // Anima il contenitore dell'immagine
        gsap.to('.header_image', {
            height: '32%',
            duration: 0.5,
        });
        $('.header_image').removeClass('fullscreen');
        // Vai alla pagina successiva dopo l'animazione
        setTimeout(function () {
            window.location.href = "/";
        }, 500);
    });
});


function goBack() {
    let previousUrl = document.referrer;

    while (previousUrl.includes("/evento/")) {
        history.pushState(null, null, previousUrl);
        previousUrl = document.referrer;
        console.log(previousUrl);
    }

    history.back();
}


$(document).ready(function() {
    $(".partecipants").click(function() {
        $("#friends-list").css('transform', 'translateY(0%)'); // Mostra la lista degli amici
    });

    // Attiva l'evento swipe verso il basso sulla div della lista degli amici
    $("#friends-list").swipe({
        swipeDown: function(event, direction, distance, duration, fingerCount) {
            $("#friends-list").css('transform', 'translateY(100%)'); // Nasconde la lista degli amici
        },
        threshold: 50 // Distanza minima (in pixel) che l'utente deve trascinare prima che l'evento swipe venga attivato
    });

    // (Opzionale) Per nascondere di nuovo la lista quando si clicca al di fuori
    $(document).click(function(event) {
        if (!$(event.target).closest("#friends-list, .partecipants").length) {
            $("#friends-list").css('transform', 'translateY(100%)');
        }
    });
});

$(document).ready(function() {
    // Funzione per aggiornare il totale
    function updateTotal() {
        var totalPrice = 0;
        // Calcola il totale per ciascuna opzione di biglietto
        $('.ticket-option').each(function() {
            var price = parseFloat($(this).find('.price').text().replace('€', '').trim());
            var quantity = parseInt($(this).find('input[type="number"]').val());
            totalPrice += price * quantity;
        });
        // Aggiorna il totale visualizzato
        $('.total-amount span').text(totalPrice.toFixed(2) + '€');
    }

    // Evento di clic sul pulsante diminuisci
    $('.decrease').click(function() {
        var input = $(this).closest('.quantity-selector').find('input[type="number"]');
        var currentValue = parseInt(input.val());
        if (currentValue > 0) {
            input.val(currentValue - 1);
            updateTotal();
        }
    });

    // Evento di clic sul pulsante aumenta
    $('.increase').click(function() {
        var input = $(this).closest('.quantity-selector').find('input[type="number"]');
        var currentValue = parseInt(input.val());
        input.val(currentValue + 1);
        updateTotal();
    });

    // Evento di cambio sul campo di input per catturare cambiamenti manuali
    $('input[type="number"]').change(updateTotal);

    // Aggiorna il totale all'inizio
    updateTotal();
});

document.addEventListener('DOMContentLoaded', function () {
    var purchaseButton = document.querySelector('.purchase-button');
    if (purchaseButton) {
        purchaseButton.addEventListener('click', function () {
            const eventData = document.getElementById('event-data-stripe');
            if (eventData) {
                const token = eventData.getAttribute('data-token');

                fetch('/payment/stripe/checkout_session', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ token: token}),
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.url) {
                        window.location.href = data.url; // Usa l'URL per la redirezione
                    }
                })
                .catch(error => {
                    console.error('Errore di rete:', error);
                });
            }
        });
    }
});

// Funzione helper per ottenere il valore di un cookie per nome
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function() {
    $('.booking').click(function() {
        $('.ticket-purchase-container').toggleClass('show-purchase-section');
        $('.overlay-unclickable').toggleClass('active'); // Attiva/disattiva l'overlay
    });

    // Chiudi la sezione di acquisto quando si clicca sull'overlay
    $('.overlay-unclickable').click(function() {
        $('.ticket-purchase-container').removeClass('show-purchase-section');
        $(this).removeClass('active');
    });
});



