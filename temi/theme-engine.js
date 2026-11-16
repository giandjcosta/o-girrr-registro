/* O Girrr — Theme Engine (16/11/2026). Layer indipendente da Lega/Stadio. */
(function (global) {
  "use strict";
  const themes = Object.freeze({
    "vice-city": Object.freeze({
      name: "Vice City Edition",
      start: "2026-11-18T00:00:00+01:00",
      end: "2026-11-21T00:00:00+01:00"
    })
  });
  const root = document.documentElement;
  function assertTheme(id) {
    if (!Object.prototype.hasOwnProperty.call(themes, id)) throw Error("Tema sconosciuto");
  }
  function apply(id) {
    if (id === null) root.removeAttribute("data-event-theme");
    else {
      assertTheme(id);
      root.setAttribute("data-event-theme", id);
    }
    global.dispatchEvent(new CustomEvent("ogirrr:theme-change", {detail:{id}}));
  }
  function preview(id) { apply(id); }
  function clearPreview() { apply(null); }
  function activateScheduled(now) {
    const at = now instanceof Date ? now : new Date();
    const active = Object.keys(themes).find(id => {
      const t = themes[id];
      return at >= new Date(t.start) && at < new Date(t.end);
    });
    apply(active || null);
    return active || null;
  }
  global.OGirrrTheme = Object.freeze({themes, preview, clearPreview, activateScheduled});
})(window);
