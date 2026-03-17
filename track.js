// Visit tracking - sends to /api/visit when backend is running
(function() {
  try {
    var data = {
      page: window.location.pathname || window.location.href,
      referrer: document.referrer || '',
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    };
    navigator.sendBeacon && navigator.sendBeacon('/api/visit', new Blob([JSON.stringify(data)], { type: 'application/json' })) ||
      fetch('/api/visit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
        keepalive: true
      }).catch(function() {});
  } catch (e) {}
})();
