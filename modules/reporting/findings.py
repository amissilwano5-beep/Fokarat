"""
FOKARAT - Gestionnaire de findings (vulnérabilités)
"""
import os
import json
import uuid
from datetime import datetime

from core.logger import Logger
from modules.reporting.cvss import CVSS31, from_preset

logger = Logger()


class Finding:
    """Représente une vulnérabilité trouvée."""

    def __init__(self, title, severity=None, cvss_preset=None, cvss_custom=None,
                 description="", evidence="", remediation="", references=None,
                 mitre_technique=None, target="", category="generic"):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.evidence = evidence
        self.remediation = remediation
        self.references = references or []
        self.mitre_technique = mitre_technique
        self.target = target
        self.category = category
        self.discovered_at = datetime.utcnow().isoformat() + "Z"

        # Calcul CVSS
        if cvss_custom:
            self.cvss = CVSS31(**cvss_custom)
        elif cvss_preset:
            self.cvss = from_preset(cvss_preset)
        elif severity:
            # Mappe sévérité texte vers preset
            mapping = {
                "CRITICAL": "rce_unauthenticated",
                "HIGH": "sql_injection",
                "MEDIUM": "xss_stored",
                "LOW": "info_disclosure",
                "INFO": "misconfig",
            }
            self.cvss = from_preset(mapping.get(severity.upper(), "misconfig"))
        else:
            self.cvss = from_preset("misconfig")

    @property
    def severity(self):
        return self.cvss.severity()

    @property
    def score(self):
        return self.cvss.score()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "severity": self.severity,
            "score": self.score,
            "vector": self.cvss.vector(),
            "category": self.category,
            "target": self.target,
            "description": self.description,
            "evidence": self.evidence,
            "remediation": self.remediation,
            "references": self.references,
            "mitre_technique": self.mitre_technique,
            "discovered_at": self.discovered_at,
        }


class FindingsManager:
    """Gestionnaire global des findings."""

    FILE = "output/findings.json"

    def __init__(self):
        self.findings = []
        self._load()

    def add(self, finding: Finding) -> Finding:
        self.findings.append(finding)
        logger.success(f"Finding ajouté : [{finding.severity}] {finding.title}")
        self._save()
        return finding

    def add_from_dict(self, data: dict) -> Finding:
        f = Finding(
            title=data.get("title", "Sans titre"),
            description=data.get("description", ""),
            evidence=data.get("evidence", ""),
            remediation=data.get("remediation", ""),
            references=data.get("references", []),
            mitre_technique=data.get("mitre_technique"),
            target=data.get("target", ""),
            category=data.get("category", "generic"),
            cvss_preset=data.get("cvss_preset"),
            cvss_custom=data.get("cvss_custom"),
            severity=data.get("severity"),
        )
        return self.add(f)

    def remove(self, finding_id: str) -> bool:
        for i, f in enumerate(self.findings):
            if f.id == finding_id:
                self.findings.pop(i)
                self._save()
                return True
        return False

    def list_all(self) -> list:
        return [f.to_dict() for f in self.findings]

    def by_severity(self) -> dict:
        out = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": [], "NONE": []}
        for f in self.findings:
            out[f.severity].append(f.to_dict())
        return out

    def stats(self) -> dict:
        sev = self.by_severity()
        return {
            "total": len(self.findings),
            "critical": len(sev["CRITICAL"]),
            "high": len(sev["HIGH"]),
            "medium": len(sev["MEDIUM"]),
            "low": len(sev["LOW"]),
            "none": len(sev["NONE"]),
            "average_score": round(
                sum(f.score for f in self.findings) / len(self.findings), 1
            ) if self.findings else 0.0,
        }

    def _save(self):
        try:
            data = [f.to_dict() for f in self.findings]
            os.makedirs("output", exist_ok=True)
            with open(self.FILE, "w", encoding="utf-8") as fh:
                json.dump(data, fh, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erreur sauvegarde findings : {e}")

    def _load(self):
        if not os.path.exists(self.FILE):
            return
        try:
            with open(self.FILE, "r", encoding="utf-8") as fh:
                data = json.load(fh)
                for d in data:
                    f = Finding(
                        title=d["title"],
                        description=d.get("description", ""),
                        evidence=d.get("evidence", ""),
                        remediation=d.get("remediation", ""),
                        references=d.get("references", []),
                        mitre_technique=d.get("mitre_technique"),
                        target=d.get("target", ""),
                        category=d.get("category", "generic"),
                    )
                    f.cvss = CVSS31(**d["metrics"]) if "metrics" in d else from_preset("misconfig")
                    f.id = d.get("id", f.id)
                    self.findings.append(f)
            logger.info(f"{len(self.findings)} finding(s) chargé(s)")
        except Exception as e:
            logger.warning(f"Erreur chargement findings : {e}")


findings_manager = FindingsManager()