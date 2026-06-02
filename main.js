// Dropdown menu toggle
document.addEventListener('DOMContentLoaded', function () {
  const toggle = document.querySelector('.menu-toggle');
  const dropdown = document.querySelector('.nav-dropdown');
  if (toggle && dropdown) {
    toggle.addEventListener('click', function (e) {
      e.stopPropagation();
      dropdown.classList.toggle('open');
      toggle.setAttribute('aria-expanded', dropdown.classList.contains('open'));
    });
    document.addEventListener('click', function () {
      dropdown.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  }

  // GA4 conversion tracking: resume download & LinkedIn profile click
  document.addEventListener('click', function (e) {
    var link = e.target.closest('a');
    if (!link || !link.href) return;
    if (typeof gtag !== 'function') return;
    if (link.hasAttribute('download') && link.href.indexOf('.pdf') !== -1) {
      gtag('event', 'resume_download', { page_location: window.location.href, link_url: link.href });
    } else if (link.href.indexOf('linkedin.com/in/arseniisamoilov') !== -1) {
      gtag('event', 'linkedin_profile_click', { page_location: window.location.href, link_url: link.href });
    }
  });
});
