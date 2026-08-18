#!/usr/bin/env python3
# Builds the Insights hub, individual article pages, sitemap, and RSS feed
# from insights-data.json. Only articles whose date is on or before today are
# published. Future-dated articles stay hidden until their date arrives, so a
# daily cron run "publishes" them on schedule. Python 3.5 compatible.

import json
import os
from datetime import datetime, date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "insights-data.json")
ARTICLES_DIR = os.path.join(BASE_DIR, "insights")
SITE = "https://arsenii.com"
MAX_SEO_TITLE = 60
TITLE_SUFFIX_FULL = " | Arsenii Samoilov"
TITLE_SUFFIX_SHORT = " | Arsenii"

# Cohesive monoline icon set. Each value is the inner markup of a 24x24 SVG
# (stroke="currentColor", fill="none"). category_icon() wraps it. Color is set
# to the navy brand accent via the .cat-icon CSS class in insights.css.
CATEGORY_ICON_PATHS = {
    # cpu / chip
    "AI Program Management": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/>',
    # clipboard with check
    "Compliance": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/>',
    "Compliance Program Manager": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 14l2 2 4-4"/>',
    # trending-up arrow
    "Growth": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "Growth Program Manager": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    # classical building / columns
    "Governance": '<path d="M3 9l9-5 9 5"/><path d="M4 9h16"/><path d="M5.5 9v9M9.5 9v9M14.5 9v9M18.5 9v9"/><path d="M3 21h18"/>',
    # gear
    "Operations": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    # speech bubble
    "Communication": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8z"/>',
    # target / bullseye
    "Strategy": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.4"/>',
    # shield
    "Risk": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    # bar chart
    "Data": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/><line x1="3" y1="20" x2="21" y2="20"/>',
    # briefcase
    "Career": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><path d="M2 13h20"/>',
    # wrench
    "Engineering": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    # dollar sign
    "Monetization": '<line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    # clipboard (default)
    "Program Management": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M8 11h8M8 15h5"/>',
}

_ICON_DEFAULT = CATEGORY_ICON_PATHS["Program Management"]

CORE_PAGES = [
    ("/", "1.0", "weekly"),
    ("/about.html", "0.8", "monthly"),
    ("/career.html", "0.95", "monthly"),
    ("/insights.html", "0.9", "weekly"),
    ("/tools/", "0.8", "monthly"),
    ("/tools/raci-matrix-generator.html", "0.85", "monthly"),
    ("/tools/risk-register.html", "0.8", "monthly"),
    ("/tools/stakeholder-matrix.html", "0.8", "monthly"),
    ("/tools/raid-log.html", "0.8", "monthly"),
    ("/tools/decision-matrix.html", "0.8", "monthly"),
    ("/tools/status-report-generator.html", "0.8", "monthly"),
    ("/tools/prioritization-matrix.html", "0.8", "monthly"),
    ("/tools/project-charter-generator.html", "0.8", "monthly"),
    ("/tools/pre-mortem-worksheet.html", "0.8", "monthly"),
    ("/tools/okr-tracker.html", "0.8", "monthly"),
    ("/tools/meeting-cost-calculator.html", "0.8", "monthly"),
    ("/tools/roadmap-builder.html", "0.8", "monthly"),
    ("/tools/retrospective-board.html", "0.8", "monthly"),
    ("/tools/wsjf-calculator.html", "0.8", "monthly"),
    ("/tools/ai-use-case-prioritizer.html", "0.85", "monthly"),
    ("/tools/ai-adoption-metrics.html", "0.85", "monthly"),
    ("/tools/ai-governance-checklist.html", "0.85", "monthly"),
    ("/tools/ai-assistant-prompt-builder.html", "0.85", "monthly"),
    ("/tools/ai-work-habits-checklist.html", "0.85", "monthly"),
    ("/tools/worldwide-planning-intelligence.html", "0.85", "monthly"),
    ("/ai-program-management.html", "0.9", "weekly"),
    ("/salary-guide.html", "0.85", "monthly"),
    ("/interview-questions.html", "0.85", "monthly"),
    ("/glossary.html", "0.8", "monthly"),
    ("/complete-guide-to-program-management.html", "0.85", "monthly"),
    ("/how-to-become-a-technical-program-manager.html", "0.85", "monthly"),
    ("/program-and-project-types.html", "0.7", "monthly"),
    ("/program-type-migration.html", "0.6", "monthly"),
    ("/program-type-product-launch.html", "0.6", "monthly"),
    ("/program-type-infrastructure.html", "0.6", "monthly"),
    ("/program-type-compliance.html", "0.6", "monthly"),
    ("/program-type-ma-integration.html", "0.6", "monthly"),
    ("/program-type-digital-transformation.html", "0.6", "monthly"),
    ("/program-type-process-improvement.html", "0.6", "monthly"),
    ("/program-type-reliability.html", "0.6", "monthly"),
    ("/program-type-data-analytics.html", "0.6", "monthly"),
    ("/program-type-security.html", "0.6", "monthly"),
    ("/program-type-change-management.html", "0.6", "monthly"),
    ("/project-type-software-development.html", "0.6", "monthly"),
    ("/tpm-vs-project-manager.html", "0.75", "monthly"),
    ("/tpm-vs-product-manager.html", "0.75", "monthly"),
    ("/scrum-master-vs-tpm.html", "0.75", "monthly"),
    ("/raci-vs-raid.html", "0.75", "monthly"),
    ("/okr-vs-kpi.html", "0.75", "monthly"),
    ("/contact.html", "0.85", "monthly"),
    ("/photography.html", "0.7", "monthly"),
    ("/culinary.html", "0.7", "monthly"),
]

