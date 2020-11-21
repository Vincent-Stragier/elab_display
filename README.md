# Écran d'affichage de l'electroLAB (electroLAB's display)

*Attention, il est assumé que le lecteur a des connaissances en électronique, et en langue anglaise. Si ce n'est pas le cas, contactez nous ou venez nous rendre visite.*

Ce projet est basé sur une Raspberry Pi 2 et un module T.V53.03 permettant d'utiliser un ancien écran d'ordinateur. L'objectif de ce projet est de construire un afficheur pour informer nos membres de nos horaires et informations. L'afficheur est mis à jour chaque minute en "scrapant" les informations de notre page Facebook à la recherche de nos posts d'horaire.



## Liste du matériel

- Raspberry Pi (2 ou plus)
- Un câble USB micro USB
- Un câble HDMI ou dans notre cas, un câble coaxial
- Un kit de conversion pour un écran LCD d'ordinateur portable
- Un écran d'ordinateur portable
- Du câble réseau, des connecteurs mâles et femelles 8P8C ("RJ45"), et du fil permettant de supporter 2 A sous 12 V
  - L'idée étant de construite un adaptateur POE passif (cependant, on peut trouver ces dernier à moins de 5 € sur des sites de vente en ligne)
- Un porte fusible
- Un fusible slow/lent, 2 ampères (à adapter en fonction de la consommation de votre système)
- Un support pour le système et des fixations
- Une alimentation pour l'écran et la Raspberry
  - Ici, nous utilisons une alimentation 12 V qui alimente le module de l'écran, qui va lui-même fournir 5,5 V à la carte Raspberry.

## Étapes du montage

### Assemblage du kit sur un support

- Assembler l'électronique :
  - suivre les instructions de montage du module de contrôle de l'écran
  - raccorder la Raspberry Pi à l'écran (HDMI ou coaxial et câble USB)
  - si vous voulez faire votre propre adaptateur POE, repérer les bornes positive et négative du module de contrôle de l'écran et y souder des fils, i.e., noir (GND ou '-') et rouge (VCC ou '+')
    - construite les adaptateurs POE passif
  - sinon, utiliser simplement votre adaptateur POE passif ou un câble dédié à l'alimentation.
- Configuration de la carte :
  - télécharger un OS sur la carte, i.e., [Raspberry Pi OS with desktop](https://www.raspberrypi.org/software/operating-systems/)
  - [installer](https://www.raspberrypi.org/documentation/installation/installing-images/) l'OS avec la méthode de votre choix
  - [activer la connexion SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/)
    - créer un fichier sans extension `ssh`, dans la racine `boot` de la carte utilisée pour l'installation, est la méthode favorite
    - [améliorer la sécurité](https://www.raspberrypi.org/documentation/configuration/security.md)
  - insérer la carte (micro)SD dans la Raspberry et démarrer le système
  - si une seule Raspberry est connectée, vous pouvez tenter de vous y connecter directement en `ssh` avec la commande `ssh pi@raspberrypi` et le mot de passe `raspberry`. Si plusieurs cartes sont connectées, identifiez l'adresse IP de votre carte (soit si l'écran est allumé, en regardant l'utilitaire de configuration, sinon, en utilisant un scanner d'adresses IP comme Nmap ou Advanced IP Scanner) et remplacez  `raspberrypi` par l'adresse IP.
  - configurer la [connexion `ssh` sans mot de passe](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)
  - toujours par le biais de `ssh`, lancer `raspi-config`
    - changer le mot de passe pour sécurisé votre carte un minimum
    - changer le nom de domaine `hostname` de la carte Raspberry, qui est `raspberrypi` par default. Par la suite, ce mot de passe pourra être utilisé pour se connecter à la carte sans devoir chercher l'adresse IP

