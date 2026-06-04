# Sankey énergie

Cette applet interactive permet d’explorer, à partir d’un diagramme de Sankey simplifié, différents leviers permettant de réduire le recours à des sources d’énergie carbonées dans un système d’usages sociétaux.

L’outil a été conçu comme support d’enseignement pour travailler la distinction entre sources d’énergie, transferts d’énergie, énergie utile et énergie inutile.

## Principe général

Le diagramme représente un système convertisseur associé à des usages sociétaux : transports, habitat, industrie, services, etc.

Les bandes du diagramme ne représentent pas une énergie « contenue » dans les systèmes. Elles quantifient des transferts d’énergie associés au fonctionnement du système pendant une durée donnée. Les largeurs des bandes sont proportionnelles aux quantités d’énergie transférées, exprimées ici en unités arbitraires.

La contrainte imposée est la conservation :

```
flux entrants = flux sortants
```

## Question didactique

L’applet peut être utilisée à partir de la question suivante :

> Comment faire pour réduire le flux d’énergie carbonée mobilisé par ce système ?

Dans la version actuelle, le flux carboné n’est pas directement réglé par un curseur. Il est calculé comme ce qu’il reste à fournir une fois prises en compte les sources décarbonées mobilisées et le besoin total du système.

Les élèves peuvent agir sur plusieurs leviers :

* réduire la taille du convertisseur ;
* réduire l’énergie inutile ;
* augmenter le recours à l’uranium ;
* augmenter le recours aux autres sources décarbonées.

L’intérêt de la manipulation est de faire apparaître que la réduction du flux carboné peut résulter d’une combinaison de ces leviers, et pas seulement d’une substitution directe d’une source par une autre.

## Installation

L’application nécessite Python ainsi que les bibliothèques `streamlit` et `plotly`.

Avec Miniconda, on peut créer un environnement dédié :

```
conda create -n sankey-energie python=3.11
conda activate sankey-energie
pip install -r requirements.txt
```

## Lancement de l’application

Depuis le dossier du projet :

```
streamlit run app.py
```

L’application s’ouvre alors dans le navigateur.

Si la page ne s’ouvre pas automatiquement, copier l’adresse locale affichée dans le terminal, par exemple :

```
http://localhost:8501
```

## Structure du dépôt

```
sankey-energie/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Licence

Licence à préciser.
