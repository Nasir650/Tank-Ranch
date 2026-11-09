document.querySelectorAll('form[data-email-subject]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const subject = encodeURIComponent(form.dataset.emailSubject);
    const fields = new FormData(form);
    const body = Array.from(fields, ([label, value]) => label + ': ' + value.trim()).join('\r\n');
    window.location.href = form.getAttribute('action') + '?subject=' + subject + '&body=' + encodeURIComponent(body);
  });
});
