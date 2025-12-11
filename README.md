# 📊 Prédiction de la Réussite des Étudiants

**Projet Data - GR3**

## 👥 Équipe
- Brendan ROBIN
- Noémie PETAT
- Antoine GEZE
- Augustin OWCA

**Quel est le contexte ?**

En tant qu'étudiant, nous voulons avoir ce qui impact la réussite scolaire. Ce projet vise à développer un modèle de prédiction permettant d'identifier les facteurs influençant la réussite académique des étudiants et de prédire leur performance.

**Quelle est la proposition de valeur ? Pourquoi ? Quels types de problèmes cela résout-il ?**

Notre projet apporte une meilleure compréhension des éléments qui influencent la réussite, ce qui peut aider à repérer les étudiants en difficulté et à cibler les actions d’accompagnement. Il répond au manque d’outils objectifs pour analyser la performance et propose une approche data simple pour éclairer les décisions pédagogiques.

**A-t-on réellement besoin de machine learning ? Ou une simple heuristique suffit-elle ?**

On va d'abord commencer par une heuristique, qui pourrait fonctionner. Mais comme il y a énormement de facteurs qui interagissent entre eux, le machine learning nous permettra d'élaborer des modèles plus complexes et plus  fiables. Il permet de capturer des relations que des règles manuelles ne pourraient pas repérer facilement

**Quels sont les différents objectifs ?**

L’objectif est de prédire la performance des étudiants et de comprendre les variables les plus importantes. Nous voulons aussi comparer plusieurs modèles simples et expliquer clairement nos résultats pour montrer comment les données peuvent aider à améliorer la réussite scolaire.

**Quelle est votre solution pour adresser ce problème ?**

Notre solution consiste à analyser le dataset, préparer les données, tester plusieurs modèles de prédiction, puis choisir celui qui fonctionne le mieux. Enfin, nous interprétons les résultats pour identifier les facteurs les plus influents et proposer une conclusion simple et compréhensible.


## 🚀 Installation en Local

### Étape 1 : Télécharger le Projet
1. Cliquer sur **Code** → **Download ZIP**
2. Extraire le dossier dans `Documents`
3. Ouvrir **VS Code** → **File** → **Open Folder** → sélectionner le dossier téléchargé

### Étape 2 : Configurer Git (première fois)
Installer **Git Bash** si ce n'est pas déjà fait

Ouvrir le terminal dans VS Code et sélectionner **Git Bash** (dans le menu "+" en haut à droite du terminal), puis exécuter :

```bash
git config --global user.email votreemailgithub@gmail.com
```

```bash
git config --global user.name votrenomusergithub
```

---

## 📝 Gestion du Code avec Git

### Workflow de Collaboration

#### 1. **Récupérer les dernières modifications**
```bash
git pull https://github.com/AugustinO28/Projet_Data_GR3.git
```

#### 2. **Créer une nouvelle branche**
Nommez la branche en relation avec vos modifications :
```bash
git checkout -b nom-descriptif-de-la-branche
```
*(Le nom de la branche apparaît dans le terminal)*

#### 3. **Faire vos modifications**
- Développez votre code
- Testez vos changements pour vous assurer qu'ils fonctionnent
- Sauvegardez vos fichiers (Ctrl+S)

#### 4. **Vérifier vos changements**
- Allez dans l'onglet **Source Control** (menu gauche de VS Code)
- Vous verrez tous vos changements listés

#### 5. **Committer vos changements**
- Cliquez sur le **+** pour ajouter les fichiers modifiés
- Écrivez un **message de commit** explicite décrivant vos changements
- Cliquez sur **Commit**

#### 6. **Publier vos changements**
- Cliquez sur **Sync Changes** pour pousser vos modifications sur GitHub

#### 7. **Fusionner votre branche**
Une fois votre travail terminé et validé :
- Allez sur **GitHub**
- Créez une **Pull Request** (PR)
- Faites **Merge** de votre branche vers `main` après révision
