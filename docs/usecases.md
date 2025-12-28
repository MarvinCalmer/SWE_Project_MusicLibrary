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
  - System zeigt die Nachricht: „Keine Tracks gefunden"  
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
3. Benutzer ändert gewünschte Datenfelder (z. B. Titel, Künstler, Album, Genre).
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

---

## Use Case 5: Playlist erstellen
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet

**Haupterfolgsszenario:**  
1. Benutzer klickt den Button zum Erstellen einer neuen Playlist.
2. System fordert den Benutzer auf, einen Playlist-Namen einzugeben.
3. Benutzer gibt den Playlist-Namen ein.
4. System fordert den Benutzer auf, eine optionale Beschreibung einzugeben.
5. Benutzer gibt die Beschreibung ein (oder lässt sie leer).
6. System erstellt die Playlist, vergibt eine eindeutige ID und speichert sie in der playlists.json.
7. System zeigt die neue Playlist in der Playlist-Liste an.

**Erweiterungen:**  
- 3a. Benutzer gibt keinen Namen ein oder bricht ab:  
  - System bricht den Vorgang ab, keine Playlist wird erstellt.

---

## Use Case 6: Playlist bearbeiten
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es existieren bereits Playlists

**Haupterfolgsszenario:**  
1. Benutzer wählt eine bestehende Playlist aus der Liste aus.
2. Benutzer klickt den Button zum Bearbeiten der Playlist.
3. System zeigt die aktuellen Playlist-Daten (Name, Beschreibung) an.
4. Benutzer ändert gewünschte Datenfelder (Name und/oder Beschreibung).
5. System speichert die aktualisierten Playlist-Daten in der playlists.json.
6. System aktualisiert die Anzeige der Playlist-Liste.

**Erweiterungen:**  
- 1a. Keine Playlist ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie eine Playlist aus"

---

## Use Case 7: Playlist löschen
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es existieren bereits Playlists

**Haupterfolgsszenario:**  
1. Benutzer wählt eine Playlist aus der Liste aus.
2. Benutzer klickt den Button zum Löschen der Playlist.
3. System fordert eine Bestätigung zur Löschung an.
4. Benutzer bestätigt die Löschung.
5. System entfernt die Playlist aus der playlists.json.
6. System aktualisiert die Anzeige der Playlist-Liste.

**Erweiterungen:**  
- 1a. Keine Playlist ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie eine Playlist aus"
- 4a. Benutzer bricht die Löschung ab:  
  - System bricht den Vorgang ab, die Playlist bleibt unverändert.

---

## Use Case 8: Track zu Playlist hinzufügen
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet, es existieren Playlists und Tracks

**Haupterfolgsszenario:**  
1. Benutzer wählt eine Playlist aus der Playlist-Liste aus.
2. Benutzer wählt einen Track aus der Track-Liste aus.
3. Benutzer klickt den Button zum Hinzufügen des Tracks zur Playlist.
4. System fügt die Track-ID zur Playlist hinzu.
5. System speichert die aktualisierte Playlist in der playlists.json.
6. System zeigt eine Bestätigung an.

**Erweiterungen:**  
- 1a. Keine Playlist ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie eine Playlist aus"
- 2a. Kein Track ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie einen Track aus"
- 4a. Track ist bereits in der Playlist enthalten:  
  - System zeigt eine Fehlermeldung: „Track ist bereits in dieser Playlist"

---

## Use Case 9: Track aus Playlist entfernen
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet, eine Playlist ist ausgewählt und enthält Tracks

**Haupterfolgsszenario:**  
1. Benutzer wählt eine Playlist aus der Playlist-Liste aus.
2. System zeigt die Tracks in der ausgewählten Playlist an.
3. Benutzer wählt einen Track aus der Playlist aus.
4. Benutzer klickt den Button zum Entfernen des Tracks aus der Playlist.
5. System entfernt die Track-ID aus der Playlist.
6. System speichert die aktualisierte Playlist in der playlists.json.
7. System aktualisiert die Anzeige der Playlist-Tracks.

**Erweiterungen:**  
- 3a. Kein Track ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie einen Track aus"
- 5a. Track ist nicht in der Playlist enthalten:  
  - System zeigt eine Fehlermeldung: „Track ist nicht in dieser Playlist"

---

## Use Case 10: Playlist exportieren
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es existieren bereits Playlists

**Haupterfolgsszenario:**  
1. Benutzer wählt eine Playlist aus der Liste aus.
2. Benutzer klickt den Button zum Exportieren der Playlist.
3. System öffnet einen Datei-Speichern-Dialog.
4. Benutzer wählt den Speicherort und Dateinamen für die Export-Datei aus.
5. System exportiert die Playlist-Daten (ID, Name, Beschreibung, Track-IDs) in eine separate JSON-Datei.
6. System zeigt eine Erfolgsmeldung an.

**Erweiterungen:**  
- 1a. Keine Playlist ist ausgewählt:  
  - System zeigt eine Warnung: „Bitte wählen Sie eine Playlist aus"
- 4a. Benutzer bricht den Speichern-Dialog ab:  
  - System bricht den Export ab
- 5a. Speicherort ist nicht verfügbar oder Datei kann nicht geschrieben werden:  
  - System zeigt eine Fehlermeldung an

---

## Use Case 11: Playlist importieren
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und verfügt über eine exportierte Playlist-Datei

**Haupterfolgsszenario:**  
1. Benutzer klickt den Button zum Importieren einer Playlist.
2. System öffnet einen Datei-Öffnen-Dialog.
3. Benutzer wählt eine Playlist-JSON-Datei aus.
4. System liest die Datei und validiert die Daten.
5. System erstellt eine neue Playlist mit den importierten Daten und vergibt eine neue eindeutige ID.
6. System speichert die neue Playlist in der playlists.json.
7. System zeigt die importierte Playlist in der Playlist-Liste an.
8. System zeigt eine Erfolgsmeldung an.

**Erweiterungen:**  
- 3a. Benutzer bricht den Öffnen-Dialog ab:  
  - System bricht den Import ab
- 4a. Datei kann nicht gelesen werden:  
  - System zeigt eine Fehlermeldung: „Datei nicht gefunden oder nicht lesbar"
- 4b. Datei enthält ungültiges JSON:  
  - System zeigt eine Fehlermeldung: „Ungültiges JSON-Format"
- 4c. Datei enthält keine gültigen Playlist-Daten:  
  - System zeigt eine Fehlermeldung: „Ungültiges Playlist-Format"

---

## Use Case 12: Playlist-Tracks anzeigen
**Primärer Akteur:** Benutzer  
**Vorbedingung:** Benutzer hat die Musik Bibliothek geöffnet und es existieren Playlists mit Tracks

**Haupterfolgsszenario:**  
1. Benutzer wählt eine Playlist aus der Playlist-Liste aus.
2. System lädt die Track-IDs der ausgewählten Playlist.
3. System lädt die vollständigen Track-Daten für jede Track-ID aus der Library.
4. System zeigt die Tracks der Playlist mit vollständigen Informationen (Name, Künstler, Album, etc.) an.

**Erweiterungen:**  
- 1a. Keine Playlist ist ausgewählt:  
  - System zeigt eine leere Track-Liste an
- 3a. Eine oder mehrere Track-IDs existieren nicht mehr in der Library:  
  - System überspringt die fehlenden Tracks und zeigt nur die vorhandenen an
  - Optional: System markiert die Playlist als „unvollständig"