document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('header-form');
  const statusEl = document.getElementById('status');
  const resultIds = {
    client_ip: 'client-ip',
    user_id: 'user_id',
    host: 'host',
    proto: 'proto',
    real_ip: 'real_ip'
  };
  const headerFields = [
    'X-Forwarded-For',
    'X-Forwarded-Host',
    'X-Forwarded-Proto',
    'X-Real-IP',
    'X-User-ID'
  ];

  form.addEventListener('submit', async event => {
    event.preventDefault();
    await submitHeaders();
  });

  async function submitHeaders() {
    const headers = new Headers({ Accept: 'application/json' });

    headerFields.forEach(name => {
      const input = document.querySelector(`[name="${name}"]`);
      if (input && input.value.trim()) {
        headers.set(name, input.value.trim());
      }
    });

    try {
      const response = await fetch('/api/headers', {
        method: 'GET',
        headers,
        cache: 'no-store'
      });

      if (!response.ok) {
        statusEl.textContent = `ERROR ${response.status}`;
        return;
      }

      const data = await response.json();
      updateResult(data);
    } catch (error) {
      statusEl.textContent = 'ERROR';
      console.error(error);
    }
  }

  function updateResult(data) {
    statusEl.textContent = data.result || '-';

    Object.entries(resultIds).forEach(([key, elementId]) => {
      const element = document.getElementById(elementId);
      if (element) {
        element.textContent = data[key] || '-';
      }
    });

    headerFields.forEach(name => {
      const element = document.getElementById(`header-${name}`);
      if (element) {
        element.textContent = data.headers[name] || '-';
      }
    });
  }
});
