# Musik Bibliothek 

Im Rahmen der Vorlesung Software Technik soll eine Musik Bibliothek erstellt werden. Diese soll durch agile Methoden wie User Stories und einen Backlog getrackt werden. Es sollen Test verfasst werden und UML-Diagramme erstellt werden.

---

## Inhaltsverzeichnis

- [Musik Bibliothek](#musik-bibliothek)
  - [Inhaltsverzeichnis](#inhaltsverzeichnis)
  - [Über das Projekt](#über-das-projekt)
  - [Autoren und Betreuung](#autoren-und-betreuung)
  - [Technologien und Tools](#technologien-und-tools)
  - [Installation und Ausführung](#installation-und-ausführung)
  - [Projektstruktur](#projektstruktur)

---

## Über das Projekt

Dieses Projekt wurde im Rahmen des Moduls Software Technik im Wintersemester 2025/26 an der Hochschule Esslingen entwickelt. Ziel ist die Entwicklung einer Musik Bibliothek. Diese soll durch agile Methoden wie User Stories und einen Backlog getrackt werden. Es sollen Test verfasst werden und UML-Diagramme erstellt werden.

---

## Autoren und Betreuung

Marvin Calmer, Gregor Ruehle, Dustin-Thai Tran, Paul Ellinger

Betreuung: Prof. Dr. Martin Roehricht

---

## Technologien und Tools

Liste der wichtigsten verwendeten Technologien, Frameworks und Tools:

- Programmiersprache: Python
- Frameworks: Pytest
- Datenspeicherung: JSON
- Tools: Git, Visual Studio Code, UML Diagrammeditor

---

## Installation und Ausführung

```bash
# Repository klonen
git clone https://github.com/MarvinCalmer/SWE_Project_MusicLibrary

# pytest installieren
make install

# Projekt starten
make run

# Tests ausführen
make test

# Aufräumen
make clean
```

---

## Projektstruktur

```bash

projektname/
│
├── src/              # Quellcode
│   ├── main.py       # Einstiegspunkt
│   ├── utils.py      # Hilfsfunktionen
│   └── ...
│
├── data/             # Datensätze oder Input-Dateien
├── tests/            # Unit Tests
├── docs/             # Dokumentation
└── README.md         # Diese Datei

```
