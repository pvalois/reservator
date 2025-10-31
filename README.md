## Projet

Dans le cadre d'un possible recrutement, le projet initial se composait d'un système  de reservation de 
serveur physiques sur demande de ressources
 
* Par un utilisateur
* Pour un certain nombre de cpu 
* Pour une quantité de ram 

## Réalisations 

* Création d'une lib de reservation permettant de gérer la récupération d'infos de la base et la recherch de vm sur critères
* Création d'une api de test flask, qui utilise la lib et gère des appels rest pour permettre de faire le pont entre un front et les fonctions de la lib
* Scripts d'initialisations et de destruction de la base 
* Création d'un frontend de test, permettant de rechercher les vm allouées a un utilisateur et à procéder à une demande 
* Script shell de validation des endpoints de l'api 
* Scripts cli de consultation, reservation, resiliation de reservation 

## Résultat

Je n'ai pas eu le poste, ayant été jugé de communication hésitante (la ou je refléchissais simplement pour donner une bonne réponse).

Je publie donc ce que j'ai écrit comme preuve de réalisation technique, avec reservation atomique (par requete atomique mariadb). et base fonctionnelle 
applicative. 

Il n'aurait surement resté qu'a gérer des options additionnelles (taille disque minimale, allocations maximales par utilisateur, ...) et faire un front plus 
"professionnel". 

Dommage pour moi ... mais aussi pour eux ! 

