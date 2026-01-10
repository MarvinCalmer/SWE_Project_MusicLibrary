import tkinter as tk
from pathlib import Path
from tkinter import simpledialog, messagebox, ttk
from src.core.library import Library
from src.core.title import Title
from src.core.playlist_manager import PlaylistManager

library = Library(filepath=Path("src/data/library.json"))
playlist_manager = PlaylistManager(filepath=Path("src/data/playlists.json"))

# Hauptfenster
root = tk.Tk()
root.title("Musikbibliothek")
root.geometry("1400x700")
root.minsize(1200, 600)

# Main container
main_container = tk.Frame(root, bg="#121212")
main_container.pack(fill=tk.BOTH, expand=True)

# Configure grid
main_container.grid_rowconfigure(0, weight=1)
main_container.grid_columnconfigure(0, weight=0)  # Playlist sidebar
main_container.grid_columnconfigure(1, weight=1)  # Song library
main_container.grid_columnconfigure(2, weight=0)  # Playlist songs (narrower)

# ============ LEFT SIDEBAR - PLAYLISTS ============
playlist_sidebar = tk.Frame(main_container, bg="#000000", width=180)
playlist_sidebar.grid(row=0, column=0, sticky="nsew")
playlist_sidebar.grid_propagate(False)

# Sidebar header
sidebar_header = tk.Frame(playlist_sidebar, bg="#000000")
sidebar_header.pack(fill=tk.X, padx=15, pady=15)

tk.Label(
    sidebar_header,
    text="Playlists",
    font=("Arial", 14, "bold"),
    bg="#000000",
    fg="#FFFFFF",
).pack(anchor="w")

# Playlist listbox
playlist_frame = tk.Frame(playlist_sidebar, bg="#000000")
playlist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

playlist_listbox = tk.Listbox(
    playlist_frame,
    bg="#121212",
    fg="#B3B3B3",
    selectbackground="#3A3A3A",
    selectforeground="#FFFFFF",
    font=("Arial", 10),
    borderwidth=0,
    highlightthickness=0,
    activestyle="none",
)
playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

playlist_scrollbar = tk.Scrollbar(playlist_frame, command=playlist_listbox.yview)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
playlist_listbox.config(yscrollcommand=playlist_scrollbar.set)

# Playlist management buttons
playlist_btn_frame = tk.Frame(playlist_sidebar, bg="#000000")
playlist_btn_frame.pack(fill=tk.X, padx=10, pady=10)

# ============ MIDDLE - SONG LIBRARY ============
library_frame = tk.Frame(main_container, bg="#121212")
library_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Library header
library_header = tk.Frame(library_frame, bg="#121212")
library_header.pack(fill=tk.X, pady=(0, 10))

tk.Label(
    library_header,
    text="Bibliothek",
    font=("Arial", 16, "bold"),
    bg="#121212",
    fg="#FFFFFF",
).pack(anchor="w")

# Search frame
search_frame = tk.Frame(library_frame, bg="#121212")
search_frame.pack(fill=tk.X, pady=(0, 10))

search_field_var = tk.StringVar(value="name")
search_field_dropdown = ttk.Combobox(
    search_frame, textvariable=search_field_var, state="readonly", width=12
)
search_field_dropdown["values"] = ["name", "artist", "album", "genre", "year"]
search_field_dropdown.pack(side=tk.LEFT, padx=(0, 5))

search_entry = tk.Entry(
    search_frame, width=30, bg="#282828", fg="#FFFFFF", insertbackground="#FFFFFF"
)
search_entry.pack(side=tk.LEFT, padx=(0, 5))

# Library buttons frame
library_btn_frame = tk.Frame(library_frame, bg="#121212")
library_btn_frame.pack(fill=tk.X, pady=(0, 10))

# Song library treeview
library_tree_frame = tk.Frame(library_frame, bg="#121212")
library_tree_frame.pack(fill=tk.BOTH, expand=True)

style = ttk.Style()
style.theme_use("default")
style.configure(
    "Library.Treeview",
    background="#121212",
    foreground="#FFFFFF",
    fieldbackground="#121212",
    borderwidth=0,
    font=("Arial", 10),
)
style.configure(
    "Library.Treeview.Heading",
    background="#282828",
    foreground="#B3B3B3",
    borderwidth=0,
    font=("Arial", 9, "bold"),
)
style.map(
    "Library.Treeview",
    background=[("selected", "#3A3A3A")],
    foreground=[("selected", "#FFFFFF")],
)

