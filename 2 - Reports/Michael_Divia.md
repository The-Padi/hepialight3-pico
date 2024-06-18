# HepiaLight 3 - Raspberry Pi Pico

# Table des matières
- [HepiaLight 3 - Raspberry Pi Pico](#hepialight-3---raspberry-pi-pico)
- [Table des matières](#table-des-matières)
- [Instruction \& Description](#instruction--description)
- [Mise en place de la communication](#mise-en-place-de-la-communication)
  - [Branchements de la carte](#branchements-de-la-carte)
  - [Upload du code](#upload-du-code)
- [Travail](#travail)
  - [Lundi, 17 Juin 2024](#lundi-17-juin-2024)
  - [Mardi, 18 Juin 2024](#mardi-18-juin-2024)
- [Creators](#creators)
- [Copyright and license](#copyright-and-license)


# Instruction & Description

Ce projet consiste à concevoir une adaptation du projet HepiaLight 2 sur une nouvelle architecture afin de prouver son fonctionnement pour HepiaLight 3. Nous utiliserons un Raspberry Pi Pico ainsi qu'une matrice numérique avec des leds RGB adressables.

# Mise en place de la communication

## Branchements de la carte

| **RPI Pico** | **NeoPixel NeoMatrix 8x8** |
| :----------: | :------------------------: |
|     3V3      |             5V             |
|     GND      |            GND             |
|    GPIO 0    |            DIN             |

## Upload du code

Après avoir uploader le bon Firmware sur le Raspberry Pi, comme indiqué [ici](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), nous pouvons utiliser le logiciel [Thonny](https://thonny.org/) afin d'uploader notre code.

# Travail

## Lundi, 17 Juin 2024

Après avoir flasher le bon Firmware sur de Raspberry Pi, j'ai pu vérifier le bon fonctionnement en uploadant un code simple en suivant [cette documentation](https://docs.micropython.org/en/latest/rp2/quickref.html#neopixel-and-apa106-driver). J'ai pu donc constater que mon code fonctionnais ainsi que les connexions était correcte.

J'ai ensuite pris du temps afin de souder des pin à la matrice de LED afin de facilité ça connexion à la Breadboard. J'ai ensuite commencé à concevoir la fonction `matrix`.

## Mardi, 18 Juin 2024

J'ai commencé par créer `hl3.py` afin d'avoir un fichier librairie avec toutes les fonctions que nous allons implémentées. Je me suis ensuite attelé à la finalisation de la fonction `matrix`. J'ai aussi profité d'implémenter toute les couleurs que nous devions implémentées d'après la documentation. J'ai ensuite enchaîné avec l'ajout de la fonction `set_line`,`set_column`, `set_led`. 

# Creators

**Michael Divià**

- <https://gitedu.hesge.ch/michael.divia>

# Copyright and license

Code and documentation copyright 2024 the authors. Code released under the [MIT License](https://gitedu.hesge.ch/michael.divia/hepialight3-pico/-/blob/94f8f25ac736165111a03ff964f1538a65eb40e3/LICENSE).

Enjoy :metal: