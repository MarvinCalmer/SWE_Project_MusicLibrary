from core.library import Library
from core.title import Title

def main():
    file_path = "src/data/library.json"
    lib = Library(filepath=file_path)

    while True:
        print("\n=== Musikbibliothek Menü ===")
        print("[1] Titel anzeigen")
        print("[2] Titel hinzufügen")
        print("[3] Titel bearbeiten")
        print("[4] Titel löschen")
        print("[5] Beenden")

        choice = input("Wähle eine Option: ")

        if choice == "1":
            lib.list_titles()  # Liste aller Titel anzeigen

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
            print("👋 Programm beendet.")
            break

        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    main()