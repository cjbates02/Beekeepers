document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("hexagon-container");

    // honeypots.forEach(honeyPot => {
    //     const hexagon = document.createElement("div");
    //     hexagon.className = "hexagon";
    //     hexagon.innerHTML = `
    //         <div>${honeyPot.name}</div>
    //         <div>${honeyPot.metric} requests</div>
    //     `;

    //     // Add click interaction for future use
    //     hexagon.addEventListener("click", () => {
    //         alert(`Viewing details for ${honeyPot.name}`);
    //     });

    //     container.appendChild(hexagon);
    // });

    websocket = io('http://127.0.0.1:5050');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
    });

    websocket.on('prom_data', (data) => { 
        const metricData = data.data;
        console.log(metricData);
        // call function to populate pod metric data here
    });
});
