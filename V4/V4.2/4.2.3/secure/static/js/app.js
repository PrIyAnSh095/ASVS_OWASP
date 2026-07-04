/**
 * ASVS 4.2.3 Lab - Frontend JavaScript
 * Handles interactive testing of HTTP/2 header validation
 */

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    const testForm = document.getElementById('testForm');
    if (testForm) {
        testForm.addEventListener('submit', function(e) {
            e.preventDefault();
            sendTestRequest();
        });
    }
}

function addHeader() {
    const headersList = document.getElementById('headersList');
    const newGroup = document.createElement('div');
    newGroup.className = 'header-input-group';
    newGroup.innerHTML = `
        <input type="text" class="header-name" placeholder="Header Name" value="">
        <input type="text" class="header-value" placeholder="Header Value" value="">
        <button type="button" class="btn-remove" onclick="removeHeader(this)">Remove</button>
    `;
    headersList.appendChild(newGroup);
}

function removeHeader(button) {
    button.parentElement.remove();
}

function sendTestRequest() {
    const protocol = document.getElementById('protocol').value;
    const body = document.getElementById('body').value;
    const responseSection = document.getElementById('responseSection');
    
    // Gather headers
    const headerGroups = document.querySelectorAll('.header-input-group');
    const headers = {};
    
    headerGroups.forEach(group => {
        const name = group.querySelector('.header-name').value.trim();
        const value = group.querySelector('.header-value').value.trim();
        if (name && value) {
            headers[name] = value;
        }
    });

    // Prepare request
    const url = new URL('/api/test?protocol=' + protocol, window.location.href);
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...headers
        }
    };

    if (body) {
        try {
            JSON.parse(body);
            options.body = body;
        } catch (e) {
            alert('Invalid JSON in request body: ' + e.message);
            return;
        }
    }

    // Send request and display response
    fetch(url, options)
        .then(response => {
            const status = response.status;
            return response.json().then(data => {
                displayResponse(data, status, headers);
            });
        })
        .catch(error => {
            displayError('Request failed: ' + error.message);
        });
}

function displayResponse(data, status, headers) {
    const responseSection = document.getElementById('responseSection');
    const responsePretty = document.getElementById('responsePretty');
    const responseRaw = document.getElementById('responseRaw');

    // Format pretty response
    const prettyResponse = {
        'HTTP Status': status,
        'Response Data': data,
        'Sent Headers': headers,
        'Timestamp': new Date().toISOString()
    };

    responsePretty.textContent = JSON.stringify(prettyResponse, null, 2);

    // Format raw response (simulated HTTP response)
    const statusText = status === 200 ? 'OK' : 
                      status === 400 ? 'Bad Request' : 
                      'Unknown';
    
    const rawResponse = `HTTP/2 ${status} ${statusText}
content-type: application/json
content-length: ${JSON.stringify(data).length}

${JSON.stringify(data, null, 2)}`;

    responseRaw.textContent = rawResponse;

    // Show response section and switch to pretty tab
    responseSection.style.display = 'block';
    switchTab('response-pretty', document.querySelector('.tab-btn.active'));
    
    // Scroll to response
    setTimeout(() => {
        responseSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function displayError(message) {
    const responseSection = document.getElementById('responseSection');
    const responsePretty = document.getElementById('responsePretty');
    
    responsePretty.textContent = `Error: ${message}`;
    responseSection.style.display = 'block';
    responseSection.scrollIntoView({ behavior: 'smooth' });
}

function switchTab(tabId, button) {
    // Remove active class from all buttons and tabs
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    
    // Add active class to clicked button and corresponding tab
    button.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

/**
 * Utility function to format JSON for display
 */
function formatJSON(data) {
    try {
        return JSON.stringify(data, null, 2);
    } catch (e) {
        return String(data);
    }
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

/**
 * Export test results
 */
function exportResults() {
    const responsePretty = document.getElementById('responsePretty').textContent;
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(responsePretty));
    element.setAttribute('download', 'asvs-4-2-3-test-results.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

/**
 * Load preset test cases
 */
function loadTestCase(testName) {
    const testCases = {
        'transfer-encoding': {
            protocol: 'http2',
            headers: {
                'Transfer-Encoding': 'chunked'
            }
        },
        'connection': {
            protocol: 'http2',
            headers: {
                'Connection': 'close'
            }
        },
        'keep-alive': {
            protocol: 'http2',
            headers: {
                'Keep-Alive': 'timeout=5, max=100'
            }
        },
        'upgrade': {
            protocol: 'http2',
            headers: {
                'Upgrade': 'h2c'
            }
        },
        'proxy-connection': {
            protocol: 'http2',
            headers: {
                'Proxy-Connection': 'Keep-Alive'
            }
        },
        'trailer': {
            protocol: 'http2',
            headers: {
                'Trailer': 'X-Custom-Trailer'
            }
        },
        'multiple-forbidden': {
            protocol: 'http2',
            headers: {
                'Transfer-Encoding': 'chunked',
                'Connection': 'close',
                'Keep-Alive': 'timeout=5'
            }
        },
        'valid': {
            protocol: 'http2',
            headers: {
                'Accept': 'application/json',
                'User-Agent': 'ASVS-Lab-Test'
            }
        }
    };

    const testCase = testCases[testName];
    if (!testCase) return;

    // Set protocol
    document.getElementById('protocol').value = testCase.protocol;

    // Clear and populate headers
    const headersList = document.getElementById('headersList');
    headersList.innerHTML = '';

    Object.entries(testCase.headers).forEach(([name, value]) => {
        const group = document.createElement('div');
        group.className = 'header-input-group';
        group.innerHTML = `
            <input type="text" class="header-name" placeholder="Header Name" value="${name}">
            <input type="text" class="header-value" placeholder="Header Value" value="${value}">
            <button type="button" class="btn-remove" onclick="removeHeader(this)">Remove</button>
        `;
        headersList.appendChild(group);
    });
}
