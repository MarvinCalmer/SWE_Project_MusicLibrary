import tkinter as tk
from pathlib import Path
from tkinter import simpledialog, messagebox, ttk
from src.core.library import Library
from src.core.title import Title

library = Library(filepath=Path("src/data/library.json"))
sort_by_name = False

# Hauptfenster
root = tk.Tk()
root.title("Musikbibliothek")
root.geometry("1000x600")
root.minsize(950, 400)

song_listbox = tk.Listbox(root, height=15, width=100)
song_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

search_frame = tk.Frame(root)
search_frame.pack(pady=5)

# Dropdown Menu
search_field_var = tk.StringVar(value="name")
search_field_dropdown = ttk.Combobox(
    search_frame, textvariable=search_field_var, state="readonly", width=15
)
search_field_dropdown["values"] = ["name", "artist", "album", "genre", "year"]
search_field_dropdown.grid(row=0, column=0, padx=5)

# Search fiedld
search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)


# helper
def refresh_listbox(titles=None):
    song_listbox.delete(0, tk.END)
    if titles is None:
        titles = library.get_titles()
    for t in titles:
        favorite_mark = "⭐ " if t.is_favorite else ""
        song_listbox.insert(
            tk.END,
            f"{favorite_mark}{t.name} - {t.artist} ({t.album}, {t.year}) [{t.genre}]",
        )


def search_titles():
    term = search_entry.get().strip()
    if not term:
        refresh_listbox()
        return

    field = search_field_var.get()
    results = library.search_library(**{field: term})

    if len(results) == 0:
        messagebox.showinfo("Keine Treffer", "Keine Titel gefunden.")
        refresh_listbox()
    else:
        found = [Title(**t) for t in results]
        refresh_listbox(found)


# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)


def add_title():
    name = simpledialog.askstring("Titel hinzufügen", "Songname:")
    if not name:
        return
    artist = simpledialog.askstring("Titel hinzufügen", "Künstler:")
    album = simpledialog.askstring("Titel hinzufügen", "Album:")
    year = simpledialog.askinteger("Titel hinzufügen", "Jahr:")
    genre = simpledialog.askstring("Titel hinzufügen", "Genre:")

    new_title = Title(
        id=None, name=name, artist=artist, album=album, year=year, genre=genre
    )
    library.add_title(new_title)
    refresh_listbox()


def delete_title():
    selection = song_listbox.curselection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return
    index = selection[0]
    title = library.get_titles_by_id(index)
    if messagebox.askyesno("Löschen bestätigen", f"'{title.name}' wirklich löschen?"):
        library.delete_title(title.id)
        refresh_listbox()


def edit_title():
    selection = song_listbox.curselection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return
    index = selection[0]
    title = library.get_titles_by_id(index)

    name = simpledialog.askstring(
        "Titel bearbeiten", "Neuer Songname:", initialvalue=title.name
    )
    artist = simpledialog.askstring(
        "Titel bearbeiten", "Neuer Künstler:", initialvalue=title.artist
    )
    album = simpledialog.askstring(
        "Titel bearbeiten", "Neues Album:", initialvalue=title.album
    )
    year = simpledialog.askinteger(
        "Titel bearbeiten", "Neues Jahr:", initialvalue=title.year
    )
    genre = simpledialog.askstring(
        "Titel bearbeiten", "Neues Genre:", initialvalue=title.genre
    )

    library.update_title(
        title.id, name=name, artist=artist, album=album, year=year, genre=genre
    )
    refresh_listbox()


def sort_titles():
    global sort_by_name

    if not sort_by_name:
        # Sortiere nach Name
        titles_sorted = sorted(library.get_titles(), key=lambda t: t.name.lower())
        sort_by_name = True
    else:
        # Sortiere nach ID
        titles_sorted = sorted(library.get_titles(), key=lambda t: t.id)
        sort_by_name = False

    refresh_listbox(titles_sorted)


def toggle_favorite():
    selection = song_listbox.curselection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return

    index = selection[0]
    title = library.get_titles_by_id(index)

    library.toggle_favorite(title.id)
    refresh_listbox()


# Buttons
tk.Button(button_frame, text="Add", width=12, command=add_title).grid(
    row=0, column=0, padx=5
)
tk.Button(button_frame, text="Edit", width=12, command=edit_title).grid(
    row=0, column=1, padx=5
)
tk.Button(button_frame, text="Delete", width=12, command=delete_title).grid(
    row=0, column=2, padx=5
)
tk.Button(button_frame, text="Search", width=12, command=search_titles).grid(
    row=0, column=3, padx=5
)
tk.Button(button_frame, text="Sort", width=12, command=sort_titles).grid(
    row=0, column=4, padx=5
)
tk.Button(button_frame, text="⭐ Favorite", width=12, command=toggle_favorite).grid(
    row=0, column=5, padx=5
)
tk.Button(button_frame, text="Exit", width=12, command=root.destroy).grid(
    row=0, column=6, padx=5
)

# Bind enter key
search_entry.bind("<Return>", lambda event: search_titles())

refresh_listbox()
root.mainloop()
