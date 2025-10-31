## Projet

Dans le cadre d’un processus de recrutement, le projet initial consistait à concevoir un système de réservation de serveurs physiques sur demande de ressources :

* Par un utilisateur
* Pour un certain nombre de CPU
* Et une quantité de RAM

## Réalisations

* Développement d’une librairie de réservation gérant la récupération des informations en base et la recherche de VM selon des critères définis
* Mise en place d’une API Flask exploitant cette librairie, exposant des endpoints REST pour relier le front et la logique applicative
* Scripts d’initialisation et de destruction de la base de données
* Création d’un frontend de test, permettant la recherche de VM et la soumission de demandes de réservation
* Scripts shell de validation des endpoints de l’API
* CLI pour la consultation, la réservation et la résiliation de ressources

Et tout cela, réalisé avant même d’avoir le poste… histoire de prouver que la réflexion et la motivation étaient bien là.

## Résultat

Le poste n’a finalement pas été attribué, le retour évoquant une communication jugée “hésitante” — là où je prenais simplement le temps de réfléchir avant de répondre.

Je publie donc ici cette réalisation comme preuve de conception et d’exécution technique, illustrant :

* Une gestion atomique des réservations (requêtes atomiques MariaDB)
* Une base applicative complète et fonctionnelle
* Des pistes d’amélioration identifiées (options avancées, quotas utilisateurs, interface front plus aboutie, etc.)

Un projet non retenu, certes — mais pleinement abouti. Dommage pour moi… et peut-être un peu pour eux aussi. 