library_tree = ttk.Treeview(
    library_tree_frame,
    columns=("title", "artist", "album", "year", "genre", "rating"),
    show="tree headings",
    style="Library.Treeview",
    selectmode="browse",
)

library_tree.heading("title", text="Titel")
library_tree.heading("artist", text="Künstler")
library_tree.heading("album", text="Album")
library_tree.heading("year", text="Jahr")
library_tree.heading("genre", text="Genre")
library_tree.heading("rating", text="Bewertung")

library_tree.column("#0", width=0, stretch=False)
library_tree.column("title", width=180, anchor="w")
library_tree.column("artist", width=120, anchor="w")
library_tree.column("album", width=120, anchor="w")
library_tree.column("year", width=60, anchor="center")
library_tree.column("genre", width=90, anchor="w")
library_tree.column("rating", width=60, anchor="center")

library_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

library_scrollbar = tk.Scrollbar(library_tree_frame, command=library_tree.yview)
library_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
library_tree.config(yscrollcommand=library_scrollbar.set)

# ============ RIGHT - PLAYLIST SONGS ============
playlist_content = tk.Frame(main_container, bg="#121212", width=240)
playlist_content.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
playlist_content.grid_propagate(False)

# Playlist header
playlist_header = tk.Frame(playlist_content, bg="#121212")
playlist_header.pack(fill=tk.X, pady=(0, 10))

playlist_title_label = tk.Label(
    playlist_header,
    text="Keine Playlist ausgewählt",
    font=("Arial", 16, "bold"),
    bg="#121212",
    fg="#FFFFFF",
)
playlist_title_label.pack(anchor="w")

playlist_info_label = tk.Label(
    playlist_header, text="", font=("Arial", 10), bg="#121212", fg="#B3B3B3"
)
playlist_info_label.pack(anchor="w")

# Playlist action buttons
playlist_action_frame = tk.Frame(playlist_content, bg="#121212")
playlist_action_frame.pack(fill=tk.X, pady=(0, 10))

# Playlist songs treeview
playlist_tree_frame = tk.Frame(playlist_content, bg="#121212")
playlist_tree_frame.pack(fill=tk.BOTH, expand=True)

playlist_tree = ttk.Treeview(
    playlist_tree_frame,
    columns=("number", "title", "artist", "album", "year"),
    show="tree headings",
    style="Library.Treeview",
    selectmode="browse",
)

playlist_tree.heading("number", text="#")
playlist_tree.heading("title", text="Titel")
playlist_tree.heading("artist", text="Künstler")
playlist_tree.heading("album", text="Album")
playlist_tree.heading("year", text="Jahr")

playlist_tree.column("#0", width=0, stretch=False)
playlist_tree.column("number", width=40, anchor="center")
playlist_tree.column("title", width=160, anchor="w")
playlist_tree.column("artist", width=120, anchor="w")
playlist_tree.column("album", width=120, anchor="w")
playlist_tree.column("year", width=60, anchor="center")

playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

playlist_scrollbar = tk.Scrollbar(playlist_tree_frame, command=playlist_tree.yview)
playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
playlist_tree.config(yscrollcommand=playlist_scrollbar.set)

# ============ GLOBAL STATE ============
current_playlist_id = [None]
sort_by_name = [False]

# ============ HELPER FUNCTIONS ============


def create_button(parent, text, command, bg_color="#1DB954", width=None):
    """Create a styled button."""
    # All buttons now have black text for better readability
    text_color = "#000000"

    # Determine active colors based on background
    if bg_color == "#1DB954":  # Green
        active_bg = "#1ED760"
    elif bg_color == "#B91D1D":  # Red
        active_bg = "#D42020"
    else:  # Dark gray (#282828)
        active_bg = "#3A3A3A"

    # Use smaller padding for a compact layout
    default_width = 8
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=text_color,
        font=("Arial", 9, "bold"),
        borderwidth=0,
        padx=10,
        pady=4,
        cursor="hand2",
        activebackground=active_bg,
        activeforeground=text_color,
    )
    if width is None:
        btn.config(width=default_width)
    else:
        btn.config(width=width)
    return btn


def refresh_library_tree(titles=None):
    """Refresh the library treeview."""
    for item in library_tree.get_children():
        library_tree.delete(item)

    if titles is None:
        titles = library.get_titles()

    for t in titles:
        favorite_mark = "⭐ " if t.is_favorite else ""
        rating_display = "★" * t.rating if isinstance(t.rating, int) and t.rating > 0 else "-"
        library_tree.insert(
            "",
            "end",
            values=(f"{favorite_mark}{t.name}", t.artist, t.album, t.year, t.genre, rating_display),
            tags=(t.id,),
        )


