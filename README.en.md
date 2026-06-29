[![Python 3](https://img.shields.io/badge/python-3.x-blue.svg?logo=pythonlang)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](/LICENSE)
[![SportOrgPlus version](https://img.shields.io/github/v/release/sembruk/sportorg-plus)](https://github.com/sembruk/sportorg-plus/releases/latest)

# SportOrgPlus

[Русский](/README.md)

Software for orienteering, rogaining and adventure racing.

This repository is a fork of [SportOrgPlus v1.7.0](https://github.com/sembruk/sportorg-plus/releases/tag/v1.7.0). SportOrgPlus itself is based on [SportOrg v1.5](https://github.com/sportorg/pysport).

The main difference from SportOrg is full rogaining support, including team events.

This branch adds macOS-focused improvements:

- migration to the current PySide6 library;
- better table contrast in the macOS dark theme;
- CH34x driver installation for USB-Serial adapters;
- serial port detection and scanning for `/dev/cu.*` and `/dev/tty.*`;
- automatic opening of macOS System Settings for driver approval when needed.

[Changelog](/changelog.en.md)

## Installation

### Windows

[Download](https://github.com/sembruk/sportorg-plus/releases/latest) and run installation file \*.msi.

### GNU/Linux

Clone repository:

```commandline
git clone https://github.com/sembruk/sportorg-plus.git
cd sportorg-plus
```

Install requirements:

```commandline
pip3 install -r requirements.txt
```

Run:

```commandline
./SportOrgPlus.pyw
```

### macOS

Clone repository:

```commandline
git clone https://github.com/sembruk/sportorg-plus.git
cd sportorg-plus
```

Create a virtual environment and install requirements:

```commandline
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.mac.txt
```

If you use a USB-Serial adapter based on CH340/CH341/CH34x, install and verify the driver:

```commandline
./setup_ch34x_macos.sh
```

The script downloads the official WCH driver, installs the package, checks Driver Extension status, opens System Settings for approval when needed, and prints detected serial ports.

Run the application:

```commandline
. .venv/bin/activate
./SportOrgPlus.pyw
```

If the app is launched outside the virtual environment, macOS may use dependencies from system Python or a conda/base environment. This can produce package compatibility warnings. The recommended launch method is from `.venv`.

### Screenshots

![Mainwindow sportorg](img/mainwindow.png)

![Dialogedit sportorg](img/dialogedit.png)
