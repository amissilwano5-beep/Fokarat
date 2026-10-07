# 🔐 Politique de Sécurité - FOKARAT

## Versions supportées

Nous supportons activement les versions suivantes avec des mises à jour de sécurité :

| Version | Supportée          |
|---------|--------------------|
| 3.x.x   | ✅ Oui             |
| 2.x.x   | ⚠️ Correctifs uniquement |
| 1.x.x   | ❌ Non             |

## 🚨 Signaler une vulnérabilité

Nous prenons toutes les vulnérabilités au sérieux. Si vous découvrez une faille **dans FOKARAT lui-même** (pas dans les outils externes), voici la procédure :

### ❌ NE PAS FAIRE
- ❌ **Ne PAS** ouvrir une issue publique sur GitHub.
- ❌ **Ne PAS** divulguer la vulnérabilité sur les réseaux sociaux.
- ❌ **Ne PAS** exploiter la faille au-delà de la preuve de concept.

### ✅ À FAIRE
1. Envoyer un email chiffré (PGP si possible) à : **amissilwano5@gmail.com**
2. Sujet : `[SECURITY] Vulnérabilité dans FOKARAT`
3. Inclure dans votre rapport :
   - Description détaillée de la vulnérabilité
   - Étapes de reproduction (PoC minimal)
   - Version impactée
   - Impact potentiel (CVSS si possible)
   - Votre nom/handle (optionnel, pour le crédit)

### ⏱️ Délais de réponse
- **48 heures** : Accusé de réception
- **7 jours** : Évaluation initiale et plan de correctif
- **30 jours** : Correctif publié (selon complexité)

## 🎁 Reconnaissance

Les chercheurs qui signalent des vulnérabilités de manière responsable seront :

- Crédités dans le fichier `SECURITY_HALL_OF_FAME.md`
- Mentionnés dans les release notes
- (Optionnel) Contactés pour co-auteur d'un avis de sécurité

## 🔒 Bonnes pratiques de sécurité pour les utilisateurs

### Pour les utilisateurs de FOKARAT

1. **Ne jamais exposer** l'API REST sur Internet sans authentification.
2. **Utiliser un environnement isolé** (VM, sandbox) pour les tests.
3. **Protéger vos payloads** avec un chiffrement fort.
4. **Ne jamais committer** vos clés API, tokens ou keystores.
5. **Vérifier les dépendances** régulièrement (`pip-audit`, `safety`).
6. **Mettre à jour FOKARAT** dès qu'une nouvelle version sort.

### Pour les contributeurs

1. **Signer vos commits** avec GPG : `git commit -S`
2. **Ne pas inclure** de secrets dans le code.
3. **Suivre les guidelines** de contribution.
4. **Tester** les modules de sécurité en local.

## 🛡️ Mécanismes de sécurité intégrés

FOKARAT intègre plusieurs couches de sécurité :

| Mécanisme | Statut | Description |
|-----------|--------|-------------|
| Validation de scope | ✅ | Vérifie l'autorisation avant chaque attaque |
| Mode dry-run | ✅ | Simule les attaques sans exécuter |
| Kill switch | ✅ | Arrêt d'urgence via signal |
| Logs d'audit | ✅ | Chaque action est enregistrée |
| Chiffrement secrets | ⚠️ En cours | Chiffrement AES des credentials |
| Sandbox | ❌ Planifié | Isolation des payloads |
| Auth API | ❌ Planifié | JWT pour l'API REST |

## 📋 Historique des vulnérabilités

| CVE | Version | Sévérité | Statut | Date |
|-----|---------|----------|--------|------|
| Aucune à ce jour | - | - | - | - |

## 📞 Contact

- 📧 Email : **amissilwano5@gmail.com**
- 🔗 GitHub Security : https://github.com/amissilwano5-beep/Fokarat/security
- 💬 Discussions : https://github.com/amissilwano5-beep/Fokarat/discussions

---

**Merci de contribuer à la sécurité de FOKARAT et de la communauté.**