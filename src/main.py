from core.library import Library
from core.title import Title

def main():
    file_path = "src/data/library.json"
    lib = Library(filepath=file_path)

    t1 = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")

    result = lib.add_title(t1)

    t1 = Title(name="Imagine", artist="John Lennon", album="Imagine", year=1971, genre="Rock")

    lib.add_title(t1)

    # Update
    result = lib.update_title(1, genre="Pop", year=1972)

if __name__ == "__main__":
    main()