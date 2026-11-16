/**
 * Shared postcard code lookup handler for homepage and /check/ forms.
 * Normalizes O -> 0 and I/L -> 1 in the numeric prefix and routes to /r/<code>/.
 */
(function () {
  const forms = document.querySelectorAll('form[data-postcard-lookup]');
  if (!forms.length) return;

  function normalizePostcardCode(value) {
    const cleaned = String(value || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
    const match = cleaned.match(/^([A-Z]{2})([0-9OIL]+)([A-Z0-9]{4})$/);
    if (!match) return null;
    const [, state, serial, suffix] = match;
    const normalizedSerial = serial.replace(/O/g, '0').replace(/[IL]/g, '1');
    return state + normalizedSerial + '-' + suffix.toLowerCase();
  }

  function showNotFound(statusEl) {
    statusEl.innerHTML =
      'We couldn\u2019t find that code - <a href="sms:+16175798197">text Joe at 617-579-8197</a>.';
  }

  async function lookupCode(rawValue, statusEl, buttonEl) {
    const code = normalizePostcardCode(rawValue);
    if (!code) {
      showNotFound(statusEl);
      return;
    }

    const url = '/r/' + code + '/';
    if (buttonEl) buttonEl.disabled = true;
    statusEl.textContent = 'Looking up your results\u2026';

    try {
      const response = await fetch(url, { cache: 'no-store' });
      if (response.ok) {
        const html = await response.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const destination = doc.querySelector('a[data-postcard-result]')?.getAttribute('href');
        if (destination && /^\/check\/[a-z0-9-]+\/$/.test(destination)) {
          window.location.assign(destination);
          return;
        }
        window.location.assign(url);
        return;
      }
      showNotFound(statusEl);
    } catch {
      showNotFound(statusEl);
    } finally {
      if (buttonEl) buttonEl.disabled = false;
    }
  }

  forms.forEach((form) => {
    const input = form.querySelector('input[name="c"]');
    const statusEl = form.querySelector('[role="status"]');
    const buttonEl = form.querySelector('button[type="submit"]');
    if (!input || !statusEl) return;

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      lookupCode(input.value, statusEl, buttonEl);
    });

    if (form.hasAttribute('data-accept-query')) {
      const suppliedCode = new URLSearchParams(window.location.search).get('c');
      if (suppliedCode) {
        input.value = suppliedCode;
        lookupCode(suppliedCode, statusEl, buttonEl);
      }
    }
  });
})();
