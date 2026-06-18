document.addEventListener('DOMContentLoaded', () => {
    // Determine which platforms are connected from hidden data
    const dataEls = document.querySelectorAll('.acct-data');
    const connectedMap = {};
    dataEls.forEach(el => {
        connectedMap[el.getAttribute('data-platform')] = el.getAttribute('data-name');
    });

    let connCount = 0;

    // Update the visual cards
    const cards = document.querySelectorAll('.c-card');
    cards.forEach(card => {
        const plat = card.getAttribute('data-plat');
        if (connectedMap[plat]) {
            connCount++;
            card.classList.add('is-conn');
            card.classList.remove('is-not-conn');
            // optionally inject real name
            const handleEl = card.querySelector('p.acct-handle.state-connected');
            if(handleEl) handleEl.textContent = connectedMap[plat];
        } else {
            card.classList.add('is-not-conn');
            card.classList.remove('is-conn');
        }
    });

    // Update Top Summary Stats
    const sumRatioEl = document.getElementById('sum-conn-ratio');
    if(sumRatioEl) sumRatioEl.textContent = `${connCount} / 4`;
    const sumConnEl = document.getElementById('sum-conn-count');
    if(sumConnEl) sumConnEl.textContent = connCount;
    const sumUnconnEl = document.getElementById('sum-unconn-count');
    if(sumUnconnEl) sumUnconnEl.textContent = 4 - connCount;
});