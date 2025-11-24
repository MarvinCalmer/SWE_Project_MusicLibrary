# Use Case Beschreibungen 

Dieses Dokument beschreibt die wichtigsten Use Cases für die Musik Bibliothek.

---

## Use Case 1: Nach Tracks suchen

**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es sind bereits Titel vorhanden

**Haupterfolgsszenario:**

1. Benutzer greift auf die gespeicherten Titel in der Bibliothek zu und kann Titel sehen.
2. Benutzer gibt Suchkriterien ein (z.B. Songname, Künstler, Album, Genre).  
3. System zeigt die Suchergebnisse an.  
4. Benutzer betrachtet die Liste der Tracks.  

**Erweiterungen:**  

- 2a. Benutzer gibt Suchkriterien ein, die keine Ergebnisse liefern:  
  - System zeigt die Nachricht: „Keine Tracks gefunden“  
- 3b. Benutzer möchte Suchergebnisse nach Genre, Künstler oder Album filtern:  
  - System zeigt Filteroptionen an, Benutzer kann auswählen ob er nach dem Titel oder den anderen Kriterien suchen möchte.

---

## Use Case 2: Track hinzufügen

**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es sind bereits Titel vorhanden

**Haupterfolgsszenario:**  

1. Benutzer klickt den Button zum Hinzufügen eines Titels.
2. Benutzer gibt die Track-Daten ein (Titel, Künstler, Album, Genre, ggf. zusätzliche Metadaten).
3. System legt den neuen Track in der JSON und der Titelliste an und vergibt eine eindeutige ID.
  
---

## Use Case 3: Track aktualisieren (edit)

**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es sind bereits Titel vorhanden

**Haupterfolgsszenario:**  

1. Benutzer wählt einen bestehenden Track aus der Liste aus.  
2. Benutzer klickt den Button zum Bearbeiten des Tracks.  
3. Benutzer ändert gewünschte Datenfelder (z. B. Titel, Künstler, Album, Genre).
4. System speichert die aktualisierten Track-Daten in der JSON und der Titelliste.

---

## Use Case 4: Track löschen

**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es sind bereits Titel vorhanden

**Haupterfolgsszenario:**  

1. Benutzer wählt einen Track aus der Liste aus.
2. Benutzer wählt den Button zum Löschen aus.  
3. System fordert eine Bestätigung zur Löschung an.  
4. Benutzer bestätigt die Löschung.  
5. System entfernt den Track aus der JSON und der Titelliste.  

**Erweiterungen:**  

- 3a. Benutzer bricht die Löschung ab:  
  - System bricht den Vorgang ab, der Track bleibt unverändert.  
