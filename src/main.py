from core.library import Library
from core.title import Title

def main():
    lib = Library(filepath="src/data/library.json")

    while True:
        print("\n=== Musikbibliothek Menü ===")
        print("[1] Titel anzeigen")
        print("[2] Titel hinzufügen")
        print("[3] Titel bearbeiten")
        print("[4] Titel löschen")
        print("[5] Suchen")
        print("[6] Beenden")

        choice = input("Wähle eine Option: ")

        if choice == "1":
            titles = lib.list_titles()
            if not titles:
                print("📚 Die Bibliothek ist leer.")
            else:
                print("\n📚 Aktuelle Bibliothek:")
                print("-" * 60)
                for t in titles:
                    print(f"ID: {t.id} | {t.artist} - {t.name} ({t.year}) [{t.genre}]")
                print("-" * 60)


        elif choice == "2":
            name = input("Titelname: ")
            artist = input("Künstler: ")
            album = input("Album: ")
            year = int(input("Jahr: "))
            genre = input("Genre: ")
            t = Title(name=name, artist=artist, album=album, year=year, genre=genre)
            result = lib.add_title(t)
            print(f"✅ Titel hinzugefügt: ID {result['title']['id']} - {result['title']['name']}")

        elif choice == "3":
            titles = lib.list_titles()
            if not titles:
                continue
            try:
                title_id = int(input("Welche ID bearbeiten?: "))
                feld = input("Welches Feld ändern? (name, artist, album, year, genre): ")
                wert = input("Neuer Wert: ")
                if feld == "year":
                    wert = int(wert)
                result = lib.update_title(title_id, **{feld: wert})
                if result["success"]:
                    print(f"✅ Titel ID {title_id} wurde aktualisiert.")
                else:
                    print("❌ Fehler:", result["error"])
            except ValueError:
                print("Ungültige Eingabe!")

        elif choice == "4":
            titles = lib.list_titles()
            if not titles:
                continue
            try:
                title_id = int(input("Welche ID löschen?: "))
                result = lib.delete_title(title_id)
                if result["success"]:
                    print(f"🗑️ Titel ID {title_id} gelöscht.")
                else:
                    print("❌ Fehler:", result["error"])
            except ValueError:
                print("Ungültige Eingabe!")

        elif choice == "5":
            # Suchkriterien abfragen
            print("\n🔍 Suche nach Titeln")
            name = input("Name (Enter überspringen, wenn nicht relevant): ").strip()
            artist = input("Künstler (Enter überspringen, wenn nicht relevant): ").strip()
            album = input("Album (Enter überspringen, wenn nicht relevant): ").strip()
            genre = input("Genre (Enter überspringen, wenn nicht relevant): ").strip()
            year_input = input("Jahr (Enter überspringen, wenn nicht relevant): ").strip()

            # Suchparameter zusammenstellen
            search_params = {}
            if name:
                search_params["name"] = name
            if artist:
                search_params["artist"] = artist
            if album:
                search_params["album"] = album
            if genre:
                search_params["genre"] = genre
            if year_input:
                try:
                    search_params["year"] = int(year_input)
                except ValueError:
                    print("❌ Ungültiges Jahr. Suche ohne Jahr.")
            
            # Suche durchführen
            results = lib.search_library(**search_params)

            # Ergebnisse anzeigen
            if results["count"] == 0:
                print("❌ Keine Treffer gefunden.")
            else:
                print(f"\n🔎 Gefundene Titel: {results['count']}")
                print("-" * 60)
                for t in results["results"]:
                    print(f"ID: {t['id']} | {t['artist']} - {t['name']} ({t['year']}) [{t['genre']}]")
                print("-" * 60)


        elif choice == "6":
            print("👋 Programm beendet.")
            break

        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()