NAV = (
    '<header class="site-header">\n'
    '    <a href="/" class="brand"><span class="logo">Arsenii Samoilov</span></a>\n'
    '    <div class="menu-wrapper">\n'
    '      <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false" aria-haspopup="true"><span></span><span></span><span></span></button>\n'
    '      <nav class="nav-dropdown" aria-label="Main navigation">\n'
    '        <a href="/">Home</a>\n'
    '        <a href="{home}career.html">Career</a>\n'
    '        <a href="{home}culinary.html">Culinary</a>\n'
    '        <a href="{home}photography.html">Photography</a>\n'
    '        <a href="{home}insights.html">Insights</a>\n'
    '        <a href="{home}tools/">Tools</a>\n'
    '        <a href="{home}contact.html">Contact</a>\n'
    '      </nav>\n'
    '    </div>\n'
    '  </header>'
)

FOOTER_NAV = (
    '<nav aria-label="Site topics" style="max-width:760px;margin:2rem auto 0;padding:1.5rem 1.5rem 0.5rem;text-align:center;font-size:0.78rem;color:#aaa;line-height:2.4;border-top:1px solid #f0f0f0;">\n'
    '    <a href="{home}about.html" style="color:#aaa;margin:0 0.4rem;">About</a> &middot;\n'
    '    <a href="{home}career.html" style="color:#aaa;margin:0 0.4rem;">Senior Technical Program Manager</a> &middot;\n'
    '    <a href="{home}ai-program-management.html" style="color:#aaa;margin:0 0.4rem;">AI Program Management</a> &middot;\n'
    '    <a href="{home}insights.html" style="color:#aaa;margin:0 0.4rem;">Program Management Insights</a> &middot;\n'
    '    <a href="{home}insights/compliance-playbook.html" style="color:#aaa;margin:0 0.4rem;">Compliance Playbook</a> &middot;\n'
    '    <a href="{home}insights/decision-logs-underrated-tpm-tool.html" style="color:#aaa;margin:0 0.4rem;">Decision Logs</a> &middot;\n'
    '    <a href="{home}culinary.html" style="color:#aaa;margin:0 0.4rem;">Culinary</a> &middot;\n'
    '    <a href="{home}photography.html" style="color:#aaa;margin:0 0.4rem;">Photography</a> &middot;\n'
    '    <a href="{home}contact.html" style="color:#aaa;margin:0 0.4rem;">Hire a Program Manager</a>\n'
    '  </nav>'
)


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def category_icon(category):
    inner = CATEGORY_ICON_PATHS.get(category, _ICON_DEFAULT)
    return (
        '<svg class="cat-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true" focusable="false">' + inner + '</svg>'
    )


def fmt_date(d):
    return d.strftime("%B %-d, %Y") if os.name != "nt" else d.strftime("%B %d, %Y")


def seo_page_title(headline, override=None):
    """Build a <=60 char browser title; prefer full suffix, then short, then trim."""
    if override:
        return override
    for suffix in (TITLE_SUFFIX_FULL, TITLE_SUFFIX_SHORT):
        candidate = headline + suffix
        if len(candidate) <= MAX_SEO_TITLE:
            return candidate
    max_head = MAX_SEO_TITLE - len(TITLE_SUFFIX_SHORT)
    head = headline[:max_head]
    if " " in head:
        head = head.rsplit(" ", 1)[0]
    return head + TITLE_SUFFIX_SHORT


