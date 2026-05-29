#!/usr/bin/env python3
"""Trim meta descriptions/titles and sync og/twitter tags across static HTML."""
import re
import glob
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DESCRIPTIONS = {
    "index.html": "Senior TPM with 19+ years at Intuit, Atlassian, Adobe, Salesforce, Roku, and Apple. AI programs, enterprise delivery, and compliance. Bay Area.",
    "career.html": "Senior Technical Program Manager resume: Intuit, Atlassian, Adobe, Salesforce, Roku, Apple. AI program management, compliance, and enterprise delivery.",
    "insights.html": "TPM insights from a Senior Technical Program Manager: AI adoption, compliance, growth programs, and enterprise delivery after 19+ years in tech.",
    "contact.html": "Contact Arsenii Samoilov, Senior Technical Program Manager, for TPM roles, advisory, or program leadership. Bay Area, open to remote.",
    "glossary.html": "Plain-language program management glossary: RACI, RAID, critical path, blast radius, north star, and terms TPMs use daily.",
    "salary-guide.html": "Technical Program Manager salary ranges by level and company (2026), plus a calculator to estimate TPM total compensation.",
    "interview-questions.html": "Technical Program Manager interview questions with what strong answers sound like, from a Senior TPM with 19+ years in tech.",
    "complete-guide-to-program-management.html": "Complete guide to program management: charter, stakeholders, dependencies, risk, status, and how TPMs run cross-team outcomes.",
    "how-to-become-a-technical-program-manager.html": "How to become a technical program manager: skills, career path, interview prep, and what hiring managers look for in TPM candidates.",
    "program-and-project-types.html": "Reference guide to program and project types: migration, product launch, compliance, M&A, transformation, security, and more.",
    "program-type-change-management.html": "Organizational change management programs: ADKAR, Kotter, sponsorship, resistance, and adoption metrics for enterprise change.",
    "program-type-compliance.html": "Compliance and regulatory programs: SOC 2, audits, control mapping, evidence, and cross-functional remediation at scale.",
    "program-type-data-analytics.html": "Data and analytics programs: pipelines, governance, self-serve BI, and delivering trusted metrics across the business.",
    "program-type-digital-transformation.html": "Digital transformation programs: modernizing operations, customer experience, and technology stacks with measurable outcomes.",
    "program-type-infrastructure.html": "Infrastructure and platform programs: reliability, capacity, migrations, and shared services that engineering teams depend on.",
    "program-type-process-improvement.html": "Process improvement and operational excellence programs: Lean, DMAIC, waste reduction, and sustainable operating models.",
    "program-type-reliability.html": "Reliability and incident management programs: SLOs, error budgets, on-call, postmortems, and reducing customer-impacting outages.",
    "program-type-security.html": "Security programs aligned to NIST CSF: identity, detection, response, and reducing risk across products and infrastructure.",
    "project-type-software-development.html": "Software development projects vs programs: scope, delivery cadence, and when a project manager owns the work end to end.",
    "tpm-vs-project-manager.html": "TPM vs project manager: scope, technical depth, and when to hire each. Side-by-side comparison from a Senior TPM.",
    "tpm-vs-product-manager.html": "TPM vs product manager: outcomes, roadmaps, and technical coordination compared side by side for hiring and career decisions.",
    "scrum-master-vs-tpm.html": "Scrum Master vs TPM: ceremonies vs cross-team outcomes. When agile delivery leadership differs from program management.",
    "raci-vs-raid.html": "RACI vs RAID: responsibility matrices vs risks, assumptions, issues, and dependencies. When to use each artifact.",
    "okr-vs-kpi.html": "OKR vs KPI: ambitious outcomes vs steady operational measures. How TPMs use both without duplicating reporting.",
    "tools/index.html": "Free program management tools: RACI, risk register, RAID log, stakeholder matrix, charter, OKR tracker, and more. Browser-based, no signup.",
    "tools/raci-matrix-generator.html": "Free RACI matrix generator: assign Responsible, Accountable, Consulted, Informed. Export CSV or print. No signup.",
    "tools/risk-register.html": "Free program risk register: score probability and impact, track owners and mitigations. Export CSV or print.",
    "tools/stakeholder-matrix.html": "Free stakeholder power/interest matrix: map sponsors and partners, plan engagement. Export CSV or print.",
    "tools/raid-log.html": "Free RAID log template: track risks, assumptions, issues, and dependencies in one place. Export CSV or print.",
    "tools/decision-matrix.html": "Free weighted decision matrix: score options against criteria with weights. Export CSV or print.",
    "tools/status-report-generator.html": "Free project status report generator: RAG status, accomplishments, risks, and next steps. Export Word or print.",
    "tools/prioritization-matrix.html": "Free effort/impact prioritization matrix: rank initiatives for maximum leverage. Export CSV or print.",
    "tools/project-charter-generator.html": "Free project charter generator: scope, goals, stakeholders, and success criteria. Export Word or print.",
    "tools/pre-mortem-worksheet.html": "Free pre-mortem worksheet: surface failure modes before launch. Export CSV or print.",
    "tools/okr-tracker.html": "Free OKR tracker: objectives, key results, and progress updates. Export CSV or print.",
    "tools/meeting-cost-calculator.html": "Meeting cost calculator: estimate spend by attendees, duration, and loaded hourly rate.",
    "tools/roadmap-builder.html": "Free roadmap builder: timeline milestones and dependencies for program planning. Export CSV or print.",
    "tools/retrospective-board.html": "Free retrospective board: Start, Stop, Continue columns for team retros. Export CSV or print.",
    "tools/wsjf-calculator.html": "WSJF calculator: weighted shortest job first prioritization for backlog and portfolio decisions.",
}

