const socket = io();
const set = (id, value) => document.getElementById(id).textContent = value;

const formatPercent = (value) => String(Math.round(value)).padStart(2, '0');
const formatSize = (bytes) => (bytes / 1e9).toFixed(1);
const formatUptime = (s) => {
    const d = Math.floor(s / 86400);
    const h = Math.floor((s % 86400) / 3600);
    const m = Math.floor((s % 3600) / 60);
    return d > 0 ? `${d}d ${h}h` : `${h}h ${m}m`;
};

socket.on('kpis', (s) => {
    set('uptime', formatUptime(s.uptime));
    set('cpu', formatPercent(s.cpu));
    set('ram', formatPercent(s.ram));
    set('ram_used', formatSize(s.ram_used));
    set('ram_total', formatSize(s.ram_total));
    set('disk', formatPercent(s.disk));
    set('disk_used', formatSize(s.disk_used));
    set('disk_total', formatSize(s.disk_total));
});