def load_articles():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for a in data["articles"]:
        a["_date"] = datetime.strptime(a["date"], "%Y-%m-%d").date()
        out.append(a)
    out.sort(key=lambda x: x["_date"], reverse=True)
    return out


def page_head(title, description, canonical, css_prefix, rss_prefix, extra_ld="", keywords=""):
    kw_tag = ('  <meta name="keywords" content="' + esc(keywords) + '">\n') if keywords else ""
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '  <meta charset="UTF-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '  <meta name="theme-color" content="#1e3a5f">\n'
        '  <script>\n'
        '    window.dataLayer = window.dataLayer || [];\n'
        '    function gtag(){dataLayer.push(arguments);}\n'
        '    gtag("js", new Date());\n'
        '    gtag("config", "G-LJE40VWDPW");\n'
        '    var g=document.createElement("script");g.async=true;'
        'g.src="https://www.googletagmanager.com/gtag/js?id=G-LJE40VWDPW";'
        'document.head.appendChild(g);\n'
        '  </script>\n'
        '  <link rel="icon" type="image/svg+xml" href="' + css_prefix + 'favicon.svg">\n'
        '  <link rel="icon" type="image/png" sizes="32x32" href="' + css_prefix + 'favicon-32.png">\n'
        '  <link rel="icon" type="image/png" sizes="16x16" href="' + css_prefix + 'favicon-16.png">\n'
        '  <link rel="icon" type="image/x-icon" href="' + css_prefix + 'favicon.ico">\n'
        '  <link rel="apple-touch-icon" href="' + css_prefix + 'apple-touch-icon.png">\n'
        '  <link rel="manifest" href="' + css_prefix + 'site.webmanifest">\n'
        '  <title>' + esc(title) + '</title>\n'
        '  <meta name="description" content="' + esc(description) + '">\n'
        + kw_tag +
        '  <meta name="author" content="Arsenii Samoilov">\n'
        '  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">\n'
        '  <link rel="canonical" href="' + canonical + '">\n'
        '  <meta property="og:type" content="article">\n'
        '  <meta property="og:url" content="' + canonical + '">\n'
        '  <meta property="og:title" content="' + esc(title) + '">\n'
        '  <meta property="og:description" content="' + esc(description) + '">\n'
        '  <meta property="og:image" content="' + SITE + '/images/headshot-share.jpg">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="799">\n'
        '  <meta property="og:image:alt" content="Arsenii Samoilov - Senior Technical Program Manager">\n'
        '  <meta property="og:site_name" content="Arsenii Samoilov">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <meta name="twitter:title" content="' + esc(title) + '">\n'
        '  <meta name="twitter:description" content="' + esc(description) + '">\n'
        '  <meta name="twitter:image" content="' + SITE + '/images/headshot-share.jpg">\n'
        '  <meta name="twitter:image:alt" content="Arsenii Samoilov - Senior Technical Program Manager">\n'
        '  <link rel="alternate" type="application/rss+xml" title="Arsenii Samoilov - Program Management Insights" href="' + SITE + '/feed.xml">\n'
        + extra_ld +
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n'
        '  <link rel="stylesheet" href="' + css_prefix + 'styles.css?v=35">\n'
        '  <link rel="stylesheet" href="' + css_prefix + 'insights.css?v=4">\n'
        '</head>\n<body>\n  '
    )


def related_articles(a, published, limit=3):
    others = [x for x in published if x["slug"] != a["slug"]]
    same_cat = [x for x in others if x["category"] == a["category"]]
    rest = [x for x in others if x["category"] != a["category"]]
    return (same_cat + rest)[:limit]


