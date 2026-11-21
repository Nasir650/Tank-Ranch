document.querySelectorAll('form[data-contact-form], form[data-video-request]').forEach((form) => {
  const button = form.querySelector('button[type="submit"]');
  const confirmation = form.dataset.confirmation
    ? document.getElementById(form.dataset.confirmation)
    : null;
  const status = document.createElement('p');
  status.setAttribute('role', 'status');
  status.setAttribute('tabindex', '-1');
  status.hidden = true;
  form.after(status);

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (button.disabled) return;

    const originalLabel = button.textContent;
    button.disabled = true;
    button.textContent = 'Sending...';
    form.setAttribute('aria-busy', 'true');
    status.hidden = true;

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' },
        signal: AbortSignal.timeout(20000),
      });
      if (!response.ok) throw new Error('Request was not accepted');

      form.hidden = true;
      // Some form layouts set display explicitly, so hide them consistently.
      form.style.display = 'none';
      if (confirmation) {
        confirmation.style.display = 'block';
        confirmation.setAttribute('tabindex', '-1');
        confirmation.setAttribute('role', 'status');
        confirmation.focus();
      } else {
        status.textContent = 'Request received. Joe will text you the video link.';
        status.hidden = false;
        status.focus();
      }
    } catch {
      status.replaceChildren(
        document.createTextNode('Your request could not be sent. Please try again, or email '),
        Object.assign(document.createElement('a'), {
          href: 'mailto:joe@tankandtrench.com',
          textContent: 'joe@tankandtrench.com',
        }),
        document.createTextNode('.'),
      );
      status.hidden = false;
      status.focus();
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
      form.removeAttribute('aria-busy');
    }
  });
});
