"""
FOKARAT - Calculateur CVSS v3.1
https://www.first.org/cvss/v3.1/specification-document
"""


class CVSS31:
    """
    Calculateur de score CVSS v3.1.

    Exemple :
        cvss = CVSS31(
            av="N", ac="L", pr="N", ui="N",
            s="U", c="H", i="H", a="H"
        )
        cvss.score()      # 9.8
        cvss.severity()   # "CRITICAL"
    """

    AV = {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2}       # Attack Vector
    AC = {"L": 0.77, "H": 0.44}                             # Attack Complexity
    PR_U = {"N": 0.85, "L": 0.62, "H": 0.27}                # Privileges Required (Unchanged)
    PR_C = {"N": 0.85, "L": 0.68, "H": 0.50}                # Privileges Required (Changed)
    UI = {"N": 0.85, "R": 0.62}                             # User Interaction
    CIA = {"N": 0.0, "L": 0.22, "H": 0.56}                  # Confidentiality / Integrity / Availability

    def __init__(self, av="N", ac="L", pr="N", ui="N", s="U", c="H", i="H", a="H"):
        self.av = av
        self.ac = ac
        self.pr = pr
        self.ui = ui
        self.s = s  # Scope: U (Unchanged) / C (Changed)
        self.c = c
        self.i = i
        self.a = a

        # Validations
        if av not in self.AV: raise ValueError(f"AV invalide : {av}")
        if ac not in self.AC: raise ValueError(f"AC invalide : {ac}")
        if ui not in self.UI: raise ValueError(f"UI invalide : {ui}")
        if s not in ("U", "C"): raise ValueError(f"Scope invalide : {s}")
        for v in (c, i, a):
            if v not in self.CIA: raise ValueError(f"CIA invalide : {v}")

    def score(self) -> float:
        """Retourne le score CVSS (0.0 - 10.0)."""
        # Base metrics
        av = self.AV[self.av]
        ac = self.AC[self.ac]
        pr = self.PR_U[self.pr] if self.s == "U" else self.PR_C[self.pr]
        ui = self.UI[self.ui]

        # Impact Sub-Score
        iss = 1 - ((1 - self.CIA[self.c]) * (1 - self.CIA[self.i]) * (1 - self.CIA[self.a]))

        if self.s == "U":
            impact = 6.42 * iss
        else:
            impact = 7.52 * (iss - 0.029) - 3.25 * ((iss - 0.02) ** 15)

        # Exploitability
        exploitability = 8.22 * av * ac * pr * ui

        # Score
        if impact <= 0:
            return 0.0

        if self.s == "U":
            raw = min(impact + exploitability, 10.0)
        else:
            raw = min(1.08 * (impact + exploitability), 10.0)

        # Arrondi supérieur à 0.1
        return round(raw * 10) / 10.0

    def severity(self) -> str:
        """Retourne la sévérité CVSS."""
        s = self.score()
        if s == 0.0: return "NONE"
        if s < 4.0: return "LOW"
        if s < 7.0: return "MEDIUM"
        if s < 9.0: return "HIGH"
        return "CRITICAL"

    def vector(self) -> str:
        """Retourne le vecteur CVSS v3.1."""
        return f"CVSS:3.1/AV:{self.av}/AC:{self.ac}/PR:{self.pr}/UI:{self.ui}/S:{self.s}/C:{self.c}/I:{self.i}/A:{self.a}"

    def to_dict(self) -> dict:
        return {
            "score": self.score(),
            "severity": self.severity(),
            "vector": self.vector(),
            "metrics": {
                "AV": self.av, "AC": self.ac, "PR": self.pr, "UI": self.ui,
                "S": self.s, "C": self.c, "I": self.i, "A": self.a,
            },
        }


# Score de référence pour les vulnérabilités typiques
PRESETS = {
    "rce_unauthenticated": {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "H"},
    "rce_authenticated":   {"av": "N", "ac": "L", "pr": "L", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "H"},
    "sql_injection":       {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "N"},
    "xss_stored":          {"av": "N", "ac": "L", "pr": "L", "ui": "R", "s": "C", "c": "L", "i": "L", "a": "N"},
    "xss_reflected":       {"av": "N", "ac": "L", "pr": "N", "ui": "R", "s": "C", "c": "L", "i": "L", "a": "N"},
    "lfi":                 {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "H", "i": "N", "a": "N"},
    "priv_esc_local":      {"av": "L", "ac": "L", "pr": "L", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "H"},
    "info_disclosure":     {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "L", "i": "N", "a": "N"},
    "auth_bypass":         {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "H"},
    "weak_credentials":    {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "H", "i": "H", "a": "H"},
    "misconfig":           {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "L", "i": "L", "a": "N"},
    "dos":                 {"av": "N", "ac": "L", "pr": "N", "ui": "N", "s": "U", "c": "N", "i": "N", "a": "H"},
}


def from_preset(name: str) -> CVSS31:
    """Crée un CVSS depuis un preset."""
    if name not in PRESETS:
        raise ValueError(f"Preset inconnu : {name}")
    return CVSS31(**PRESETS[name])


def list_presets():
    """Liste tous les presets disponibles."""
    return [{"id": k, "vector": CVSS31(**v).vector(), "score": CVSS31(**v).score(),
             "severity": CVSS31(**v).severity()} for k, v in PRESETS.items()]