def refresh_playlist_list():
    """Refresh the playlist listbox."""
    playlist_listbox.delete(0, tk.END)
    playlists = playlist_manager.get_all_playlists()
    for pl in playlists:
        track_count = len(pl["title_ids"])
        playlist_listbox.insert(tk.END, f"{pl['name']} ({track_count})")


def refresh_playlist_songs():
    """Refresh the playlist songs treeview."""
    for item in playlist_tree.get_children():
        playlist_tree.delete(item)

    if current_playlist_id[0] is None:
        playlist_title_label.config(text="Keine Playlist ausgewählt")
        playlist_info_label.config(text="Wähle eine Playlist aus der Liste")
        return

    playlist = playlist_manager.get_playlist(current_playlist_id[0])
    if playlist is None:
        return

    playlist_title_label.config(text=playlist["name"])
    track_count = len(playlist["title_ids"])
    info_text = f"{playlist['description']} • {track_count} Song"
    if track_count != 1:
        info_text += "s"
    playlist_info_label.config(text=info_text)

    for idx, title_id in enumerate(playlist["title_ids"], 1):
        try:
            lib_index = library._find_index_by_id(title_id)
            if lib_index is not None:
                title = library.get_titles_by_id(lib_index)
                playlist_tree.insert(
                    "",
                    "end",
                    values=(idx, title.name, title.artist, title.album, title.year),
                )
            else:
                playlist_tree.insert(
                    "", "end", values=(idx, "[Gelöschter Song]", "-", "-", "-")
                )
        except:
            playlist_tree.insert("", "end", values=(idx, "[Fehler]", "-", "-", "-"))


def get_selected_title_id_from_library():
    """Get the title ID of the selected song in library."""
    selection = library_tree.selection()
    if not selection:
        return None

    item = selection[0]
    # Find the title by matching the displayed data
    values = library_tree.item(item)["values"]
    title_name = values[0].replace("⭐ ", "")
    artist = values[1]

    # Find matching title in library
    for title in library.get_titles():
        if title.name == title_name and title.artist == artist:
            return title.id
    return None


# ============ LIBRARY FUNCTIONS ============


def search_titles():
    """Search titles in library."""
    term = search_entry.get().strip()
    if not term:
        refresh_library_tree()
        return

    field = search_field_var.get()
    results = library.search_library(**{field: term})

    if len(results) == 0:
        messagebox.showinfo("Keine Treffer", "Keine Titel gefunden.")
        refresh_library_tree()
    else:
        found = [Title(**t) for t in results]
        refresh_library_tree(found)


def add_title():
    """Add a new title to library."""
    name = simpledialog.askstring("Titel hinzufügen", "Songname:")
    if not name:
        return
    artist = simpledialog.askstring("Titel hinzufügen", "Künstler:")
    album = simpledialog.askstring("Titel hinzufügen", "Album:")
    year = simpledialog.askinteger("Titel hinzufügen", "Jahr:")
    genre = simpledialog.askstring("Titel hinzufügen", "Genre:")

    rating = simpledialog.askinteger("Titel hinzufügen", "Bewertung (1-5):", minvalue=1, maxvalue=5)

    new_title = Title(
        id=None,
        name=name,
        artist=artist,
        album=album,
        year=year,
        genre=genre,
        rating=rating,
    )
    library.add_title(new_title)
    refresh_library_tree()


def edit_title():
    """Edit the selected title."""
    title_id = get_selected_title_id_from_library()
    if title_id is None:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return

    index = library._find_index_by_id(title_id)
    title = library.get_titles_by_id(index)

    name = simpledialog.askstring(
        "Titel bearbeiten", "Neuer Songname:", initialvalue=title.name
    )
    if name is None:
        return
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
    rating = simpledialog.askinteger(
        "Titel bearbeiten", "Bewertung (1-5):", initialvalue=title.rating, minvalue=1, maxvalue=5
    )

    library.update_title(
        title.id,
        name=name,
        artist=artist,
        album=album,
        year=year,
        genre=genre,
        rating=rating,
    )
    refresh_library_tree()
    if current_playlist_id[0] is not None:
        refresh_playlist_songs()


def delete_title():
    """Delete the selected title."""
    title_id = get_selected_title_id_from_library()
    if title_id is None:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return

    index = library._find_index_by_id(title_id)
    title = library.get_titles_by_id(index)

    if messagebox.askyesno("Löschen bestätigen", f"'{title.name}' wirklich löschen?"):
        library.delete_title(title.id)
        refresh_library_tree()
        if current_playlist_id[0] is not None:
            refresh_playlist_songs()


