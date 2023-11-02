$(".notification-action.accept").on("click", function () {
    const notificationId = $(this).closest(".notification-actions").data("notification-id");
    const $notification = $(this).closest(".notification");

    $.post("accept_friend_request", { notification_id: notificationId }, function (response) {
        if (response.success) {
            $notification.addClass("erase-out");
            setTimeout(function () {
                $notification.remove();
                // Verifica se ci sono ancora notifiche nella lista
                if ($(".notifications-list .notification").length === 0) {
                    // Aggiunge il messaggio "Nessuna nuova notifica"
                    $(".notifications-list").append('<div id="no-notifications">Nessuna nuova notifica.</div>');
                }
            }, 200); // 200ms è la durata dell'animazione
        } else {
            // Gestisci l'errore
        }
    });
});



