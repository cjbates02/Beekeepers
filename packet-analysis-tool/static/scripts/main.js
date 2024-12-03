document.addEventListener("DOMContentLoaded", () => {
    const dataFeedBody = document.getElementById('data-feed-body');
    const dataFeedStateContainer = document.getElementById('data-feed-state-container');

    let dataFeedEnabled = true;

    websocket = io('http://127.0.0.1:5000');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
        updateDataFeedStateIcon();
    });

    websocket.on('packet', (data) => { 
        const packet = data.packet;
        console.log(packet);
        if (dataFeedEnabled) {
            addPacketToFeed(packet);
        }
    });

    dataFeedStateContainer.addEventListener('click', () => {
        dataFeedEnabled = !dataFeedEnabled;
        updateDataFeedStateIcon();
    });

    function addPacketToFeed(packet) {
        const row = document.createElement('div');
        row.classList.add('data-feed-row');

        const srcIpSpan = wrapDivAroundContent(packet.ip_src, 'source-ip');
        const dstIpSpan = wrapDivAroundContent(packet.ip_dst, 'dest-ip');
        const srcPortSpan = wrapDivAroundContent(packet.port_src, 'source-port');
        const dstPortSpan = wrapDivAroundContent(packet.port_dst, 'dest-port');

        row.appendChild(srcIpSpan);
        row.appendChild(dstIpSpan);
        row.appendChild(srcPortSpan);
        row.appendChild(dstPortSpan);

        dataFeedBody.insertBefore(row, dataFeedBody.firstChild);
    }

    function wrapDivAroundContent(content, className) {
        const div = document.createElement('div');
        div.classList.add(className);
        div.innerText = content;
        return div;
    }

    function updateDataFeedStateIcon() {
        dataFeedStateContainer.innerHTML = '';

        const dataFeedStateIcon = document.createElement('img');
        const iconName = dataFeedEnabled ? iconPause : iconPlay;

        dataFeedStateIcon.src = getIconPath(iconName);
        dataFeedStateIcon.title = iconName;
        dataFeedStateIcon.classList.add('icon');
        dataFeedStateContainer.appendChild(dataFeedStateIcon);
    }

    function getIconPath(iconName) {
        return `${iconDirectory}${iconName}.svg`;
    }

});