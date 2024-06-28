# HepiaLight 3 - Raspberry Pi Pico

# Table des matières

<!-- TOC -->

- [HepiaLight 3 - Raspberry Pi Pico](#hepialight-3---raspberry-pi-pico)
- [Table des matières](#table-des-mati%C3%A8res)
- [Instruction & Description](#instruction--description)
- [Mise en place de la communication](#mise-en-place-de-la-communication)
    - [Upload du code](#upload-du-code)
- [Journal de bord](#journal-de-bord)
    - [Lundi, 17 Juin 2024](#lundi-17-juin-2024)
    - [Mardi, 18 Juin 2024](#mardi-18-juin-2024)
    - [Mercredi, 19 Juin 2024](#mercredi-19-juin-2024)
    - [Jeudi, 20 Juin 2024](#jeudi-20-juin-2024)
    - [Lundi, 24 Juin 2024](#lundi-24-juin-2024)
    - [Mardi, 25 Juin 2024](#mardi-25-juin-2024)
    - [Mercredi, 26 Juin 2024](#mercredi-26-juin-2024)
    - [Jeudi, 27 Juin 2024](#jeudi-27-juin-2024)
    - [Vendredi, 28 Juin 2024](#vendredi-28-juin-2024)
- [Travail réalisé](#travail-r%C3%A9alis%C3%A9)
- [Creators](#creators)
- [Copyright and license](#copyright-and-license)

<!-- /TOC -->

# Instruction & Description

Ce projet consiste à concevoir une adaptation du projet HepiaLight 2 sur une nouvelle architecture afin de prouver son fonctionnement pour HepiaLight 3. Nous utiliserons un Raspberry Pi Pico ainsi qu'une matrice numérique avec des leds RGB adressables ainsi qu'une MyLab2 pour les capteurs externes (accéléromètre, touchscreen).

# Mise en place de la communication

## Upload du code

Après avoir uploader le bon Firmware sur le Raspberry Pi, comme indiqué [ici](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), nous pouvons utiliser le logiciel [Thonny](https://thonny.org/) afin d'uploader notre code.

# Journal de bord

## Lundi, 17 Juin 2024

- Lecture de documentation

## Mardi, 18 Juin 2024

- Mise en place de l'environnement de travail Thonny.
- Upload du firmware sur la Raspberry Pi.
- Aide à Michael pour l’implémentation du texte en mouvement
- Tentative d’implémentation d'une lecture d'un capteur de température par I2C comme "proof of concept" pour l'ajout d'un accéléromètre -> Réussi à détecter le capteur mais pas à le lire.

## Mercredi, 19 Juin 2024

- Résolution des problèmes d'I2C.
- Récupération et traitement des données d'un capteur de température.
- Récupération et traitement des données de l'accéléromètre de la MyLab2.
- Documentation sur le fonctionnement du SPI.
- Exploration de possibilités pour des implémentations futurs.

## Jeudi, 20 Juin 2024

- Recherches documentaires sur SPI.

## Lundi, 24 Juin 2024

- Recherches documentaire sur les interruptions GPIOs.

## Mardi, 25 Juin 2024

- Aide à Michael pour la structure du rapport pour les parties I2C et SPI.

## Mercredi, 26 Juin 2024

- Recherches sur la structure de code à adopter.

## Jeudi, 27 Juin 2024

- Mise en accord avec les autres groupes sur l'API (peu impactant étant le seul à traiter les questions d'I2C et de SPI).
- Mise en place finale de l’accéléromètre
- Mise en place finale du touchscreen

## Vendredi, 28 Juin 2024

- Mise en place finale de l'écran LCD
- Écriture rapport et présentation
- Préparation de la démonstration

# Travail réalisé

A titre personnel, je me suis donc occupé des capteurs externes touchscreen et accéléromètre (I2C) et de l'affichage LCD (SPI) le tout avec une carte MyLab2. Pour plus de détails, voir les sections associées dans le Main Report.


# Creators

**Gaspard Le Gouic**

- <https://gitedu.hesge.ch/gaspard.legouic>

# Copyright and license

Code and documentation copyright 2024 the authors. Code released under the [MIT License](https://gitedu.hesge.ch/michael.divia/hepialight3-pico/-/blob/94f8f25ac736165111a03ff964f1538a65eb40e3/LICENSE).