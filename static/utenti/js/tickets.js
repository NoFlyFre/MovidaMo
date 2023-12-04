function zoomQRCode(ticketId) {
    var qrImg = document.getElementById('qr-' + ticketId);
    var overlay = document.getElementById('qr-overlay');
  
    qrImg.style.transform = 'translate(-50%, -50%) scale(2)'; // Zoom in
    qrImg.classList.add('zoomed-qr');
    overlay.style.display = 'block';
  }
  
  function closeZoomQRCode() {
    var zoomedQrImgs = document.querySelectorAll('.zoomed-qr');
    var overlay = document.getElementById('qr-overlay');
  
    zoomedQrImgs.forEach(function(img) {
      img.style.transform = 'translate(-50%, -50%) scale(1)'; // Zoom out
      img.classList.remove('zoomed-qr');
    });
    overlay.style.display = 'none';
  }