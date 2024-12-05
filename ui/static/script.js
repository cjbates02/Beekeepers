document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('metrics-container');
    const loader = document.getElementById('loader');

    websocket = io('http://127.0.0.1:5050');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
    });

    websocket.on('prom_data', (data) => { 
        const metricData = data.data;
        loader.classList.add('hidden');
        populatePods(metricData);
    });

    function populatePods(metricData) {
        container.innerHTML = ''; 
        Object.keys(metricData).forEach(key => {
            const pod = metricData[key];
            const hexagon = document.createElement("div");
            hexagon.className = "hexagon";
            hexagon.innerHTML = `
                <div class="hex-content-container">
                    <p class="pod-title">${key}</p>
                    <div class="hex-content">
                        <div class="pod-metric"><span>CPU: </span><span class="pod-metric-value">${(pod.cpu_usage * 100).toFixed(2)}%</span></div>
                        <div class="pod-metric"><span>Memory: </span><span class="pod-metric-value">${(pod.memory_usage / 1024 ** 3).toFixed(2)}Gb</span></div>
                        <div class="pod-metric"><span>Status: </span><span class="pod-metric-value">${(pod.status) ? 'Up' : 'Down'}</span></div>
                    </div>
                </div>
            `;

            

            container.appendChild(hexagon);
        });
    }

    window.handleAction = (honeypot, action) => {
        alert(`Performing '${action}' action on ${honeypot}`);
        // Send action to the server if needed
    };
});