def sort_titles():
    """Sort titles in library."""
    if not sort_by_name[0]:
        titles_sorted = sorted(library.get_titles(), key=lambda t: t.name.lower())
        sort_by_name[0] = True
    else:
        titles_sorted = sorted(library.get_titles(), key=lambda t: t.id)
        sort_by_name[0] = False

    refresh_library_tree(titles_sorted)


def toggle_favorite():
    """Toggle favorite status of selected title."""
    title_id = get_selected_title_id_from_library()
    if title_id is None:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return

    library.toggle_favorite(title_id)
    refresh_library_tree()


def set_rating():
    """Set or change the rating (1-5) of the selected title."""
    title_id = get_selected_title_id_from_library()
    if title_id is None:
        messagebox.showwarning("Hinweis", "Bitte einen Titel auswählen.")
        return

    index = library._find_index_by_id(title_id)
    title = library.get_titles_by_id(index)

    rating = simpledialog.askinteger(
        "Bewertung",
        "Bewertung (1-5):",
        initialvalue=title.rating,
        minvalue=1,
        maxvalue=5,
    )

    # If user cancelled
    if rating is None:
        return

    try:
        library.update_title(title.id, rating=rating)
        refresh_library_tree()
    except ValueError as e:
        messagebox.showerror("Fehler", str(e))


# ============ PLAYLIST FUNCTIONS ============


def on_playlist_select(event):
    """Handle playlist selection."""
    selection = playlist_listbox.curselection()
    if not selection:
        return

    index = selection[0]
    playlists = playlist_manager.get_all_playlists()
    if index < len(playlists):
        current_playlist_id[0] = playlists[index]["id"]
        refresh_playlist_songs()


def create_new_playlist():
    """Create a new playlist."""
    name = simpledialog.askstring("Neue Playlist", "Playlist Name:")
    if not name:
        return

    description = simpledialog.askstring(
        "Neue Playlist", "Beschreibung (optional):", initialvalue=""
    )

    playlist_manager.create_playlist(name, description or "")
    refresh_playlist_list()


def edit_playlist():
    """Edit the selected playlist."""
    if current_playlist_id[0] is None:
        messagebox.showwarning("Hinweis", "Bitte eine Playlist auswählen.")
        return

    playlist = playlist_manager.get_playlist(current_playlist_id[0])

    name = simpledialog.askstring(
        "Playlist bearbeiten", "Neuer Name:", initialvalue=playlist["name"]
    )
    if name is None:
        return

    description = simpledialog.askstring(
        "Playlist bearbeiten",
        "Neue Beschreibung:",
        initialvalue=playlist["description"],
    )

    playlist_manager.update_playlist(
        current_playlist_id[0], name=name, description=description or ""
    )
    refresh_playlist_list()
    refresh_playlist_songs()


def delete_playlist():
    """Delete the selected playlist."""
    if current_playlist_id[0] is None:
        messagebox.showwarning("Hinweis", "Bitte eine Playlist auswählen.")
        return

    playlist = playlist_manager.get_playlist(current_playlist_id[0])
    if messagebox.askyesno(
        "Löschen bestätigen", f"Playlist '{playlist['name']}' wirklich löschen?"
    ):
        playlist_manager.delete_playlist(current_playlist_id[0])
        current_playlist_id[0] = None
        refresh_playlist_list()
        refresh_playlist_songs()


