// Seleziona tutti gli elementi della classe "category"
const categories = document.querySelectorAll('.category');
const filterBtn = document.querySelector('.filter_btn');
var selectedCategories = [];

// Aggiungi un gestore di eventi a ciascun elemento
categories.forEach(category => {
  // Aggiungi un gestore di eventi per il clic
  category.addEventListener('click', event => {
    // Impedisci il comportamento predefinito del link
    event.preventDefault();

    // Aggiungi o rimuovi la classe "active" dall'elemento cliccato
    category.classList.toggle('active');

    // Se la categoria è attiva, aggiungi gli stili CSS
    if (category.classList.contains('active')) {
      category.style.backgroundColor = 'var(--colore_secondario)';
      category.style.border = '1px solid var(--colore_primario)';
      category.style.padding = '4px 17px 7px 17px';
      category.style.boxShadow = '0px 0.5px 1.2px rgba(0, 0, 0, 0.011), 0px 1.1px 2.7px rgba(0, 0, 0, 0.016), 0px 1.8px 4.6px rgba(0, 0, 0, 0.019), 0px 2.7px 6.9px rgba(0, 0, 0, 0.022), 0px 3.9px 10px rgba(0, 0, 0, 0.025), 0px 5.5px 14.2px rgba(0, 0, 0, 0.028), 0px 7.8px 20.1px rgba(0, 0, 0, 0.031), 0px 11.3px 29.2px rgba(0, 0, 0, 0.034), 0px 17.4px 45px rgba(0, 0, 0, 0.039), 0px 31px 80px rgba(0, 0, 0, 0.05)';
      category.style.transform = 'scale(1.04)';

      filterBtn.innerHTML = '<a href="#"><svg viewBox="0 0 512 512" width="24" height="24" style="vertical-align: middle; " xmlns="http://www.w3.org/2000/svg"> <defs></defs><path d="M 55.214 95.822 C 60.471 84.671 71.622 77.582 83.968 77.582 L 428.07 77.582 C 440.417 77.582 451.568 84.671 456.825 95.822 C 462.082 106.974 460.489 120.117 452.683 129.675 L 306.997 307.7 L 206.629 215.966 L 89.457 128.801 C 81.73 119.323 49.877 106.894 55.214 95.822 Z" style="fill: rgb(255, 255, 255);"></path><rect x="60.082" y="54.826" width="38" height="632.966" style="stroke: rgb(0, 0, 0); fill: rgb(255, 255, 255); stroke-opacity: 0;" transform="matrix(0.62528, -0.780401, 0.786869, 0.617206, -85.803688, 88.685905)" rx="19" ry="19"></rect><path d="M 205.885 288.5 L 306.997 367.811 L 306.997 408.939 C 306.997 418.577 301.581 427.419 292.899 431.72 C 284.217 436.021 273.941 435.145 266.215 429.33 L 215.237 391.097 C 208.785 386.318 205.041 378.751 205.041 370.706 L 205.885 288.5 Z" style="fill: rgb(255, 255, 255);"></path></svg ></a>';
    }
    // Se la categoria non è attiva, rimuovi gli stili CSS
    else {
      category.style.backgroundColor = 'rgba(30, 39, 92, 0.5)';
      category.style.border = 'none';
      category.style.padding = '5px 18px 8px 18px';
      category.style.boxShadow = 'none';
      category.style.transform = 'none';
    }

    const activeCategories = document.querySelectorAll('.category.active');
    if (activeCategories.length === 0) {
      filterBtn.innerHTML = '<a href="#"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="20" height="20" style="vertical-align: middle;"><!--! Font Awesome Pro 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. --><path fill="#FFFFFF" d="M3.9 54.9C10.5 40.9 24.5 32 40 32H472c15.5 0 29.5 8.9 36.1 22.9s4.6 30.5-5.2 42.5L320 320.9V448c0 12.1-6.8 23.2-17.7 28.6s-23.8 4.3-33.5-3l-64-48c-8.1-6-12.8-15.5-12.8-25.6V320.9L9 97.3C-.7 85.4-2.8 68.8 3.9 54.9z"/></svg></a>';
    }


  });
});

$(document).ready(function () {
  $('.category').on('click', function () {
    // Recupera gli id delle categorie attive
    var active_categories = $('.category.active').map(function () {
      return $(this).data('id');
    }).get();

    // Effettua la chiamata JSON
    $.ajax({
      url: '/eventi/',
      type: 'GET',
      dataType: 'json',
      data: {
        categories: active_categories
      },
      traditional: true,
      success: function (data) {
        console.log(data);
        $('#filtered_data').html(data.events);
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown);
      }
    });
  });
});