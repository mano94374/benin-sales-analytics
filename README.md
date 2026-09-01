# 🇧🇯 Benin Sales Analytics

## 📊 Présentation du projet

**Benin Sales Analytics** est un projet d'analyse de données commerciales réalisé avec Python.

L'objectif est d'analyser les ventes d'une entreprise au Bénin afin d'identifier les produits les plus performants, les villes générant le plus de chiffre d'affaires et l'évolution des ventes au cours du temps.

Le projet comprend également un dashboard interactif permettant de visualiser les principaux indicateurs commerciaux.

---

## 🎯 Objectifs

Ce projet permet de :

* Nettoyer et contrôler les données de ventes
* Calculer le chiffre d'affaires
* Analyser les performances des produits
* Analyser les performances des villes
* Étudier l'évolution mensuelle du chiffre d'affaires
* Identifier les valeurs potentiellement aberrantes
* Calculer plusieurs KPI commerciaux
* Produire des graphiques d'analyse
* Générer un rapport Excel
* Créer un dashboard interactif avec Streamlit

---

## 🗂️ Structure du projet

```text
benin-sales-analytics/
│
├── data/
│   └── ventes.csv
│
├── outputs/
│   ├── Benin_Sales_Analytics.xlsx
│   ├── resume_produits.xlsx
│   └── charts/
│
├── src/
│   ├── analysis.py
│   └── dashboard.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠️ Technologies utilisées

* **Python**
* **Pandas** — manipulation et analyse des données
* **Matplotlib** — visualisation des données
* **Plotly** — graphiques interactifs
* **Streamlit** — création du dashboard
* **Excel** — export et présentation des résultats
* **Git / GitHub** — gestion et partage du projet

---

## 📈 Principaux résultats

L'analyse porte sur **12 ventes**.

### KPI principaux

| Indicateur               |       Résultat |
| ------------------------ | -------------: |
| Chiffre d'affaires total | 5 496 000 FCFA |
| Quantité totale vendue   |             86 |
| Panier moyen             |   458 000 FCFA |
| Produit n°1              |     Ordinateur |
| CA du produit n°1        | 2 700 000 FCFA |
| Ville n°1                |        Cotonou |
| CA de Cotonou            | 2 260 000 FCFA |
| Meilleur mois            |   Février 2026 |
| CA du meilleur mois      | 2 466 000 FCFA |

### Performance des produits

L'ordinateur génère près de **49,1 % du chiffre d'affaires total**, tandis que la souris représente le plus grand volume de ventes mais une contribution beaucoup plus faible au chiffre d'affaires.

Cela montre qu'un produit vendu en grande quantité n'est pas nécessairement celui qui génère le plus de revenus.

### Performance des villes

**Cotonou** est la ville générant le plus de chiffre d'affaires avec environ **41,1 % du CA total**, suivie d'**Abomey-Calavi** avec environ **34,4 %**.

### Évolution mensuelle

Le chiffre d'affaires évolue de la manière suivante :

* Janvier : **2 030 000 FCFA**
* Février : **2 466 000 FCFA**
* Mars : **1 000 000 FCFA**

Le chiffre d'affaires augmente de janvier à février, puis diminue fortement en mars.

L'analyse montre notamment qu'aucune vente d'ordinateur n'est enregistrée en mars, alors que l'ordinateur est le produit contribuant le plus au chiffre d'affaires.

---

## 📊 Dashboard

Le projet contient un dashboard interactif développé avec **Streamlit** permettant de filtrer les données par :

* Ville
* Produit

et de visualiser notamment :

* Le chiffre d'affaires total
* Les unités vendues
* Le CA moyen par vente
* Le produit le plus performant
* Le CA par produit
* Le CA par ville

---

## 🔍 Contrôle et qualité des données

Plusieurs contrôles ont été réalisés :

* Vérification des valeurs manquantes
* Vérification des doublons
* Vérification des produits et catégories
* Vérification des villes
* Vérification des valeurs minimales et maximales
* Vérification des quantités et prix négatifs ou nuls
* Contrôle de la cohérence des dates
* Détection des valeurs aberrantes avec la méthode IQR
* Vérification du calcul du chiffre d'affaires

Aucune valeur manquante, aucun doublon et aucune valeur négative ou nulle n'ont été détectés dans les données analysées.

---

## 🚀 Installation

Cloner le projet :

```bash
git clone https://github.com/mano94374/benin-sales-analytics.git
cd benin-sales-analytics
```

Créer un environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## ▶️ Exécution de l'analyse

```bash
python3 src/analysis.py
```

---

## 📊 Lancer le dashboard

```bash
streamlit run src/dashboard.py
```

Le dashboard sera ensuite accessible depuis le navigateur.

---

## 👨‍💻 Auteur

**Emmanuel**

Projet réalisé dans le cadre de mon apprentissage en **Data Analytics**.

