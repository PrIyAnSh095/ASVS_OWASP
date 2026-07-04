document.addEventListener('DOMContentLoaded', () => {
  const responseTypeEl = document.getElementById('response-type');
  const responseTypeResultEl = document.getElementById('response-type-result');
  const declaredLengthEl = document.getElementById('declared-length');
  const actualLengthEl = document.getElementById('actual-length');
  const matchResultEl = document.getElementById('match-result');
  const statusResultEl = document.getElementById('status-result');
  const responseBodyEl = document.getElementById('response-body');
  const responseHeadersEl = document.getElementById('response-headers');
  const explanationEl = document.getElementById('explanation');
  const generateButton = document.getElementById('generate-button');
  const analyzeButton = document.getElementById('analyze-button');

  async function analyze() {
    const responseType = responseTypeEl.value;
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: responseType })
    });
    const json = await response.json();

    responseTypeResultEl.textContent = json.response_type;
    declaredLengthEl.textContent = json.declared_length;
    actualLengthEl.textContent = json.body_length;
    matchResultEl.textContent = json.matches ? 'YES' : 'NO';
    statusResultEl.textContent = json.status;
    responseBodyEl.textContent = json.body;
    responseHeadersEl.textContent = `Content-Length: ${json.declared_length}\nContent-Type: ${json.content_type}\n\n(Declared: ${json.declared_length}, Actual: ${json.body_length})`;
    explanationEl.textContent = json.message;
  }

  async function generate() {
    const responseType = responseTypeEl.value;
    const response = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: responseType })
    });

    const text = await response.text();
    const contentLength = response.headers.get('content-length') || '-';
    const contentType = response.headers.get('content-type') || '-';

    responseTypeResultEl.textContent = responseType;
    declaredLengthEl.textContent = contentLength;
    actualLengthEl.textContent = text.length;
    const matches = parseInt(contentLength, 10) === text.length;
    matchResultEl.textContent = matches ? 'YES' : 'NO';
    statusResultEl.textContent = matches ? 'PASS' : 'FAIL';
    responseBodyEl.textContent = text;
    responseHeadersEl.textContent = `Content-Length: ${contentLength}\nContent-Type: ${contentType}\n\n(Declared: ${contentLength}, Actual: ${text.length})`;
    explanationEl.textContent = matches
      ? 'Content-Length matches actual body length. Response is RFC-compliant.'
      : 'Content-Length does NOT match actual body length! Response violates RFC 9112.';
  }

  generateButton.addEventListener('click', generate);
  analyzeButton.addEventListener('click', analyze);
  analyze();
});