TITLES = {
    "index.html": "Arsenii Samoilov | Senior Technical Program Manager",
    "career.html": "Senior TPM Resume | Arsenii Samoilov | Intuit, Apple",
    "insights.html": "TPM Insights | Arsenii Samoilov",
    "contact.html": "Hire a Senior TPM | Arsenii Samoilov",
    "interview-questions.html": "TPM Interview Questions (2026) | Arsenii Samoilov",
    "salary-guide.html": "TPM Salary Guide & Calculator (2026) | Arsenii",
    "scrum-master-vs-tpm.html": "Scrum Master vs TPM: What's the Difference?",
    "tpm-vs-project-manager.html": "TPM vs Project Manager: What's the Difference?",
    "tpm-vs-product-manager.html": "TPM vs Product Manager: What's the Difference?",
    "tools/index.html": "Free TPM Tools | RACI, Risk Register, RAID",
    "tools/raci-matrix-generator.html": "Free RACI Matrix Generator | Build Online",
    "tools/risk-register.html": "Free Program Risk Register | Export Online",
    "tools/stakeholder-matrix.html": "Free Stakeholder Matrix | Power/Interest Grid",
    "tools/decision-matrix.html": "Free Weighted Decision Matrix | Score Options",
    "tools/prioritization-matrix.html": "Free Effort/Impact Prioritization Matrix",
    "tools/wsjf-calculator.html": "Free WSJF Calculator | Prioritization Tool",
    "insights/project-manager-vs-technical-program-manager.html": "PM to TPM: What Actually Changes | Arsenii",
    "insights/compliance-playbook.html": "Compliance PM Playbook | Arsenii Samoilov",
    "insights/ai-adoption.html": "Enterprise AI Adoption at Scale | Arsenii",
    "insights/growth-pm.html": "Growth PM in Practice | Arsenii Samoilov",
    "insights/managing-dependencies-eight-teams.html": "Dependencies Across Eight Teams | Arsenii",
}


def trim_desc(text, max_len=158):
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "."


def update_html(path):
    rel = os.path.relpath(path, BASE)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    orig = html

    desc = DESCRIPTIONS.get(rel)
    if desc is None:
        m = re.search(r'<meta name="description" content="([^"]*)"', html)
        if m and len(m.group(1)) > 160:
            desc = trim_desc(m.group(1))

    if desc:
        html = re.sub(
            r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="' + desc.replace('"', "&quot;") + '"',
            html,
            count=1,
        )
        for prop in ("og:description",):
            pat = r'<meta property="' + prop + r'" content="[^"]*"'
            rep = '<meta property="' + prop + '" content="' + desc.replace('"', "&quot;") + '"'
            if re.search(pat, html):
                html = re.sub(pat, rep, html, count=1)
        pat = r'<meta name="twitter:description" content="[^"]*"'
        if re.search(pat, html):
            html = re.sub(
                pat,
                '<meta name="twitter:description" content="' + desc.replace('"', "&quot;") + '"',
                html,
                count=1,
            )

    title = TITLES.get(rel)
    if title:
        html = re.sub(r"<title>.*?</title>", "<title>" + title + "</title>", html, count=1)
        if re.search(r'<meta property="og:title"', html):
            html = re.sub(
                r'<meta property="og:title" content="[^"]*"',
                '<meta property="og:title" content="' + title.replace('"', "&quot;") + '"',
                html,
                count=1,
            )
        if re.search(r'<meta name="twitter:title"', html):
            html = re.sub(
                r'<meta name="twitter:title" content="[^"]*"',
                '<meta name="twitter:title" content="' + title.replace('"', "&quot;") + '"',
                html,
                count=1,
            )

    if html != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    changed = 0
    for path in glob.glob(os.path.join(BASE, "**/*.html"), recursive=True):
        if "/archive/" in path:
            continue
        if update_html(path):
            changed += 1
            print("updated", os.path.relpath(path, BASE))
    print("done,", changed, "files")


if __name__ == "__main__":
    main()
