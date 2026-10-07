# 🤝 Contribuer à FOKARAT

Merci de votre intérêt pour FOKARAT ! Voici comment contribuer.

## 📋 Code de conduite

En participant, vous acceptez notre [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 🐛 Signaler un bug

1. Vérifiez que le bug n'est pas déjà signalé dans les [issues](https://github.com/amissilwano5-beep/Fokarat/issues).
2. Ouvrez une nouvelle issue avec :
   - Titre clair et descriptif
   - Version de FOKARAT
   - OS et version de Python
   - Étapes de reproduction
   - Comportement attendu vs observé
   - Logs (si possible)

## 💡 Proposer une fonctionnalité

1. Ouvrez une issue avec le tag `enhancement`.
2. Décrivez le problème que ça résout.
3. Proposez une solution.

## 🔧 Soumettre une Pull Request

### Avant de commencer
```bash
# Fork le projet
# Clone votre fork
git clone https://github.com/amissilwano5-beep/Fokarat.git
cd Fokarat

# Créer une branche
git checkout -b feature/ma-fonctionnalite


Développement
Suivez le style de code existant (PEP 8, Black).

Ajoutez des tests pour toute nouvelle fonctionnalité.

Documentez votre code (docstrings).

Vérifiez que tout marche : make test && make lint.

Commit
Utilisez des messages clairs, en français :

git commit -m "feat(modules): ajout du module X"
git commit -m "fix(core): correction du bug Y"

Puis ouvrez une Pull Request sur GitHub avec :

Description claire du changement

Références aux issues liées

Captures d'écran si UI

🎨 Créer un plugin

Le SDK FOKARAT permet d'ajouter des modules sans toucher au cœur.

# plugins/mon_plugin.py
from sdk import PluginBase, PluginMetadata

class MonPlugin(PluginBase):
    @property
    def metadata(self):
        return PluginMetadata(
            name="Mon Plugin",
            version="1.0.0",
            author="Votre Nom",
            description="Description",
            category="misc",
        )

    def run(self, config, args=None):
        print("Hello!")
        return {"status": "success"}

📚 Checklist avant PR
□ Tests passent (make test)
□ Lint OK (make lint)
□ Code formaté (make format)
□ Documentation à jour
□ CHANGELOG mis à jour
□ Pas de secrets hard-codés

