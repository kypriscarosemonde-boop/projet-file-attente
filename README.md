# Simulation de File d’Attente M/M/c avec Interface Graphique

##  Objectif du projet

Ce projet a pour objectif de modéliser et simuler un système de file d’attente de type **M/M/c** (arrivées de Poisson, services exponentiels, plusieurs serveurs) à l’aide d’une **application Python avec interface graphique**.

Il permet d’analyser les performances d’un système réel (banque, supermarché, etc.) afin d’optimiser :

* le nombre de serveurs
* le temps d’attente des clients
* la charge du système



## Concepts théoriques

Le modèle **M/M/c** repose sur :

* **λ (lambda)** : taux d’arrivée des clients
* **μ (mu)** : taux de service
* **c** : nombre de serveurs
* **ρ = λ / (c × μ)** : taux d’occupation

###  Interprétation :

* ρ < 1 → système **stable**
* ρ ≥ 1 → système **instable**



## Architecture du projet

projet_files_attente/
│
├── login.py
├── dashboard.py
├── simulation.py
├── main.py
├── users.json
├── requirements.txt
└── tests/
└── test_simulation.py



## Authentification

### Identifiants par défaut :

* Username : **admin**
* Password : **admin123**



##  Installation

### 1. Cloner le projet

git clone https://github.com/kypriscarosemonde-boop/projet-file-attente.git
cd projet-file-attente

### 2. Installer les dépendances

pip install -r requirements.txt



## Exécution

Lancer l’application avec :

python login.py



## Fonctionnalités principales

## Interface graphique

* Dashboard moderne
* Navigation intuitive
* Date/heure en temps réel

### Simulation

* Paramètres dynamiques (λ, μ, c)
* Vérification de stabilité (ρ)
* Historique des simulations

### Visualisation

* Histogramme
* Fonction de répartition
* Évolution temporelle

### Statistiques

* Moyenne, médiane, quartiles
* Écart-type
* Probabilités d’attente


## Aperçu

![Interface](screenshot.png)


##  Améliorations possibles

* Base de données (SQLite)
* Export PDF / Excel
* Version web (Flask / Django)
* Authentification sécurisée


## Auteur

Projet académique – Simulation et modélisation des files d’attente.
KY Prisca , KONATE Samchoudine et TAMBOURA

## Remarque

Ce projet illustre l’application des **processus stochastiques** et de la **théorie des files d’attente** dans un contexte réel.
