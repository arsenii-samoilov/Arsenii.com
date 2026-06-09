#!/usr/bin/env python3
"""Regenerate server/nginx-path-redirects.conf after adding pages. Deploy to server snippets/."""
import os

OUT = os.path.join(os.path.dirname(__file__), "nginx-path-redirects.conf")

pages = [
    "/about.html", "/career.html", "/contact.html", "/culinary.html", "/photography.html",
    "/glossary.html", "/salary-guide.html", "/interview-questions.html",
    "/ai-program-management.html",
    "/complete-guide-to-program-management.html",
    "/how-to-become-a-technical-program-manager.html",
    "/program-and-project-types.html", "/program-type-migration.html",
    "/program-type-product-launch.html", "/program-type-infrastructure.html",
    "/program-type-compliance.html", "/program-type-ma-integration.html",
    "/program-type-digital-transformation.html", "/program-type-process-improvement.html",
    "/program-type-reliability.html", "/program-type-data-analytics.html",
    "/program-type-security.html", "/program-type-change-management.html",
    "/project-type-software-development.html", "/tpm-vs-project-manager.html",
    "/tpm-vs-product-manager.html", "/scrum-master-vs-tpm.html", "/raci-vs-raid.html",
    "/okr-vs-kpi.html",
]
insights = [
    "ai-adoption", "compliance-playbook", "decision-logs-underrated-tpm-tool",
    "escalation-paths-with-teeth", "first-30-days-on-a-new-program", "growth-pm",
    "managing-dependencies-eight-teams", "project-manager-vs-technical-program-manager",
    "status-report-executives-actually-read",
]
tools = [
    "raci-matrix-generator", "risk-register", "stakeholder-matrix", "raid-log",
    "decision-matrix", "status-report-generator", "prioritization-matrix",
    "project-charter-generator", "pre-mortem-worksheet", "okr-tracker",
    "meeting-cost-calculator", "roadmap-builder", "retrospective-board", "wsjf-calculator",
    "ai-use-case-prioritizer", "ai-adoption-metrics", "ai-governance-checklist",
    "ai-assistant-prompt-builder",
    "ai-work-habits-checklist",
]

lines = [
    "# Path canonicalization for arsenii.com",
    "if ($request_uri = /index.htm) { return 301 https://arsenii.com/; }",
    "if ($request_uri = /index.html) { return 301 https://arsenii.com/; }",
    "if ($request_uri = /tools/index.htm) { return 301 https://arsenii.com/tools/; }",
    "if ($args ~* \"^source=\") { return 301 https://arsenii.com/; }",
    "location = /pricing { return 301 https://arsenii.com/contact.html; }",
    "location = /pricing.html { return 301 https://arsenii.com/contact.html; }",
    "location = /insights { return 301 https://arsenii.com/insights.html; }",
    "location = /insights/ { return 301 https://arsenii.com/insights.html; }",
    "if ($request_uri = /tools/index.html) { return 301 https://arsenii.com/tools/; }",
]
for p in pages:
    slug = p[1:-5]
    lines.append("location = /%s { return 301 https://arsenii.com%s; }" % (slug, p))
for slug in insights:
    lines.append(
        "location = /insights/%s { return 301 https://arsenii.com/insights/%s.html; }"
        % (slug, slug)
    )
for slug in tools:
    lines.append(
        "location = /tools/%s { return 301 https://arsenii.com/tools/%s.html; }"
        % (slug, slug)
    )
lines.append('if ($request_uri ~ "^//+") { return 301 https://arsenii.com$uri; }')

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("Wrote", OUT)
