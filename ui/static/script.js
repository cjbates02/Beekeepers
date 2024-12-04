document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById('metrics-container');

    websocket = io('http://127.0.0.1:5050');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
    });

    websocket.on('prom_data', (data) => { 
        const metricData = data.data;
        populatePods(metricData);
    });

    function populatePods(metricData) {
        container.innerHTML = ''; // Clear the container before populating
        Object.keys(metricData).forEach(key => {
            const pod = metricData[key];
            const hexagon = document.createElement("div");
            hexagon.className = "hexagon";

            hexagon.innerHTML = `
                <div class="hex-content">
                    <h3>${key}</h3>
                    <p>CPU: ${pod.cpu_usage_percentage}% / ${pod.cpu_limit}</p>
                    <p>Memory: ${pod.memory_usage_percentage}% / ${pod.memory_limit}</p>
                    <p>Status: ${pod.status}</p>
                </div>
                <div class="hex-buttons">
                    <button class="action-button start" onclick="handleAction('${key}', 'start')">
                        <i class="fas fa-play"></i>
                    </button>
                    <button class="action-button stop" onclick="handleAction('${key}', 'stop')">
                        <i class="fas fa-stop"></i>
                    </button>
                    <button class="action-button restart" onclick="handleAction('${key}', 'restart')">
                        <i class="fas fa-sync"></i>
                    </button>
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