def export_playlist():
    """Export the selected playlist to a JSON file."""
    if current_playlist_id[0] is None:
        messagebox.showwarning("Hinweis", "Bitte eine Playlist auswählen.")
        return

    playlist = playlist_manager.get_playlist(current_playlist_id[0])

    # Open file dialog to choose export location
    from tkinter import filedialog

    default_filename = f"{playlist['name'].replace(' ', '_')}.json"

    filepath = filedialog.asksaveasfilename(
        title="Playlist exportieren",
        defaultextension=".json",
        initialfile=default_filename,
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if filepath:
        try:
            playlist_manager.export_playlist(current_playlist_id[0], filepath)
            messagebox.showinfo(
                "Erfolg", f"Playlist '{playlist['name']}' wurde exportiert."
            )
        except Exception as e:
            messagebox.showerror("Fehler", f"Export fehlgeschlagen: {e}")


def import_playlist():
    """Import a playlist from a JSON file."""
    from tkinter import filedialog

    filepath = filedialog.askopenfilename(
        title="Playlist importieren",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
    )

    if filepath:
        try:
            imported = playlist_manager.import_playlist(filepath)
            refresh_playlist_list()
            messagebox.showinfo(
                "Erfolg", f"Playlist '{imported['name']}' wurde importiert."
            )
        except ValueError as e:
            messagebox.showerror("Fehler", f"Import fehlgeschlagen: {e}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Unerwarteter Fehler: {e}")


def add_song_to_playlist():
    """Add selected song from library to current playlist."""
    if current_playlist_id[0] is None:
        messagebox.showwarning("Hinweis", "Bitte zuerst eine Playlist auswählen.")
        return

    title_id = get_selected_title_id_from_library()
    if title_id is None:
        messagebox.showwarning("Hinweis", "Bitte einen Song auswählen.")
        return

    try:
        playlist_manager.add_track(current_playlist_id[0], title_id)
        refresh_playlist_songs()
        refresh_playlist_list()
    except ValueError as e:
        messagebox.showerror("Fehler", str(e))


def remove_song_from_playlist():
    """Remove selected song from current playlist."""
    if current_playlist_id[0] is None:
        messagebox.showwarning("Hinweis", "Bitte eine Playlist auswählen.")
        return

    selection = playlist_tree.selection()
    if not selection:
        messagebox.showwarning("Hinweis", "Bitte einen Song auswählen.")
        return

    item = selection[0]
    item_values = playlist_tree.item(item)["values"]
    song_number = item_values[0]

    playlist = playlist_manager.get_playlist(current_playlist_id[0])
    song_index = song_number - 1

    if song_index < len(playlist["title_ids"]):
        title_id = playlist["title_ids"][song_index]

        try:
            playlist_manager.remove_track(current_playlist_id[0], title_id)
            refresh_playlist_songs()
            refresh_playlist_list()
        except ValueError as e:
            messagebox.showerror("Fehler", str(e))


# ============ CREATE BUTTONS ============

# Playlist sidebar buttons
create_button(playlist_btn_frame, "Neue Playlist", create_new_playlist).pack(
    fill=tk.X, pady=2
)
create_button(playlist_btn_frame, "Bearbeiten", edit_playlist, bg_color="#282828").pack(
    fill=tk.X, pady=2
)
create_button(playlist_btn_frame, "Löschen", delete_playlist, bg_color="#282828").pack(
    fill=tk.X, pady=2
)

# Separator
tk.Frame(playlist_btn_frame, bg="#282828", height=1).pack(fill=tk.X, pady=5)

# Import/Export buttons
create_button(
    playlist_btn_frame, "Exportieren", export_playlist, bg_color="#282828"
).pack(fill=tk.X, pady=2)
create_button(
    playlist_btn_frame, "Importieren", import_playlist, bg_color="#282828"
).pack(fill=tk.X, pady=2)

# Library buttons
create_button(library_btn_frame, "Hinzufügen", add_title, width=8).pack(side=tk.LEFT, padx=2)
create_button(library_btn_frame, "Editieren", edit_title, bg_color="#282828", width=8).pack(
    side=tk.LEFT, padx=2
)
create_button(
    library_btn_frame, "Löschen", delete_title, bg_color="#B91D1D", width=8
).pack(side=tk.LEFT, padx=2)
create_button(
    library_btn_frame, "Suchen", search_titles, bg_color="#282828", width=8
).pack(side=tk.LEFT, padx=2)
create_button(
    library_btn_frame, "Sortieren", sort_titles, bg_color="#282828", width=8
).pack(side=tk.LEFT, padx=2)
create_button(
    library_btn_frame, "Favoritisieren", toggle_favorite, bg_color="#282828", width=8
).pack(side=tk.LEFT, padx=2)
create_button(
    library_btn_frame, "Bewerten", set_rating, bg_color="#282828", width=8
).pack(side=tk.LEFT, padx=2)

# Playlist action buttons
create_button(playlist_action_frame, "Song hinzufügen", add_song_to_playlist).pack(
    side=tk.LEFT, padx=2
)
create_button(
    playlist_action_frame,
    "Song entfernen",
    remove_song_from_playlist,
    bg_color="#B91D1D",
).pack(side=tk.LEFT, padx=2)

# ============ BIND EVENTS ============
playlist_listbox.bind("<<ListboxSelect>>", on_playlist_select)
search_entry.bind("<Return>", lambda event: search_titles())


# Double-click to add song to playlist
def on_library_double_click(event):
    if current_playlist_id[0] is not None:
        add_song_to_playlist()


library_tree.bind("<Double-Button-1>", on_library_double_click)

# ============ INITIAL LOAD ============
refresh_library_tree()
refresh_playlist_list()
refresh_playlist_songs()

root.mainloop()
