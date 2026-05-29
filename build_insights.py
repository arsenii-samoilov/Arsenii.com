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

CATEGORY_ICONS = {
    "AI Program Management": "🤖",
    "Compliance": "📋",
    "Compliance Program Manager": "📋",
    "Growth": "🚀",
    "Growth Program Manager": "🚀",
    "Governance": "🏛",
    "Operations": "⚙️",
    "Communication": "💬",
    "Strategy": "🎯",
    "Risk": "🛡",
    "Data": "📊",
    "Career": "🗂",
    "Engineering": "🔧",
    "Monetization": "💰",
    "Program Management": "📌",
}

CORE_PAGES = [
    ("/", "1.0", "weekly"),
    ("/career.html", "0.95", "monthly"),
    ("/insights.html", "0.9", "weekly"),
    ("/contact.html", "0.85", "monthly"),
    ("/photography.html", "0.7", "monthly"),
    ("/culinary.html", "0.7", "monthly"),
]

NAV = (
    '<header class="site-header">\n'
    '    <a href="{home}index.html" class="brand"><span class="logo">Arsenii Samoilov</span></a>\n'
    '    <div class="menu-wrapper">\n'
    '      <button class="menu-toggle" aria-label="Toggle menu" aria-expanded="false" aria-haspopup="true"><span></span><span></span><span></span></button>\n'
    '      <nav class="nav-dropdown" aria-label="Main navigation">\n'
    '        <a href="{home}index.html">Home</a>\n'
    '        <a href="{home}career.html">Career</a>\n'
    '        <a href="{home}culinary.html">Culinary</a>\n'
    '        <a href="{home}photography.html">Photography</a>\n'
    '        <a href="{home}insights.html">Insights</a>\n'
    '        <a href="{home}contact.html">Contact</a>\n'
    '      </nav>\n'
    '    </div>\n'
    '  </header>'
)

FOOTER_NAV = (
    '<nav aria-label="Site topics" style="max-width:760px;margin:2rem auto 0;padding:1.5rem 1.5rem 0.5rem;text-align:center;font-size:0.78rem;color:#aaa;line-height:2.4;border-top:1px solid #f0f0f0;">\n'
    '    <a href="{home}career.html" style="color:#aaa;margin:0 0.4rem;">Senior Technical Program Manager</a> &middot;\n'
    '    <a href="{home}career.html" style="color:#aaa;margin:0 0.4rem;">Engineering Program Manager</a> &middot;\n'
    '    <a href="{home}insights.html" style="color:#aaa;margin:0 0.4rem;">TPM Insights</a> &middot;\n'
    '    <a href="{home}career.html" style="color:#aaa;margin:0 0.4rem;">AI Program Management</a> &middot;\n'
    '    <a href="{home}contact.html" style="color:#aaa;margin:0 0.4rem;">Hire a Program Manager</a>\n'
    '  </nav>'
)


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def category_icon(category):
    return CATEGORY_ICONS.get(category, "📌")


def fmt_date(d):
    return d.strftime("%B %-d, %Y") if os.name != "nt" else d.strftime("%B %d, %Y")


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
        '  <meta name="theme-color" content="#ffffff">\n'
        '  <script>\n'
        '    window.dataLayer = window.dataLayer || [];\n'
        '    function gtag(){dataLayer.push(arguments);}\n'
        '    gtag("js", new Date());\n'
        '    gtag("config", "G-LJE40VWDPW");\n'
        '    var g=document.createElement("script");g.async=true;'
        'g.src="https://www.googletagmanager.com/gtag/js?id=G-LJE40VWDPW";'
        'document.head.appendChild(g);\n'
        '  </script>\n'
        '  <link rel="icon" type="image/png" href="' + css_prefix + 'favicon.png">\n'
        '  <link rel="icon" type="image/x-icon" href="' + css_prefix + 'favicon.ico">\n'
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
        '  <meta property="og:site_name" content="Arsenii Samoilov">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        '  <meta name="twitter:title" content="' + esc(title) + '">\n'
        '  <meta name="twitter:description" content="' + esc(description) + '">\n'
        '  <meta name="twitter:image" content="' + SITE + '/images/headshot-share.jpg">\n'
        '  <link rel="alternate" type="application/rss+xml" title="Arsenii Samoilov - TPM Insights" href="' + SITE + '/feed.xml">\n'
        + extra_ld +
        '  <link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">\n'
        '  <link rel="stylesheet" href="' + css_prefix + 'styles.css?v=34">\n'
        '  <link rel="stylesheet" href="' + css_prefix + 'insights.css?v=3">\n'
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
    html = page_head(a["title"] + " | Arsenii Samoilov", a["description"], canonical,
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
        "name": "TPM Insights by Arsenii Samoilov",
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
    extra_ld = '  <script type="application/ld+json">' + json.dumps(blog_ld) + '</script>\n'

    html = page_head(
        "TPM Insights | Arsenii Samoilov | Senior Technical Program Manager",
        "Program management insights from Arsenii Samoilov, Senior Technical Program Manager with 19+ years at Intuit, Atlassian, Adobe, Salesforce, Roku, and Apple. AI program management, compliance governance, and enterprise growth.",
        canonical, "", "", extra_ld,
        "Technical Program Manager, Senior TPM, AI Program Management, Compliance Program Manager, Engineering Program Manager, program management insights, TPM blog, Arsenii Samoilov, enterprise program management, Bay Area")
    html += NAV.format(home="")
    html += (
        '\n  <main>\n'
        '    <div class="insights-hero">\n'
        '      <h1>TPM Insights</h1>\n'
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
        '    <title>Arsenii Samoilov - TPM Insights</title>\n'
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
    print("Published: {0}  Scheduled: {1}  Total: {2}".format(
        len(published), scheduled, len(articles)))


if __name__ == "__main__":
    main()
