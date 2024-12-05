document.addEventListener("DOMContentLoaded", () => {
    const dataFeedBody = document.getElementById('data-feed-body');
    const dataFeedStateContainer = document.getElementById('data-feed-state-container');
    const downloadPcapBtn = document.getElementById('download-pcap-btn');

    let dataFeedEnabled = true;

    websocket = io('http://10.0.10.17:5050');

    websocket.on('connect', () => {
        console.log('Connected to flask socket io server.');
        updateDataFeedStateIcon();
    });

    websocket.on('packet', (data) => { 
        const packet = data.packet;
        if (dataFeedEnabled) {
            addPacketToFeed(packet);
        }
    });

    dataFeedStateContainer.addEventListener('click', () => {
        dataFeedEnabled = !dataFeedEnabled;
        updateDataFeedStateIcon();
    });

    downloadPcapBtn.addEventListener('click', () => {
        downloadPcapFile();
    });

    function addPacketToFeed(packet) {
        const row = document.createElement('div');
        row.classList.add('data-feed-row');

        const checkbox = document.createElement('input');
        checkbox.classList.add('checkbox');
        checkbox.type = 'checkbox';
        checkbox.value = packet.base64packet;
        
        const srcIpDiv = wrapDivAroundContent(packet.ip_src, 'source-ip');
        const dstIpDiv = wrapDivAroundContent(packet.ip_dst, 'dest-ip');
        const srcPortDiv = wrapDivAroundContent(packet.port_src, 'source-port');
        const dstPortDiv = wrapDivAroundContent(packet.port_dst, 'dest-port');

        row.appendChild(checkbox);
        row.appendChild(srcIpDiv);
        row.appendChild(dstIpDiv);
        row.appendChild(srcPortDiv);
        row.appendChild(dstPortDiv);

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

    function downloadPcapFile() {
        const packets = getCheckedPacketData();
        fetch('http://10.0.10.17:5050/download-pcap-file', {
            method : 'POST',
            headers: {
                'Content-type': 'application/json'
            },
            body: JSON.stringify(packets),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.blob();
        })
        .then(blob => {
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'capture.pcap'; 
            link.click();  
        })
        .catch(error => {
            console.error('Error trying to download pcap file:', error);
        });
    }

    function getCheckedPacketData() {
        const packets = [];
        const checkedPackets = document.querySelectorAll('.checkbox:checked');
        checkedPackets.forEach(packet => {
            packets.push(packet.value);
        });
        return packets;
    }



});