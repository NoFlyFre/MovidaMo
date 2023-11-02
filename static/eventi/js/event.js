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
            console.log("Hai cliccato per tornare alla visualizzazione normale");
        } else {
            // Animate header
            gsap.to('.header_image', {
                height: 'auto',
                duration: 0.5,
            });
            // Show fullscreen image
            $(this).addClass('fullscreen');
            console.log("Hai cliccato per espandere l'immagine a schermo intero");
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

