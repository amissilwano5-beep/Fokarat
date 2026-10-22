"""
FOKARAT - Générateur de rapports PDF
Utilise reportlab si disponible, sinon fallback HTML.
"""
import os
import json
from datetime import datetime

from core.logger import Logger
from modules.reporting.findings import findings_manager
from modules.reporting.cvss import CVSS31

logger = Logger()


class PDFReportGenerator:
    """
    Génère un rapport PDF professionnel avec :
    - Page de couverture
    - Executive Summary
    - Statistiques
    - Findings détaillés (avec CVSS)
    - Recommandations
    - Mapping MITRE ATT&CK
    """

    def __init__(self, client_name="Client", assessor="FOKAS", scope="Non spécifié"):
        self.client_name = client_name
        self.assessor = assessor
        self.scope = scope
        self.date = datetime.now().strftime("%Y-%m-%d")

    def generate(self, output_path="output/fokarat_report.pdf") -> str:
        """Génère le rapport (PDF si reportlab, sinon HTML)."""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import cm
            from reportlab.lib import colors
            from reportlab.platypus import (
                SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                Table, TableStyle
            )
            return self._generate_pdf(output_path)
        except ImportError:
            logger.warning("reportlab absent. Génération HTML à la place.")
            logger.info("Installe : pip install reportlab")
            return self._generate_html(output_path.replace(".pdf", ".html"))

    def _generate_pdf(self, output_path):
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, PageBreak,
            Table, TableStyle
        )

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                leftMargin=2*cm, rightMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        # ─── Styles custom
        title_style = ParagraphStyle(
            "TitleFokas", parent=styles["Title"],
            fontSize=28, textColor=colors.HexColor("#0C6B4E"),
            spaceAfter=20, alignment=1,
        )
        h1_style = ParagraphStyle(
            "H1Fokas", parent=styles["Heading1"],
            fontSize=20, textColor=colors.HexColor("#0C6B4E"),
            spaceAfter=12, spaceBefore=20,
        )
        h2_style = ParagraphStyle(
            "H2Fokas", parent=styles["Heading2"],
            fontSize=14, textColor=colors.HexColor("#0C6B4E"),
            spaceAfter=8, spaceBefore=12,
        )
        body_style = styles["BodyText"]

        # ─── PAGE DE COUVERTURE
        story.append(Spacer(1, 4*cm))
        story.append(Paragraph("FOKARAT", title_style))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph("<b>Rapport de Test d'Intrusion</b>",
                                ParagraphStyle("Sub", parent=styles["Heading2"],
                                              alignment=1, fontSize=16, textColor=colors.grey)))
        story.append(Spacer(1, 3*cm))
        cover_data = [
            ["Client", self.client_name],
            ["Auditeur", self.assessor],
            ["Date", self.date],
            ["Scope", self.scope],
            ["Framework", "FOKARAT v4.0"],
        ]
        cover_table = Table(cover_data, colWidths=[5*cm, 10*cm])
        cover_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#0C6B4E")),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        story.append(cover_table)
        story.append(PageBreak())

        # ─── EXECUTIVE SUMMARY
        story.append(Paragraph("1. Executive Summary", h1_style))
        stats = findings_manager.stats()

        summary_text = (
            f"Ce rapport présente les résultats du test d'intrusion réalisé sur "
            f"<b>{self.client_name}</b> par <b>{self.assessor}</b> le <b>{self.date}</b>. "
            f"Au total, <b>{stats['total']}</b> vulnérabilité(s) ont été identifiée(s), "
            f"avec un score CVSS moyen de <b>{stats['average_score']}</b>. "
            f"Le niveau de risque global est estimé à "
            f"<b>{self._global_risk(stats)}</b>."
        )
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 0.5*cm))

        # Table de sévérité
        sev_data = [
            ["Sévérité", "Nombre", "Description"],
            ["CRITICAL", str(stats["critical"]), "Correction immédiate requise"],
            ["HIGH", str(stats["high"]), "Correction prioritaire"],
            ["MEDIUM", str(stats["medium"]), "Correction planifiée"],
            ["LOW", str(stats["low"]), "Amélioration recommandée"],
            ["NONE", str(stats["none"]), "Informationnel"],
        ]
        sev_table = Table(sev_data, colWidths=[3*cm, 2.5*cm, 9.5*cm])
        sev_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0C6B4E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FFEBEE")),
            ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#FFF3E0")),
            ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FFFDE7")),
            ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor("#E8F5E9")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ]))
        story.append(sev_table)
        story.append(PageBreak())

        # ─── FINDINGS DÉTAILLÉS
        story.append(Paragraph("2. Vulnérabilités détaillées", h1_style))
        story.append(Spacer(1, 0.3*cm))

        if not findings_manager.findings:
            story.append(Paragraph("<i>Aucune vulnérabilité enregistrée.</i>", body_style))
        else:
            sorted_findings = sorted(findings_manager.findings,
                                     key=lambda f: f.score, reverse=True)
            for i, f in enumerate(sorted_findings, 1):
                story.append(Paragraph(f"2.{i} {f.title}", h2_style))

                # Table info
                info_data = [
                    ["ID", f.id, "Sévérité", f.severity],
                    ["Score CVSS", f"{f.score} / 10", "Cible", f.target or "N/A"],
                    ["Vecteur", f.cvss.vector(), "", ""],
                ]
                info_table = Table(info_data, colWidths=[3*cm, 5*cm, 3*cm, 4*cm])
                info_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F5E9")),
                    ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#E8F5E9")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("PADDING", (0, 0), (-1, -1), 4),
                    ("SPAN", (1, 2), (3, 2)),
                ]))
                story.append(info_table)
                story.append(Spacer(1, 0.3*cm))

                if f.description:
                    story.append(Paragraph("<b>Description</b>", body_style))
                    story.append(Paragraph(f.description, body_style))
                    story.append(Spacer(1, 0.2*cm))

                if f.evidence:
                    story.append(Paragraph("<b>Preuve</b>", body_style))
                    story.append(Paragraph(
                        f"<font face='Courier' size=8>{self._escape(f.evidence[:1000])}</font>",
                        body_style
                    ))
                    story.append(Spacer(1, 0.2*cm))

                if f.remediation:
                    story.append(Paragraph("<b>Recommandation</b>", body_style))
                    story.append(Paragraph(f.remediation, body_style))
                    story.append(Spacer(1, 0.2*cm))

                if f.mitre_technique:
                    story.append(Paragraph(
                        f"<b>MITRE ATT&CK :</b> {f.mitre_technique}", body_style))
                    story.append(Spacer(1, 0.2*cm))

                if f.references:
                    story.append(Paragraph("<b>Références</b>", body_style))
                    for r in f.references:
                        story.append(Paragraph(f"• {r}", body_style))

                story.append(Spacer(1, 0.5*cm))

        # ─── RECOMMANDATIONS GLOBALES
        story.append(PageBreak())
        story.append(Paragraph("3. Recommandations globales", h1_style))
        recs = self._global_recommendations(stats)
        for r in recs:
            story.append(Paragraph(f"• {r}", body_style))

        # ─── FOOTER
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(
            f"<i>Rapport généré par FOKARAT — {self.date} — "
            f"Usage éducatif et tests autorisés uniquement.</i>",
            ParagraphStyle("Footer", parent=body_style, fontSize=8,
                           textColor=colors.grey, alignment=1)
        ))

        doc.build(story)
        logger.success(f"Rapport PDF généré : {output_path}")
        return output_path

    def _generate_html(self, output_path):
        """Fallback HTML si reportlab absent."""
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        stats = findings_manager.stats()
        findings = findings_manager.list_all()

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Rapport FOKARAT - {self.client_name}</title>
<style>
    body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 2em auto;
            color: #333; line-height: 1.6; }}
    h1 {{ color: #0C6B4E; border-bottom: 2px solid #0C6B4E; padding-bottom: 0.3em; }}
    h2 {{ color: #0C6B4E; margin-top: 1.5em; }}
    table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
    th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
    th {{ background: #0C6B4E; color: white; }}
    .critical {{ background: #FFEBEE; }}
    .high {{ background: #FFF3E0; }}
    .medium {{ background: #FFFDE7; }}
    .low {{ background: #E8F5E9; }}
    .footer {{ color: #888; font-size: 0.85em; margin-top: 3em; text-align: center; }}
    code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
</style>
</head>
<body>
<h1>FOKARAT — Rapport de Test d'Intrusion</h1>
<table>
    <tr><th>Client</th><td>{self.client_name}</td></tr>
    <tr><th>Auditeur</th><td>{self.assessor}</td></tr>
    <tr><th>Date</th><td>{self.date}</td></tr>
    <tr><th>Scope</th><td>{self.scope}</td></tr>
</table>

<h1>1. Executive Summary</h1>
<p>Total : <b>{stats['total']}</b> vulnérabilité(s).
Score CVSS moyen : <b>{stats['average_score']}</b>.
Niveau de risque : <b>{self._global_risk(stats)}</b>.</p>

<table>
    <tr><th>Sévérité</th><th>Nombre</th></tr>
    <tr class="critical"><td>CRITICAL</td><td>{stats['critical']}</td></tr>
    <tr class="high"><td>HIGH</td><td>{stats['high']}</td></tr>
    <tr class="medium"><td>MEDIUM</td><td>{stats['medium']}</td></tr>
    <tr class="low"><td>LOW</td><td>{stats['low']}</td></tr>
</table>

<h1>2. Vulnérabilités</h1>
"""
        for i, f in enumerate(sorted(findings, key=lambda x: x["score"], reverse=True), 1):
            html += f"""
<h2>2.{i} {f['title']}</h2>
<table>
    <tr><th>ID</th><td>{f['id']}</td><th>Sévérité</th><td>{f['severity']}</td></tr>
    <tr><th>Score</th><td>{f['score']}/10</td><th>Cible</th><td>{f['target'] or 'N/A'}</td></tr>
    <tr><th>Vecteur</th><td colspan="3"><code>{f['vector']}</code></td></tr>
</table>
<p><b>Description :</b> {f['description']}</p>
<p><b>Preuve :</b> <code>{f['evidence'][:500]}</code></p>
<p><b>Recommandation :</b> {f['remediation']}</p>
"""

        html += f"""
<h1>3. Recommandations globales</h1>
<ul>
"""
        for r in self._global_recommendations(stats):
            html += f"<li>{r}</li>\n"
        html += """
</ul>
<p class="footer">Rapport généré par FOKARAT — Usage éducatif uniquement.</p>
</body>
</html>
"""
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write(html)
        logger.success(f"Rapport HTML généré : {output_path}")
        return output_path

    def _global_risk(self, stats):
        if stats["critical"] > 0: return "CRITIQUE"
        if stats["high"] > 0: return "ÉLEVÉ"
        if stats["medium"] > 0: return "MOYEN"
        if stats["low"] > 0: return "FAIBLE"
        return "INFORMATIF"

    def _global_recommendations(self, stats):
        recs = []
        if stats["critical"] > 0:
            recs.append("<b>Correction immédiate</b> : traiter toutes les vulnérabilités CRITICAL sous 24-48h.")
        if stats["high"] > 0:
            recs.append("<b>Priorité haute</b> : corriger les vulnérabilités HIGH sous 1-2 semaines.")
        if stats["medium"] > 0:
            recs.append("<b>Planification</b> : intégrer les vulnérabilités MEDIUM dans le prochain cycle de patch.")
        recs.append("Mettre en place un <b>programme de tests réguliers</b> (au moins trimestriel).")
        recs.append("Former les développeurs aux <b>bonnes pratiques de sécurité</b> (OWASP Top 10).")
        recs.append("Déployer un <b>WAF</b> et un <b>SIEM</b> pour la détection en temps réel.")
        recs.append("Établir un <b>plan de réponse aux incidents</b> documenté et testé.")
        return recs

    def _escape(self, text):
        """Échappe les caractères spéciaux pour ReportLab."""
        return (text.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))


class ExecutiveReport:
    """Rapport court (1 page) pour le management."""

    def __init__(self, client_name="Client", assessor="FOKAS"):
        self.client_name = client_name
        self.assessor = assessor
        self.date = datetime.now().strftime("%Y-%m-%d")

    def generate_markdown(self, output_path="output/executive_summary.md"):
        stats = findings_manager.stats()
        lines = [
            f"# Executive Summary — {self.client_name}",
            "",
            f"**Auditeur** : {self.assessor}  ",
            f"**Date** : {self.date}  ",
            f"**Niveau de risque global** : **{self._risk(stats)}**",
            "",
            "## Statistiques",
            "",
            "| Sévérité | Nombre |",
            "|----------|--------|",
            f"| CRITICAL | {stats['critical']} |",
            f"| HIGH | {stats['high']} |",
            f"| MEDIUM | {stats['medium']} |",
            f"| LOW | {stats['low']} |",
            f"| **Total** | **{stats['total']}** |",
            "",
            f"**Score CVSS moyen** : {stats['average_score']} / 10",
            "",
            "## Top 3 vulnérabilités critiques",
            "",
        ]
        top = sorted(findings_manager.findings, key=lambda f: f.score, reverse=True)[:3]
        for i, f in enumerate(top, 1):
            lines.append(f"{i}. **{f.title}** ({f.severity} - CVSS {f.score}) — cible : {f.target}")

        lines += ["", "## Actions recommandées", ""]
        for r in PDFReportGenerator()._global_recommendations(stats):
            clean = r.replace("<b>", "**").replace("</b>", "**")
            lines.append(f"- {clean}")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        logger.success(f"Executive summary : {output_path}")
        return output_path

    def _risk(self, stats):
        if stats["critical"] > 0: return "CRITIQUE"
        if stats["high"] > 0: return "ÉLEVÉ"
        if stats["medium"] > 0: return "MOYEN"
        if stats["low"] > 0: return "FAIBLE"
        return "INFORMATIF"