const socket = io();
const cpu = document.getElementById('cpu');

socket.on('cpu', (data) => {
    cpu.textContent = Math.round(data.percent) + '%';
});