---
title: README

---

# 🎟️ JO Tickets

> **Application de gestion des billets pour les compétitions de football des JO Paris 2024.**

---

## 🚀 Présentation du projet

Ce projet est une application de gestion des billets pour les compétitions de football des JO. Il comprend trois composants principaux :

1. **🔧 Backend Django** : Gestion de la base de données, API REST et interface d'administration.
2. **📱 Application Mobile** : Interface web permettant aux supporters de consulter les matchs et d'acheter des billets.
3. **📷 Scanner de billets** : Application permettant aux stadiers de vérifier la validité des billets via QR code.

---

## ✅ Prérequis

- 🐍 **Python 3.8+**
- 📦 **MySQL** ou autre SGBD compatible
- 🌐 Navigateur web moderne
- 🛠️ Extension **LiveServer** pour VSCode (ou serveur équivalent)

---

## ⚙️ Installation et démarrage

### 📥 Cloner le projet

```bash
git clone https://github.com/esiee-it-slam-2025/dabo_elijah.git
cd Projet-JO-Ticket
```

### 📚 Installation des dépendances

```bash
pip install django
django-cors-headers
djangorestframework
```

### 💾 Configuration de la base de données

Si vous utilisez phpMyAdmin (recommandé) :

- Connectez-vous à phpMyAdmin
- Sélectionnez votre base de données `jo_projet`
- Cliquez sur l'onglet **Importer**
- Sélectionnez le fichier `data_jo.sql`
- Cliquez sur **Exécuter**


### 🗂️ Préparation de la base de données

```bash
cd admin
python manage.py makemigrations
python manage.py makemigrations mainapp
python manage.py migrate
```

### 📥 Import des données initiales

```bash
# Pour MySQL
mysql -u username -p jo_projet < data_jo.sql
```

### 👤 Création d'un superutilisateur

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte administrateur.

### 🚦 Lancer le serveur backend

```bash
python manage.py runserver
```

Le serveur backend sera accessible à l'adresse : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 📱 Lancer l'application mobile et le scanner

Utilisez l'extension LiveServer de VSCode :

- Ouvrez le dossier dans VSCode
- Cliquez-droit sur `mobile/index.html` et `scanner/index.html`
- Sélectionnez **Open with Live Server**

---

## 📖 Guide d'utilisation

### 🛠️ Interface d'administration

- Accédez à [http://127.0.0.1:8000/admin-matches/](http://127.0.0.1:8000/admin-matches/)
- Connectez-vous avec le superutilisateur créé
- Gérez les dates, lieux, équipes et scores des matchs

Admin Django standard : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### 📱 Application mobile

- Accédez à l'URL fournie par LiveServer (ex : [http://127.0.0.1:5500/mobile/index.html](http://127.0.0.1:5500/mobile/index.html))
- Inscrivez-vous, connectez-vous et parcourez les matchs
- Achetez des billets (Silver, Gold, Platinum)
- Consultez vos billets et téléchargez les QR codes

### 🎫 Scanner de billets

- Accédez au scanner via l'URL LiveServer (ex : [http://127.0.0.1:5500/scanner/index.html](http://127.0.0.1:5500/scanner/index.html))
- Utilisez la caméra ou uploadez un QR code
- Vérifiez et validez les billets

---

## 📁 Structure du projet

```
Projet-JO-Ticket/
├── README.md
├── data_jo.sql                  # Données initiales
├── admin/                       # Backend Django
│   ├── manage.py
│   ├── admin/                   # Configuration
│   └── mainapp/                 # Application principale
│       ├── models/
│       ├── views/
│       ├── settings/
│       ├── templates/
│       └── static/
├── mobile/                      # Application mobile
│   ├── index.html
│   ├── auth.html
│   ├── my-tickets.html
│   ├── ticket-purchase.html
│   └── assets/
└── scanner/                     # Scanner de billets
    ├── index.html
    └── assets/
```

---

## 🌟 Fonctionnalités

### 🔧 Backend Django
- API REST complète
- Authentification
- Administration personnalisée
- Validation des billets

### 📱 Application mobile
- Inscription, connexion
- Achat billets (Silver 100€, Gold 200€, Platinum 300€)
- Génération QR codes
- Consultation des billets

### 📷 Scanner de billets
- Scan QR codes via caméra ou image
- Vérification validité
- Informations détaillées
- Validation entrée stade

---

## 🛠️ Dépannage

- **CORS** : Vérifiez les paramètres dans `settings/base.py`
- **Scan QR** : Préférez des identifiants courts
- **API introuvable** : Vérifiez le serveur backend

---

## 🛠️ Technologies utilisées

- 🐍 **Backend** : Django, Django REST Framework, cors-headers
- 🌐 **Frontend** : HTML5, CSS3, JavaScript (vanilla)
- 📷 **QR Code** : jsQR (lecture)
- 💽 **Base de données** : PhpMyAdmin (recommandé)

---
