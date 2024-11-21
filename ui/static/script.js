document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("hexagon-container");

    honeypots.forEach(honeyPot => {
        const hexagon = document.createElement("div");
        hexagon.className = "hexagon";
        hexagon.innerHTML = `
            <div>${honeyPot.name}</div>
            <div>${honeyPot.metric} requests</div>
        `;

        // Add click interaction for future use
        hexagon.addEventListener("click", () => {
            alert(`Viewing details for ${honeyPot.name}`);
        });

        container.appendChild(hexagon);
    });
});
