# Écran d'affichage de l'electroLAB (electroLAB's display)

*Attention, il est assumé que le lecteur a des connaissances en électronique, et en Python, sait utiliser le terminal sur sa machine principale, ainsi que `SSH` et langue anglaise. Si ce n'est pas le cas, contactez nous ou venez nous rendre visite à l'electroLAB ([electroLAB@alumni.umons.ac.be](mailto:electroLAB@alumni.umons.ac.be)), nous aurons le plaisir de répondre à toutes vos questions.*

Ce projet est basé sur une Raspberry Pi 2 et un module T.V53.03 permettant d'utiliser un ancien écran d'ordinateur. L'objectif de ce projet est de construire un afficheur pour informer nos membres de nos horaires et informations. L'afficheur est mis à jour chaque minute en "scrapant" les informations de notre page Facebook à la recherche de nos _posts_ d'horaire.



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

- suivez les instructions de montage du module de contrôle de l'écran
- raccordez la Raspberry Pi à l'écran (HDMI ou coaxial et câble USB)
- si vous voulez faire votre propre adaptateur POE, repérez les bornes positive et négative du module de contrôle de l'écran et y souder des fils, i.e., noir (GND ou `-`) et rouge (VCC ou `+`)
  - construite les adaptateurs POE passif
- sinon, utilisez simplement votre adaptateur POE passif ou un câble dédié à l'alimentation.

### Configuration de la carte

