[![Python 3](https://img.shields.io/badge/python-3.x-blue.svg?logo=pythonlang)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)](/LICENSE)
[![SportOrgPlus version](https://img.shields.io/github/v/release/sembruk/sportorg-plus)](https://github.com/sembruk/sportorg-plus/releases/latest)

# SportOrgPlus

[English](/README.en.md)

Программа для проведения соревнований по спортивному ориентированию, рогейну и приключенческим гонкам.

Этот репозиторий является ответвлением от [SportOrgPlus v1.7.0](https://github.com/sembruk/sportorg-plus/releases/tag/v1.7.0). SportOrgPlus, в свою очередь, основан на [SportOrg версии 1.5](https://github.com/sportorg/pysport).

Основное отличие SportOrgPlus от SportOrg — полная поддержка соревнований по рогейну, включая командный формат.

В этой ветке добавлены доработки для macOS:

- переход на актуальную библиотеку PySide6;
- улучшенный контраст таблиц в темной теме macOS;
- установка CH34x-драйвера для USB-Serial адаптеров;
- проверка и сканирование последовательных портов `/dev/cu.*` и `/dev/tty.*`;
- автоматическое открытие системных настроек macOS для подтверждения драйвера, если это требуется.

[Список изменений](/changelog.ru.md)

[Руководство пользователя](/docs/index.md)

## Установка

### Windows

[Скачать](https://github.com/sembruk/sportorg-plus/releases/latest) и запустить файл установки \*.msi.

### GNU/Linux

Скачать проект:

```commandline
git clone https://github.com/sembruk/sportorg-plus.git
cd sportorg-plus
```

Установить зависимости:

```commandline
pip3 install -r requirements.txt
```

Запустить:

```commandline
./SportOrgPlus.pyw
```

### macOS

Скачать проект:

```commandline
git clone https://github.com/sembruk/sportorg-plus.git
cd sportorg-plus
```

Создать виртуальное окружение и установить зависимости:

```commandline
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.mac.txt
```

Если используется USB-Serial адаптер на чипе CH340/CH341/CH34x, установить и проверить драйвер:

```commandline
./setup_ch34x_macos.sh
```

Скрипт скачает официальный драйвер WCH, установит пакет, проверит статус Driver Extension, откроет окно подтверждения в System Settings при необходимости и покажет найденные последовательные порты.

Запустить приложение:

```commandline
. .venv/bin/activate
./SportOrgPlus.pyw
```

Если приложение запускается не из виртуального окружения, macOS может использовать зависимости из системного Python или conda/base-окружения. В этом случае возможны предупреждения о несовместимых версиях пакетов. Рекомендуемый запуск — из `.venv`.

### Скриншоты

![Mainwindow sportorg](img/mainwindow.png)

![Dialogedit sportorg](img/dialogedit.png)
