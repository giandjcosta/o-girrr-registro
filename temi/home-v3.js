/* O Girrr Miami Nights Home V3: solo demo, 17/11/2026.
   Nessun dato reale, sessione, database o navigazione della produzione. */
(() => {
  "use strict";
  const root = document.documentElement;
  const photo = document.getElementById("hero-photo");
  const toggle = document.getElementById("mode-toggle");
  const label = document.getElementById("mode-label");
  if (!photo || !toggle || !label) return;
  const sunset = "https://images.unsplash.com/photo-1605723517503-3cadb5818a0c?auto=format&fit=crop&w=2000&q=82";
  const nightlife = "https://images.pexels.com/photos/11457824/pexels-photo-11457824.jpeg?auto=compress&cs=tinysrgb&w=1920";
  let night = false;
  function render() {
    root.dataset.night = String(night);
    photo.src = night ? nightlife : sunset;
    toggle.setAttribute("aria-pressed", String(night));
    toggle.setAttribute("aria-label", night ? "Torna al tramonto" : "Attiva la modalità notturna");
    toggle.title = night ? "Mostra il tramonto" : "Mostra Ocean Drive di notte";
    label.textContent = night ? "OCEAN DRIVE" : "TRAMONTO";
  }
  photo.addEventListener("error", () => {
    // 17/11/2026: il fallback CSS resta visibile anche se la CDN fotografica è offline.
    photo.style.visibility = "hidden";
  });
  photo.addEventListener("load", () => { photo.style.visibility = "visible"; });
  toggle.addEventListener("click", () => { night = !night; render(); });
  render();
})();
