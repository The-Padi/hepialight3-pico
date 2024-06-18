# HepiaLight 3 - Raspberry Pi Pico

# Table des matières

<!-- TOC -->

- [HepiaLight 3 - Raspberry Pi Pico](#hepialight-3---raspberry-pi-pico)
- [Table des matières](#table-des-mati%C3%A8res)
- [Instruction & Description](#instruction--description)
- [Mise en place de la communication](#mise-en-place-de-la-communication)
    - [Branchements de la carte](#branchements-de-la-carte)
    - [Upload du code](#upload-du-code)
- [Travail](#travail)
    - [Lundi, 17 Juin 2024](#lundi-17-juin-2024)
    - [Mardi, 18 Juin 2024](#mardi-18-juin-2024)
- [Creators](#creators)
- [Copyright and license](#copyright-and-license)

<!-- /TOC -->

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

- Lecture de documentation

## Mardi, 18 Juin 2024

- Mise en place de l'environnement de travail Thonny.
- Upload du firmware sur la Raspberry Pi.
- Aide à Michael pour l’implémentation du texte en mouvement
- Tentative d’implémentation d'une lecture d'un capteur de température par I2C comme "proof of concept" pour l'ajout d'un accéléromètre -> Réussi à détecter le capteur mais pas à le lire.

# Creators

**Gaspard Le Gouic**

- <https://gitedu.hesge.ch/gaspard.legouic>

# Copyright and license

Code and documentation copyright 2024 the authors. Code released under the [MIT License](https://gitedu.hesge.ch/michael.divia/hepialight3-pico/-/blob/94f8f25ac736165111a03ff964f1538a65eb40e3/LICENSE).