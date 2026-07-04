document.addEventListener('DOMContentLoaded', () => {
    const executeBtn = document.getElementById('executeBtn');
    if (executeBtn) {
        executeBtn.addEventListener('click', async () => {
            const query = document.getElementById('query').value;
            const responseViewer = document.getElementById('responseViewer');
            const statusIndicator = document.getElementById('statusIndicator');
            const depthIndicator = document.getElementById('depthIndicator');
            const costIndicator = document.getElementById('costIndicator');
            
            responseViewer.textContent = 'Executing...';
            
            try {
                const res = await fetch('/graphql', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await res.json();
                responseViewer.textContent = JSON.stringify(data, null, 2);
                
                if (res.ok && !data.errors) {
                    statusIndicator.textContent = 'Status: PASS';
                    statusIndicator.className = 'pass';
                } else {
                    statusIndicator.textContent = 'Status: FAIL';
                    statusIndicator.className = 'fail';
                }

                if (data.extensions) {
                    if (depthIndicator) depthIndicator.textContent = 'Depth: ' + (data.extensions.depth || 'N/A');
                    if (costIndicator) costIndicator.textContent = 'Cost: ' + (data.extensions.cost || 'N/A');
                }

            } catch (err) {
                responseViewer.textContent = 'Network Error: ' + err.message;
                statusIndicator.textContent = 'Status: ERROR';
                statusIndicator.className = 'fail';
            }
        });
    }
});