def build_article_page(a, published):
    canonical = SITE + "/insights/" + a["slug"] + ".html"
    modified = a.get("modified", a["date"])
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": a["title"],
        "description": a["description"],
        "datePublished": a["date"],
        "dateModified": modified,
        "author": {"@type": "Person", "name": "Arsenii Samoilov", "url": SITE, "sameAs": ["https://www.linkedin.com/in/arseniisamoilov/", "https://www.wikidata.org/wiki/Q139972269", "https://github.com/arsenii-samoilov"]},
        "publisher": {"@type": "Person", "name": "Arsenii Samoilov"},
        "mainEntityOfPage": canonical,
        "url": canonical,
        "articleSection": a["category"],
        "keywords": ", ".join(a["tags"]),
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": SITE + "/insights.html"},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": canonical},
        ],
    }
    howto_ld = ""
    if "howto" in a:
        hw = a["howto"]
        howto_schema = {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": hw["name"],
            "description": hw["description"],
            "author": {"@type": "Person", "name": "Arsenii Samoilov", "url": SITE},
            "step": [
                {"@type": "HowToStep", "name": s["name"], "text": s["text"]}
                for s in hw["steps"]
            ]
        }
        howto_ld = '  <script type="application/ld+json">' + json.dumps(howto_schema) + '</script>\n'

    extra_ld = (
        '  <meta property="article:published_time" content="' + a["date"] + '">\n'
        '  <meta property="article:modified_time" content="' + modified + '">\n'
        '  <meta property="article:author" content="Arsenii Samoilov">\n'
        '  <meta property="article:section" content="' + esc(a["category"]) + '">\n'
        + "".join('  <meta property="article:tag" content="' + esc(t) + '">\n' for t in a["tags"]) +
        '  <script type="application/ld+json">' + json.dumps(ld) + '</script>\n'
        '  <script type="application/ld+json">' + json.dumps(crumbs) + '</script>\n'
        + howto_ld)

    tags_html = "".join('<span class="insight-tag">' + esc(t) + '</span>' for t in a["tags"])

    related = related_articles(a, published)
    related_html = ""
    if related:
        rows = ""
        for r in related:
            rows += (
                '        <a class="related-row" href="' + r["slug"] + '.html">\n'
                '          <span class="related-meta">' + esc(r["category"]) + '</span>\n'
                '          <span class="related-title">' + esc(r["title"]) + '</span>\n'
                '        </a>\n'
            )
        related_html = (
            '      <aside class="related-insights" aria-label="Related insights">\n'
            '        <h2 class="related-heading">Related Insights</h2>\n'
            + rows +
            '      </aside>\n'
        )

    article_kw = ", ".join(a["tags"]) + ", Technical Program Manager, Arsenii Samoilov"
    icon = category_icon(a["category"])
    page_title = seo_page_title(a["title"], a.get("seoTitle"))
    html = page_head(page_title, a["description"], canonical,
                     "../", "../", extra_ld, article_kw)
    html += NAV.format(home="../")
    html += (
        '\n  <main>\n'
        '    <article class="article-page">\n'
        '      <p class="eyebrow"><a href="../insights.html" style="color:inherit;">Insights</a> &middot; ' + icon + ' ' + esc(a["category"]) + ' &middot; ' + fmt_date(a["_date"]) + '</p>\n'
        '      <h1>' + icon + ' ' + esc(a["title"]) + '</h1>\n'
        '      <div class="article-body">' + a["body"] + '\n'
        '        <p class="article-author-note">Arsenii Samoilov is a <a href="../career.html" style="color:var(--accent);font-weight:500;">Senior Technical Program Manager</a> with 19+ years at Intuit, Atlassian, Adobe, Salesforce, Roku, and Apple.</p>\n'
        '      </div>\n'
        '      <div class="insight-tags">' + tags_html + '</div>\n'
        + related_html +
        '      <div class="article-footer-nav"><a href="../insights.html" class="btn btn-ghost">&larr; All Insights</a> <a href="../contact.html" class="btn btn-secondary">Work with me &rarr;</a></div>\n'
        '    </article>\n'
        '  </main>\n  '
    )
    html += FOOTER_NAV.format(home="../")
    html += ('\n  <footer class="site-footer"><p>&copy; 2026 Arsenii Samoilov. Bay Area, California.</p></footer>\n'
             '  <script src="../main.js?v=2"></script>\n</body>\n</html>\n')
    return html


def build_index(published):
    canonical = SITE + "/insights.html"
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Program Management Insights by Arsenii Samoilov",
        "url": canonical,
        "description": "Program management insights from a Senior Technical Program Manager with 19+ years at Intuit, Atlassian, Adobe, Salesforce, Roku, and Apple.",
        "author": {"@type": "Person", "name": "Arsenii Samoilov", "jobTitle": "Senior Technical Program Manager", "url": SITE, "sameAs": ["https://www.linkedin.com/in/arseniisamoilov/", "https://www.wikidata.org/wiki/Q139972269", "https://github.com/arsenii-samoilov"]},
        "blogPost": [
            {"@type": "BlogPosting", "headline": a["title"],
             "url": SITE + "/insights/" + a["slug"] + ".html",
             "datePublished": a["date"], "description": a["description"]}
            for a in published
        ],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Insights", "item": canonical},
        ],
    }
    extra_ld = ('  <script type="application/ld+json">' + json.dumps(blog_ld) + '</script>\n'
                '  <script type="application/ld+json">' + json.dumps(crumbs) + '</script>\n')

    html = page_head(
        "Program Management Insights | Arsenii Samoilov",
        "Program management insights from a Senior Technical Program Manager: AI adoption, compliance, growth programs, and enterprise delivery after 19+ years in tech.",
        canonical, "", "", extra_ld,
        "Technical Program Manager, Senior TPM, AI Program Management, Compliance Program Manager, Engineering Program Manager, program management insights, TPM blog, Arsenii Samoilov, enterprise program management, Bay Area")
    html += NAV.format(home="")
    html += (
        '\n  <main>\n'
        '    <div class="insights-hero">\n'
        '      <h1>Program Management Insights</h1>\n'
        '      <p>Notes on program management from 19+ years leading enterprise programs at Intuit, Atlassian, Adobe, Salesforce, Roku, and Apple. AI adoption, compliance governance, and growth strategy.</p>\n'
        '    </div>\n'
        '    <div class="insights-index">\n'
    )
    for a in published:
        url = "insights/" + a["slug"] + ".html"
        icon = category_icon(a["category"])
        pills = "".join(
            '<span class="index-tag">' + esc(t) + '</span>'
            for t in a["tags"][:3]
        )
        html += (
            '      <a class="index-row" href="' + url + '">\n'
            '        <span class="index-meta">' + icon + ' ' + esc(a["category"]) + ' &middot; ' + fmt_date(a["_date"]) + '</span>\n'
            '        <h2>' + icon + ' ' + esc(a["title"]) + '</h2>\n'
            '        <p>' + esc(a["description"]) + '</p>\n'
            '        <div class="index-tags">' + pills + '</div>\n'
            '      </a>\n'
        )
    html += (
        '    </div>\n'
        '    <div style="max-width:760px;margin:0 auto;padding:3rem 1.5rem 1rem;border-top:2px solid var(--accent-light);">\n'
        '      <p style="font-family:var(--font-sans);font-size:0.7rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--text-muted);margin:0 0 0.75rem;">Program Management Tools</p>\n'
        '      <p style="font-size:var(--text-sm);line-height:1.85;color:var(--text);margin:0 0 1rem;">A small set of <a href="tools/" style="color:var(--accent);font-weight:500;">program management tools</a> I offer to the TPM community. They run in your browser with no signup: the RACI Matrix Generator for who owns what, the Program Risk Register for scoring and tracking risk, and the Stakeholder Power/Interest Grid for deciding who to keep close. Each one exports to CSV or print.</p>\n'
        '      <p style="font-size:var(--text-sm);line-height:1.85;color:var(--text);margin:0 0 1rem;">For the TPM career path, see the <a href="salary-guide.html" style="color:var(--accent);font-weight:500;">Technical Program Manager salary guide</a>, a set of real <a href="interview-questions.html" style="color:var(--accent);font-weight:500;">TPM interview questions</a>, and a plain-English <a href="glossary.html" style="color:var(--accent);font-weight:500;">program management glossary</a>.</p>\n'
        '      <p style="font-family:var(--font-sans);font-size:0.7rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--text-muted);margin:0 0 0.75rem;">Guides</p>\n'
        '      <p style="font-size:var(--text-sm);line-height:1.85;color:var(--text);margin:0 0 2rem;">New to the discipline? Start with the <a href="complete-guide-to-program-management.html" style="color:var(--accent);font-weight:500;">complete guide to program management</a> or <a href="how-to-become-a-technical-program-manager.html" style="color:var(--accent);font-weight:500;">how to become a technical program manager</a>. Browse the <a href="program-and-project-types.html" style="color:var(--accent);font-weight:500;">types of programs and projects</a> for migration, launch, compliance, security, and more. For quick role distinctions, see <a href="tpm-vs-project-manager.html" style="color:var(--accent);font-weight:500;">TPM vs project manager</a> and <a href="tpm-vs-product-manager.html" style="color:var(--accent);font-weight:500;">TPM vs product manager</a>.</p>\n'
        '      <p style="font-family:var(--font-sans);font-size:0.7rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:var(--text-muted);margin:0 0 0.75rem;">Advisory &amp; Consulting</p>\n'
        '      <h2 style="font-family:var(--font-serif);font-size:clamp(1.3rem,3vw,1.7rem);font-weight:600;color:var(--accent-dark);margin:0 0 1rem;">Available for TPM Advisory Engagements</h2>\n'
        '      <p style="font-size:var(--text-sm);line-height:1.85;color:var(--text);margin:0 0 1rem;">Beyond full-time roles, I take selective advisory engagements where a senior technical program manager can accelerate a specific outcome: standing up a compliance framework, unblocking an AI adoption initiative, or restructuring a growth program that has stalled.</p>\n'
        '      <p style="font-size:var(--text-sm);line-height:1.85;color:var(--text);margin:0 0 1.5rem;">If your team needs an experienced enterprise program manager for a defined problem, <a href="contact.html" style="color:var(--accent);font-weight:500;">get in touch</a>.</p>\n'
        '      <a href="contact.html" class="btn btn-secondary">Contact for Advisory &rarr;</a>\n'
        '    </div>\n'
        '  </main>\n  '
    )
    html += FOOTER_NAV.format(home="")
    html += ('\n  <footer class="site-footer"><p>&copy; 2026 Arsenii Samoilov. Bay Area, California.</p></footer>\n'
             '  <script src="main.js?v=2"></script>\n</body>\n</html>\n')
    return html


