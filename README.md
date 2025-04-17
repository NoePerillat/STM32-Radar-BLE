# STM32-Radar-BLE

Ce projet permet de lire la distance mesurée par un capteur à ultrasons connecté à un STM32 via une liaison Bluetooth Low Energy (BLE).  
L'application Android a été développée avec MIT App Inventor, et le STM32 a été programmé en MicroPython.


Fonctionnement de l’application

- Se connecte à un périphérique BLE (STM32)
- Lit toutes les 2 secondes la dernière distance mesurée
- Affiche la valeur reçue dans l'application


Contenu du projet

- `STM32_APP.aia` : projet App Inventor (à importer sur [ai2.appinventor.mit.edu](https://ai2.appinventor.mit.edu))
- `STM32.apk` : Application android à installer sur le téléphone android
- `main.py` (ou script MicroPython sur STM32) : code pour mesurer la distance et mettre à jour la characteristic BLE


Pré-requis

Côté STM32 :
- Une carte STM32 compatible BLE et MicroPython (ex : Nucleo WB55)
- Un capteur à ultrasons (branché sur D7)
- MicroPython installé
- Code STM32 flashé (voir plus bas)

Côté Android :
- Un smartphone compatible BLE
- L'application Android .apk
- Autorisations activées : Localisation (services Bluetooth) et Nearby Devices (BLE)



Utilisation

1. Flasher le STM32
   
   Charger ce code sur le STM32 : main.py

3. Via une console série envoyer les commandes suivantes :
   
   -ctrl + C
   
   -ctrl + D

5. Installer l'application android :
   
   Configurer les autorisations de position et nearby devices

7. Lancer l'application :
   
   -Effectuer une recherche devices BLE
   -Choisir la device "Nucleo_WB55_Noe"
   -Attendre quelques secondes la première valeur

