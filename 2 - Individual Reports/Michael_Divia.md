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
  - [Mercredi, 19 Juin 2024](#mercredi-19-juin-2024)
  - [Jeudi 20 Juin 2024](#jeudi-20-juin-2024)
  - [Vendredi 21 Juin 2024](#vendredi-21-juin-2024)
  - [Mardi 25 Juin 2024](#mardi-25-juin-2024)
  - [Jeudi 27 Juin 2024](#jeudi-27-juin-2024)
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

Après avoir uploader le bon Firmware sur le Raspberry Pi, comme indiqué [ici](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), nous pouvons utiliser le logiciel [Thonny](https://thonny.org/) afin d'uploader notre code (en installant le module Pypi).

# Travail

## Lundi, 17 Juin 2024

Après avoir flasher le bon Firmware sur de Raspberry Pi, j'ai pu vérifier le bon fonctionnement en uploadant un code simple en suivant [cette documentation](https://docs.micropython.org/en/latest/rp2/quickref.html#neopixel-and-apa106-driver). J'ai pu donc constater que mon code fonctionnais ainsi que les connexions était correcte.

J'ai ensuite pris du temps afin de souder des pin à la matrice de LED afin de facilité ça connexion à la Breadboard. J'ai ensuite commencé à concevoir la fonction `matrix`.

## Mardi, 18 Juin 2024

J'ai commencé par créer `hl3.py` afin d'avoir un fichier librairie avec toutes les fonctions que nous allons implémentées. Je me suis ensuite attelé à la finalisation de la fonction `matrix`.

J'ai aussi profité d'implémenter toute les couleurs que nous devions implémentées d'après la documentation. J'ai ensuite enchaîné avec l'ajout de la fonction `set_line`,`set_column`, `set_led`, `get_led` puis, avec l'aide de Gaspard, nous avons implémenter le début de la fonction `afficher_texte`.

J'ai ensuite créer un fonction de démo `christmas` afin de démontré le bon fonctionnement des LEDs. Cette fonction est une ré-implémentation de la fonction de M. Gluck que vous pouvez trouver [ici](https://gitedu.hesge.ch/cores/projects/hepialight2/hepialight2-examples/-/blob/02261b68aad94dd52c6b35fdb83ed1d54028061b/peripherals/display/christmas_ball.py).

Suite à cela nous avons, avec l'aide de M. Escribano, à implémenter les fonction `UART` suivante : `send`, `snedline`, `receive` et `receiveline` et nous avons commencé à les tester entre 2 cartes mais nous avons eux quelque problème, nous allons donc devoir continuer à investiguer cela demain.

## Mercredi, 19 Juin 2024

Avec l'aide de M. Escribano nous avons finalisé la correction des fonctions `receive` et `receiveline` afin de pouvoir communiqué en `UART` entre 2 cartes en utilisant les ports prévu à cet effet sur les RPI Pico (`NORTH` et `SOUTH` dans notre code).

Nous avons ensuite enchaîné avec la communication `UART` via les `GPIO`, pour cela nous avons utilisé `rp2 PIO`. Nous avons donc adapté tout les fonctions crées précédemment afin de fonctionner avec ces derniers.

## Jeudi 20 Juin 2024

Design et impression d'une boîte.

## Vendredi 21 Juin 2024

J'ai modifié la fonction d'affichage et de scrolling du texte afin d'utiliser un `FrameBuffer`. Cela accélère considérablement la vitesse de scolling.

## Mardi 25 Juin 2024

J'ai fini d'optimiser la fonction d'affichage et de scrolling du text. Le texte commence maintenant en dehors de l'écran et nous n'avons plus de problème de ralentissement a chaque fois que nous voulons afficher du texte. Ce problème était dû à un problème d'allocation mémoire et de garbage collection du `FrameBuffer`.

J'ai ensuite enchaîné avec la création d'une fonction `set_img` fonctionnant comme la fonction `afficher_grille` de `hepialight2`.

J'ai terminé ma journée en rédigeant la majorité du rapport.

## Jeudi 27 Juin 2024

Pour commencé, j'ai ajouter des commentaires DocString sur toute les fonctions de notre librairie `HepiaLight3`.

J'ai ensuite enchaîné avec la création de la présentation avec M. Escribano.

# Creators

**Michael Divià**

- <https://gitedu.hesge.ch/michael.divia>

# Copyright and license

Code and documentation copyright 2024 the authors. Code released under the [MIT License](https://gitedu.hesge.ch/michael.divia/hepialight3-pico/-/blob/94f8f25ac736165111a03ff964f1538a65eb40e3/LICENSE).

Enjoy :metal:
