function selectFile(filename) {
    document.getElementById('sourceFile').value = filename;
    document.getElementById('filenameInput').value = filename;
}

function fetchHeaders() {
    const filename = document.getElementById('filenameInput').value;
    const source = document.getElementById('sourceFile').value;
    const outputEl = document.getElementById('headersOutput');
    
    outputEl.textContent = "Fetching headers from server...";
    
    // Construct target URL
    const url = `/download?source=${encodeURIComponent(source)}&filename=${encodeURIComponent(filename)}`;
    
    fetch(url, {
        method: 'GET'
    })
    .then(response => {
        let headersText = `HTTP/1.1 ${response.status} ${response.statusText}\n`;
        
        // Iterate and compile headers
        for (let pair of response.headers.entries()) {
            headersText += `${pair[0]}: ${pair[1]}\n`;
        }
        
        // Show first 200 bytes of response body just to verify
        return response.blob().then(blob => {
            headersText += `\n[Response Body Size: ${blob.size} bytes]`;
            outputEl.textContent = headersText;
        });
    })
    .catch(error => {
        outputEl.textContent = `Error performing header test: ${error.message}\nMake sure container is running.`;
    });
}
