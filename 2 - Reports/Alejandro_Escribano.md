# HepiaLight 3 - Raspberry Pi Pico - Personal Journal #

<u>**Table Of Contents**</u>
- [Introduction/Abstract](#introductionabstract)
- [Daily Work Log](#daily-work-log)
    - [17 June 2024](#17-june-2024)
    - [18 June 2024](#18-june-2024)
    - [19 June 2024](#19-june-2024)
    - [20 June 2024](#20-june-2024)
    - [21 June 2024](#21-june-2024)
    - [24 June 2024](#24-june-2024)
    - [25 June 2024](#25-june-2024)
    - [26 June 2024](#26-june-2024)
    - [27 June 2024](#27-june-2024)
    - [28 June 2024](#28-june-2024)
- [References](#references)
- [Creators](#creators)
- [Copyright and License](#copyright-and-license)

--------------------------------------------------------------------------------

## Introduction/Abstract ##



## Daily Work Log ##

### 17 June 2024 ###

- 

- 

### 18 June 2024 ###

- 

- 

### 19 June 2024 ###

- 

- Working together with **M. Divià**, we set out to try to map part of the ``GPIO`` interfaces of the RBPi Pico in order to "create" two additional ``UART`` interfaces, giving us a total of four so that we would have a total of four to communicate with all adjacent neighbours.  
We made a first attempt using MicroPython and the libraries made available by it, but the results were more than inadequate. The ``UART`` timings didn't seem to be correct even though they were configured correctly and the messages arrived successfully very rarely. Using the **AnalogDiscovery 2** we determined that the current system did not appear to be fast enough to meet the ``UART`` timings standard.  
After this failed attempt and after having talked to some of the assistants, we decided to make a second attempt, but this time using the ``PIO`` library available for the RBPi Pico. This implements, among other things, **lower level assembly functions** to interact with the I/O of the system. After studying some of the examples found on the internet and adjusting some of the parameters, we were able to get the two extra ``UART`` interfaces to work. The advantage and speed of using this method proved to be **clearly superior** to anything we had used before.

- Discussed with **M. Perez** and **M. Le Gouic** the possibility of adding **wireless communications** to the project either using an ESP32 or replacing the current RBPi Pico by a RBPi Pico W. It still is only a possibility under discussion, because we don't know yet the viability and complexity of it.

### 20 June 2024 ###

- Had to present another project during the morning. As a consequence I didn't touch this one during the morning.

- I had to work the whole day on another project in order to be able to present it at the end of the week.

- There was no progress from my side on **HEPIALight3**.

### 21 June 2024 ###



### 24 June 2024 ###



### 25 June 2024 ###



### 26 June 2024 ###



### 27 June 2024 ###



### 28 June 2024 ###



## References ##



## Creators

[**Alejandro Escribano Martín**](https://gitedu.hesge.ch/Alejandro.Escribano)

In collaboration with : [Michel Divià](https://gitedu.hesge.ch/michael.divia) and [Gaspard Le Gouic](https://gitedu.hesge.ch/gaspard.legouic)

## Copyright and License

Code and documentation © 2024 the authors. Code released under the [MIT License](../LICENSE).
