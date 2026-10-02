/* ==========================================================
   BANNER DE COOKIES — Más que Magos
   Pegar este <script> justo antes de </body> en TODAS las
   páginas del sitio (home, empresas, ayuntamientos, celebraciones,
   y sus versiones CAT/EN — ajustando los textos si hace falta).
========================================================== */
(function () {
  var CONSENT_KEY = 'mqm_cookie_consent';
  var existing = localStorage.getItem(CONSENT_KEY);

  // Si ya hay una decisión guardada, no mostramos nada más.
  if (existing) {
    window.mqmCookieConsent = existing; // 'accepted' o 'rejected'
    return;
  }

  var banner = document.createElement('div');
  banner.id = 'mqm-cookie-banner';
  banner.style.cssText = [
    'position:fixed', 'left:16px', 'right:16px', 'bottom:16px',
    'max-width:560px', 'margin:0 auto', 'z-index:99999',
    'background:#1A1005', 'color:#FFF8EE',
    'border:1px solid rgba(196,151,61,.35)', 'border-radius:16px',
    'padding:20px 22px', 'box-shadow:0 10px 40px rgba(0,0,0,.35)',
    'font-family:\'DM Sans\',sans-serif', 'font-size:14px', 'line-height:1.6'
  ].join(';');

  banner.innerHTML =
    '<p style="margin:0 0 14px;color:rgba(255,248,238,.85)">' +
      'Usamos cookies propias y de terceros para mejorar tu experiencia y, si las aceptas, para medir el tráfico y las campañas de publicidad. ' +
      '<a href="/politica-cookies.html" style="color:#D4A94E;text-decoration:underline">Más información</a>.' +
    '</p>' +
    '<div style="display:flex;gap:10px;flex-wrap:wrap">' +
      '<button id="mqm-cookie-accept" style="flex:1;min-width:120px;background:#C4973D;color:#1a1005;border:none;padding:11px 18px;border-radius:100px;font-weight:700;font-size:13px;cursor:pointer">Aceptar todas</button>' +
      '<button id="mqm-cookie-reject" style="flex:1;min-width:120px;background:transparent;color:#FFF8EE;border:1px solid rgba(255,248,238,.35);padding:11px 18px;border-radius:100px;font-weight:600;font-size:13px;cursor:pointer">Rechazar</button>' +
    '</div>';

  document.body.appendChild(banner);

  function setConsent(value) {
    localStorage.setItem(CONSENT_KEY, value);
    window.mqmCookieConsent = value;
    banner.remove();
    // Avisamos al resto de la página por si algún script (GA, Ads...)
    // quiere reaccionar al consentimiento sin recargar.
    document.dispatchEvent(new CustomEvent('mqmCookieConsentChanged', { detail: value }));
  }

  document.getElementById('mqm-cookie-accept').addEventListener('click', function () {
    setConsent('accepted');
  });
  document.getElementById('mqm-cookie-reject').addEventListener('click', function () {
    setConsent('rejected');
  });
})();

/* ==========================================================
   CÓMO USARLO CON GOOGLE ANALYTICS / GOOGLE ADS (opcional):

   Si en el futuro añades Google Analytics o quieres que el pixel
   de conversión de Ads solo se cargue tras aceptar cookies, envuelve
   esa carga así, en vez de ponerla suelta en el <head>:

   if (window.mqmCookieConsent === 'accepted') {
     cargarGoogleAnalytics();
   } else {
     document.addEventListener('mqmCookieConsentChanged', function(e){
       if (e.detail === 'accepted') cargarGoogleAnalytics();
     });
   }

   El tag de Google Ads (AW-18179083545) que ya tienes en todas las
   páginas actualmente se carga siempre, sin esperar consentimiento.
   Si quieres que respete el banner también, dímelo y te lo adapto.
========================================================== */
