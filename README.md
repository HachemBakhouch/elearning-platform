# Plateforme E-Learning - Système de Quiz Éducatif

Une plateforme d'apprentissage moderne et multilingue développée avec Django 5.2.4 LTS, spécialement conçue pour l'enseignement des mathématiques aux enfants du primaire.

## Fonctionnalités

### Système de Quiz Avancé
- **Modes d'apprentissage** : Entraînement (avec feedback immédiat) et Examen (évaluation)
- **Types de questions** : Choix multiples, Vrai/Faux, Questions ouvertes
- **Questions randomisées** et limitation du nombre de questions par quiz
- **Explanations détaillées** avec astuces de calcul mathématique
- **Suivi de progression** individuel des élèves

### Support Multilingue
- **Français** (langue par défaut)
- **Arabe** (avec support RTL)
- **Anglais**
- Interface d'administration multilingue

### Gestion Pédagogique
- **Catégories par discipline** : Mathématiques, Français, Anglais, Arabe
- **Niveaux scolaires** : 1ère à 6ème année primaire
- **Sous-catégories** : Organisation fine du contenu
- **Statistiques détaillées** : Progression et résultats des élèves
- **Interface d'administration** intuitive pour les enseignants

### Interface Moderne
- **Design responsive** : Compatible mobile, tablette et desktop
- **Thème sombre/clair** automatique
- **Interface utilisateur** adaptée aux enfants
- **Navigation intuitive** par discipline et niveau

## Technologies Utilisées

- **Backend** : Django 5.2.4 LTS (Python 3.13+)
- **Base de données** : SQLite (développement) / PostgreSQL (production)
- **Frontend** : HTML5, CSS3, JavaScript ES6+, Bootstrap 5
- **Images** : Pillow pour le traitement d'images
- **Configuration** : python-decouple pour la gestion des variables d'environnement

## Installation et Configuration

### Prérequis
- Python 3.13+
- Git
- Un éditeur de code (VS Code recommandé)

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/HachemBakhouch/elearning-platform.git
cd elearning-platform
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Activation
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration**
```bash
# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos paramètres
```

5. **Base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

## Accès à l'Application

- **Application** : http://127.0.0.1:8000/
- **Administration** : http://127.0.0.1:8000/admin/

## Structure du Projet

```
elearning_platform/
├── elearning_platform/     # Configuration Django
│   ├── settings.py         # Paramètres de l'application
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuration WSGI
├── quiz/                  # App principale des quiz
│   ├── models.py          # Modèles Quiz, Category, Progress
│   ├── admin.py           # Interface d'administration
│   ├── views.py           # Logique métier
│   └── templates/         # Templates HTML
├── multichoice/           # Questions à choix multiples
├── true_false/            # Questions Vrai/Faux
├── essay/                 # Questions ouvertes
├── static/                # Fichiers statiques (CSS, JS, images)
├── templates/             # Templates globaux
├── media/                 # Fichiers uploadés
├── requirements.txt       # Dépendances Python
└── manage.py             # Gestionnaire Django
```

## Utilisation

### Pour les Enseignants (Administrateurs)

1. **Créer des catégories** : Mathématiques, Français, etc.
2. **Créer des quiz** : Définir titre, description, paramètres
3. **Ajouter des questions** : Choix multiples avec explications
4. **Suivre les progrès** : Consulter les résultats des élèves

### Pour les Élèves

1. **Sélectionner une discipline** : Mathématiques, Français, etc.
2. **Choisir un niveau** : 1ère à 6ème année
3. **Passer un quiz** : Mode entraînement ou examen
4. **Consulter les résultats** : Score et explications détaillées

## Contenu Pédagogique Actuel

### Mathématiques - 4ème Année
- **Tables de multiplication** (1 à 9) avec astuces de calcul
- **Géométrie** (en développement)
- **Fractions simples** (en développement)
- **Problèmes concrets** (en développement)

### Autres Disciplines
- **Français** : Grammaire, conjugaison, vocabulaire (en développement)
- **Arabe** : قواعد، صرف، مفردات (en développement)
- **Anglais** : Grammar, vocabulary, reading (en développement)

## Configuration Avancée

### Variables d'Environnement (.env)

```env
# Sécurité
DEBUG=True
SECRET_KEY=your-secret-key-here

# Base de données
DATABASE_URL=sqlite:///db.sqlite3

# Autorisations
ALLOWED_HOSTS=localhost,127.0.0.1

# Emails (optionnel)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Déploiement en Production

1. **Utiliser PostgreSQL**
2. **Configurer un serveur web** (Nginx + Gunicorn)
3. **SSL/HTTPS** obligatoire
4. **Variables d'environnement** sécurisées
5. **Collecte des fichiers statiques**

```bash
python manage.py collectstatic
```

## Tests

```bash
# Lancer tous les tests
python manage.py test

# Tests spécifiques
python manage.py test quiz.tests
```

## Contribution

1. **Fork** le projet
2. **Créer une branche** (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commit** vos changements (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Créer une Pull Request**

## Roadmap

### Version 1.1 (Prochaine)
- Interface élève moderne avec dashboard
- Système de badges et récompenses
- Export des résultats (PDF, Excel)
- API REST pour application mobile

### Version 1.2 (Future)
- Chat en temps réel entre élèves et enseignants
- Création de quiz collaboratifs
- Intégration vidéo et audio
- Analytics avancées avec graphiques

### Version 2.0 (Vision)
- Intelligence artificielle pour recommandations personnalisées
- Reconnaissance vocale pour les langues
- Réalité augmentée pour la géométrie
- Gamification complète

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteurs

- **Hachem Bakhouch** - *Développeur Principal* - [@HachemBakhouch](https://github.com/HachemBakhouch)

## Remerciements

- Projet original `django-quiz` de Tom Walker pour l'inspiration
- Communauté Django pour l'excellente documentation
- Bootstrap pour les composants UI
- Font Awesome pour les icônes

## Support

- **Issues** : [GitHub Issues](https://github.com/HachemBakhouch/elearning-platform/issues)
- **Documentation** : [Wiki du projet](https://github.com/HachemBakhouch/elearning-platform/wiki)
- **Contact** : [GitHub Profile](https://github.com/HachemBakhouch)