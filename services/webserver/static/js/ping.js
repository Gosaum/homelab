document.getElementById('ping').addEventListener('click', async () => {
    const result = document.getElementById('pong');
    try {
        const response = await fetch('/api/ping');
        if (!response.ok) throw new Error(response.status);
        const data = await response.json();
        result.textContent = data.status;
    } catch (err) {
        result.textContent = err.message;
    }
});