const videoRequest = document.querySelector('form[data-video-request]');

if (videoRequest) {
  const button = videoRequest.querySelector('button[type="submit"]');
  const status = videoRequest.nextElementSibling;

  videoRequest.addEventListener('submit', async (event) => {
    event.preventDefault();
    button.disabled = true;
    status.hidden = true;

    try {
      const response = await fetch(videoRequest.action, {
        method: 'POST',
        body: new FormData(videoRequest),
        headers: { Accept: 'application/json' },
      });

      if (!response.ok) throw new Error('Video request failed');

      videoRequest.hidden = true;
      status.textContent = 'Request received. Joe will text you the video link.';
    } catch {
      status.textContent = 'Your request could not be sent. Please try again or text Joe.';
    } finally {
      button.disabled = false;
      status.hidden = false;
      status.focus();
    }
  });
}
