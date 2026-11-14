// Firefox usa un profilo NSS con la CA del proxy, senza disattivare TLS.
const fs = require('fs'), os = require('os'), path = require('path');
const pw = require('playwright');
async function browser(motore) {
  if (motore !== 'firefox') return pw[motore].launch(motore === 'webkit' && process.env.WEBKIT_PATH ? { executablePath: process.env.WEBKIT_PATH } : {});
  const sorgente = process.env.FIREFOX_CERT_PROFILE;
  if (!sorgente || !fs.existsSync(path.join(sorgente, 'cert9.db'))) throw new Error('FIREFOX_CERT_PROFILE deve indicare il profilo NSS del certificato del proxy');
  const contesti = new Set();
  return {
    async newContext(opzioni = {}) {
      const cartella = fs.mkdtempSync(path.join(os.tmpdir(), 'girrr-firefox-'));
      for (const f of ['cert9.db', 'key4.db', 'pkcs11.txt']) if (fs.existsSync(path.join(sorgente, f))) fs.copyFileSync(path.join(sorgente, f), path.join(cartella, f));
      const o = { ...opzioni }; delete o.isMobile; delete o.defaultBrowserType;
      const c = await pw.firefox.launchPersistentContext(cartella, { ...o, firefoxUserPrefs: { 'security.enterprise_roots.enabled': true } });
      contesti.add(c);
      const chiudi = c.close.bind(c);
      c.close = async () => { await chiudi(); contesti.delete(c); fs.rmSync(cartella, { recursive: true, force: true }); };
      return c;
    },
    async close() { for (const c of [...contesti]) await c.close(); }
  };
}
module.exports = { browser };