def build_sitemap(published):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, prio, freq in CORE_PAGES:
        lines += ['  <url>', '    <loc>' + SITE + loc + '</loc>',
                  '    <lastmod>' + today + '</lastmod>',
                  '    <changefreq>' + freq + '</changefreq>',
                  '    <priority>' + prio + '</priority>', '  </url>']
    for a in published:
        lines += ['  <url>',
                  '    <loc>' + SITE + '/insights/' + a["slug"] + '.html</loc>',
                  '    <lastmod>' + a["date"] + '</lastmod>',
                  '    <changefreq>yearly</changefreq>',
                  '    <priority>0.8</priority>', '  </url>']
    lines.append('</urlset>')
    return "\n".join(lines) + "\n"


def build_feed(published):
    items = []
    for a in published[:20]:
        url = SITE + "/insights/" + a["slug"] + ".html"
        pub = datetime.strptime(a["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 09:00:00 -0800")
        items.append(
            '    <item>\n'
            '      <title>' + esc(a["title"]) + '</title>\n'
            '      <link>' + url + '</link>\n'
            '      <guid isPermaLink="true">' + url + '</guid>\n'
            '      <pubDate>' + pub + '</pubDate>\n'
            '      <description>' + esc(a["description"]) + '</description>\n'
            '    </item>'
        )
    build_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S -0800")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '  <channel>\n'
        '    <title>Arsenii Samoilov - Program Management Insights</title>\n'
        '    <link>' + SITE + '/insights.html</link>\n'
        '    <atom:link href="' + SITE + '/feed.xml" rel="self" type="application/rss+xml"/>\n'
        '    <description>Program management insights from Arsenii Samoilov, Senior Technical Program Manager.</description>\n'
        '    <language>en-us</language>\n'
        '    <lastBuildDate>' + build_date + '</lastBuildDate>\n'
        + "\n".join(items) + '\n'
        '  </channel>\n</rss>\n'
    )


def main():
    articles = load_articles()
    today = date.today()
    published = [a for a in articles if a["_date"] <= today]

    os.makedirs(ARTICLES_DIR, exist_ok=True)

    for a in published:
        path = os.path.join(ARTICLES_DIR, a["slug"] + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_article_page(a, published))

    with open(os.path.join(BASE_DIR, "insights.html"), "w", encoding="utf-8") as f:
        f.write(build_index(published))
    with open(os.path.join(BASE_DIR, "sitemap-pages.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap(published))
    with open(os.path.join(BASE_DIR, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(build_feed(published))

    scheduled = len(articles) - len(published)
    over = []
    for a in articles:
        title = seo_page_title(a["title"], a.get("seoTitle"))
        if len(title) > MAX_SEO_TITLE:
            over.append(a["slug"])
    if over:
        raise SystemExit("SEO titles exceed {0} chars: {1}".format(MAX_SEO_TITLE, ", ".join(over)))
    print("Published: {0}  Scheduled: {1}  Total: {2}".format(
        len(published), scheduled, len(articles)))


if __name__ == "__main__":
    main()
