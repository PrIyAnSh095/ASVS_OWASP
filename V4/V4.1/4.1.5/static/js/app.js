const SECRET_KEY = 'supersecretsharedkey';

function encodeUTF8(str) {
  return new TextEncoder().encode(str);
}

async function calculateSignature(body) {
  const key = await window.crypto.subtle.importKey(
    'raw',
    encodeUTF8(SECRET_KEY),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const signature = await window.crypto.subtle.sign('HMAC', key, body);
  return Array.from(new Uint8Array(signature)).map(b => b.toString(16).padStart(2, '0')).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  const endpointEl = document.getElementById('endpoint');
  const secretEl = document.getElementById('secret-message');
  const amountEl = document.getElementById('amount');
  const recipientEl = document.getElementById('recipient');
  const signatureEl = document.getElementById('signature');
  const statusCodeEl = document.getElementById('status-code');
  const displaySignatureEl = document.getElementById('display-signature');
  const requestBodyEl = document.getElementById('request-body');
  const verificationResultEl = document.getElementById('verification-result');
  const resultEl = document.getElementById('result');
  const responseBodyEl = document.getElementById('response-body');
  const explanationEl = document.getElementById('explanation');
  const generateButton = document.getElementById('generate-button');
  const tamperButton = document.getElementById('tamper-button');
  const sendButton = document.getElementById('send-button');

  function buildPayload() {
    return {
      message: secretEl.value,
      amount: Number(amountEl.value),
      recipient: recipientEl.value
    };
  }

  function updateRequestBody(payload) {
    const text = JSON.stringify(payload, null, 2);
    requestBodyEl.textContent = text;
    return text;
  }

  async function generate() {
    const payload = buildPayload();
    const bodyText = updateRequestBody(payload);
    const body = encodeUTF8(bodyText);
    const signature = await calculateSignature(body);
    signatureEl.value = signature;
    displaySignatureEl.textContent = signature;
    verificationResultEl.textContent = 'Generated';
    resultEl.textContent = '-';
    responseBodyEl.textContent = '-';
    statusCodeEl.textContent = '-';
    explanationEl.textContent = 'Signature generated for the current payload. Send the request to verify it.';
  }

  function tamper() {
    amountEl.value = Number(amountEl.value) + 1;
    const payload = buildPayload();
    updateRequestBody(payload);
    verificationResultEl.textContent = 'Tampered';
    resultEl.textContent = 'FAIL';
    explanationEl.textContent = 'Payload modified after signature generation. Secure server should reject this request.';
  }

  async function sendRequest() {
    const payload = buildPayload();
    const bodyText = requestBodyEl.textContent.trim() || JSON.stringify(payload);
    const signature = signatureEl.value.trim();
    const endpoint = endpointEl.value;
    const url = endpoint;

    if (!signature) {
      explanationEl.textContent = 'No signature present. Secure server should reject unsigned requests.';
    }

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Signature': signature
      },
      body: bodyText
    });

    const text = await response.text();
    statusCodeEl.textContent = response.status;
    displaySignatureEl.textContent = signature || '<missing>';
    requestBodyEl.textContent = bodyText;
    responseBodyEl.textContent = text || '<empty response>';
    const valid = response.status === 200;
    verificationResultEl.textContent = valid ? 'passed' : 'failed';
    resultEl.textContent = valid ? 'PASS' : 'FAIL';
    explanationEl.textContent = valid
      ? 'The server accepted the signed request.'
      : 'The server rejected the request due to missing or invalid signature.';
  }

  generateButton.addEventListener('click', generate);
  tamperButton.addEventListener('click', tamper);
  sendButton.addEventListener('click', sendRequest);

  generate();
});
