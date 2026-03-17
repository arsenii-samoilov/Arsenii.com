// Visit tracking - sends to /api/visit when backend is running
(function() {
  try {
    var base = (typeof window.ARSENII_API_URL === 'string' && window.ARSENII_API_URL) ? window.ARSENII_API_URL.replace(/\/$/, '') : '';
    var url = base + '/api/visit';
    var data = {
      page: window.location.pathname || window.location.href,
      referrer: document.referrer || '',
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    };
    navigator.sendBeacon && navigator.sendBeacon(url, new Blob([JSON.stringify(data)], { type: 'application/json' })) ||
      fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        keepalive: true
      }).catch(function() {});
  } catch (e) {}
})();