- téléchargez un OS sur la carte, i.e., [Raspberry Pi OS with desktop](https://www.raspberrypi.org/software/operating-systems/)

- [installez](https://www.raspberrypi.org/documentation/installation/installing-images/) l'OS avec la méthode de votre choix

- [activez la connexion SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/)
  
  - créez un fichier sans extension `ssh`, dans la racine `boot` de la carte utilisée pour l'installation, est la méthode favorite
  - [améliorez la sécurité](https://www.raspberrypi.org/documentation/configuration/security.md)
  
- insérez la carte (micro)SD dans la Raspberry et démarrez le système

- si une seule Raspberry est connectée, vous pouvez tenter de vous y connecter directement en `ssh` avec la commande `ssh pi@raspberrypi` et le mot de passe `raspberry` dans un terminal. Si plusieurs cartes sont connectées, identifiez l'adresse IP de votre carte (soit si l'écran est allumé, en regardant l'utilitaire de configuration, sinon, en utilisant un scanner d'adresses IP comme Nmap ou Advanced IP Scanner) et remplacez  `raspberrypi` par l'adresse IP.

- configurez la [connexion `ssh` sans mot de passe](https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md)

- toujours par le biais de `ssh`, lancez `raspi-config`
  - changez le mot de passe pour sécurisé votre carte un minimum
  - changez le nom de domaine `hostname` de la carte Raspberry, qui est `raspberrypi` par default. Par la suite, ce nom de domaine pourra être utilisé pour se connecter à la carte sans devoir chercher l'adresse IP
  - changez la résolution de votre écran si nécessaire (ne pas modifier si vous utilisez le port composite, ou RCA)
  - configurez la _timezone_
  - après avoir redémarrez la Raspberry, si vous voulez retirer `piwiz`, suivez les [instructions de ce post](https://www.raspberrypi.org/forums/viewtopic.php?t=231557) ou suivez les étapes de l'utilitaire jusqu'au bout
  
- clonez le dépôt `elabdisp`

  - créez le dossier où sera cloné le projet`sudo mkdir -p /etc/elabdisp/`
  - se déplacez dans le dossier `cd /etc/elabdisp/`
  - clonez le projet ` sudo git clone https://github.com/2010019970909/elab_display.git`
  - astuce, ajoutez un alias pour réinitialiser votre dépôt et récupérer le dernier code de la branche `main`
    - Ajouter une alias dans `~\.bashrc` (`sudo nano ~\.bashrc`, éditez le fichier et appliquer les changements `source ~\.bashrc`)
    -  `alias gr="sudo git reset --hard HEAD && sudo git checkout main && sudo git pull"`
    - maintenant après s'être déplacé dans le répertoire du projet cloné (`cd /etc/elabdisp/elab_display/`), il suffit de saisir la commande `gr` pour oublier tous les changements locales et récupérer le dernier code

- installez les modules nécessaires

  - `python3 -m pip install demoji emoji facebook_scraper pillow`
  - `sudo apt install python3-pil python3-pil.imagetk -y`

- listez les écrans connectés et démarrer l'application sur l'écran

  - `ps aux | grep Xorg`

    - ```bash
      root       413 10.2  2.7 120576 12232 tty7     Ssl+ 13:41   5:58 /usr/lib/xorg/Xorg :0 -seat seat0 -auth /var/run/lightdm/root/:0 -nolisten tcp vt7 -novtswitch
      pi        3137  3.0  0.4   7348  1960 pts/0    S+   14:39   0:00 grep --color=auto Xorg
      ```

    - `/usr/lib/xorg/Xorg :0` nous indique que l'on peut utiliser l'écran `0`

  - `DISPLAY=:0.0 python3 /etc/elabdisp/elab_display/GUI_schedule_scraping.py &`

    - `DISPLAY=:0.0` indique quel écran utiliser pour lancer le programme
    - `&` permet de lancer la commande et de la libérer de la console (on peut donc entrer d'autres commande par la suite)
    - `/etc/elabdisp/elab_display/GUI_schedule_scraping.py` est le chemin complet vers exécutable

- modifiez le script à votre convenance

  - `sudo nano /etc/elabdisp/elab_display/GUI_schedule_scraping.py`

  - ici, avec le RCA (port composite), la résolution est très faible et le ratio n'est plus correct (et au lieu de trouver une configuration adaptée dans Raspberry Pi OS, quelques modification dans le code sont nécessaire, bien que l'idéal serait de simplement utiliser un câble HDMI)

    - ```python
      ENABLE_EMOJI = False
      PHONE_NBR = fs.add_emoji(":telephone_receiver:") \
              \+ " : NUMÉRO DE TÉLÉPHONE DE VINCENT" \
              if ENABLE_EMOJI            \
              else "Tél. : NUMÉRO DE TÉLÉPHONE DE VINCENT"
      ```

      on s'assure d'abord que `ENABLE_EMOJI` est désactivé, comme c'est le cas ici (il semble que Raspberry ne supporte pas les emoji nativement). Ensuite on peut indique un numéro de téléphone à la place de `NUMÉRO DE TÉLÉPHONE DE VINCENT` ou changer totalement le contenu de cette ligne

    - ``````python
      self.font = tkFont.Font(family="Helvetica", size=40)
      ``````

      ici, il faut changer `size=40` en `size=15`, pour éviter que le texte soit trop grand

    - ``````python
      self.img = ImageTk.PhotoImage(
                  Image.open(LOGO_PATH).resize(  # Logo
                      (int(self.screen_height/10),  # Target width
                       int(self.screen_height/10)),  # Target height
                      Image.ANTIALIAS))
      ``````

      au niveau de `# Target width`, pour tenter de corriger le ratio sur le logo, on peut changer `int(self.screen_height/10),` en `int(self.screen_height/10*3/4),`

- dernière étape, lancez le script au démarrage de la carte Raspberry en utilisant `crontab`

  - ajouter une commande dans `crontab`, en utilisant la commande `crontab -e` (si on vous demande de choisir un terminal, choisissez `nano`, ou celui qui vous convient)

  - commande à ajouter

    ``````bash
    @reboot DISPLAY=:0.0 python3 /etc/elabdisp/elab_display/GUI_schedule_scraping.py &
    ``````

    cette commande s'exécute au démarrage (`@reboot`) avec l'écran 0 ou autre valeur déterminée plus haut (`DISPLAY=:0.0`) et démarre le script de manière indépendante de `crontab`, `python3 /etc/elabdisp/elab_display/GUI_schedule_scraping.py &`

  - vérifiez que la commande à bien été ajoutée avec `crontab -l`

  - au prochain démarrage, vous pourrez utiliser la commande `journalctl -u cron.service` pour lister les évènements du service `cron` et voir si votre commande s'est bien exécutée (évidement, la GUI devrait se lancer en moins de 5 minutes)