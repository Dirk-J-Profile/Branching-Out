"""Interaktive Filteranwendung für eine users.json-Datei."""

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


def filter_users_by_name(users: list[dict[str, Any]], name: str) -> list[dict[str, Any]]:
    """Findet Nutzer, deren Name den Suchbegriff enthält (groß/klein ignoriert)."""
    search_term = name.strip().casefold()
    if not search_term:
        return []
    return [
        user
        for user in users
        if search_term in str(user.get("name", "")).casefold()
    ]


def filter_users_by_age(users: list[dict[str, Any]], age: int) -> list[dict[str, Any]]:
    """Findet Nutzer mit exakt dem angegebenen Alter."""
    matches: list[dict[str, Any]] = []
    for user in users:
        try:
            if int(user.get("age")) == age:
                matches.append(user)
        except (TypeError, ValueError):
            # Ein einzelner fehlerhafter Datensatz soll die Suche nicht abbrechen.
            continue
    return matches


def filter_users_by_email(users: list[dict[str, Any]], email: str) -> list[dict[str, Any]]:
    """Findet Nutzer, deren E-Mail den Suchbegriff enthält (groß/klein ignoriert)."""
    search_term = email.strip().casefold()
    if not search_term:
        return []
    return [
        user
        for user in users
        if search_term in str(user.get("email", "")).casefold()
    ]


def _load_users(file_path: Path) -> list[dict[str, Any]]:
    """Lädt und prüft die JSON-Datei."""
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Die JSON-Datei muss eine Liste von Benutzerobjekten enthalten.")
    if not all(isinstance(user, dict) for user in data):
        raise ValueError("Jeder Eintrag in der JSON-Datei muss ein Benutzerobjekt sein.")
    return data


def _print_results(users: list[dict[str, Any]]) -> None:
    if not users:
        print("Keine passenden Nutzer gefunden.")
        return

    print(f"{len(users)} passende(r) Nutzer gefunden:")
    for user in users:
        print(json.dumps(user, ensure_ascii=False, indent=2))


def main() -> int:
    """Startet den interaktiven Filter für users.json im aktuellen Ordner."""
    file_path = Path("users.json")

    try:
        users = _load_users(file_path)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden.")
        return 1
    except JSONDecodeError as error:
        print(f"Fehler: '{file_path}' enthält ungültiges JSON (Zeile {error.lineno}, Spalte {error.colno}).")
        return 1
    except ValueError as error:
        print(f"Fehler: {error}")
        return 1
    except OSError as error:
        print(f"Fehler beim Lesen von '{file_path}': {error}")
        return 1

    print("Filteroptionen:")
    print("1 - Nach Name filtern")
    print("2 - Nach Alter filtern")
    print("3 - Nach E-Mail filtern")
    choice = input("Bitte Filteroption wählen (1-3): ").strip()

    if choice == "1":
        name = input("Name oder Teil des Namens: ")
        if not name.strip():
            print("Fehler: Der Name darf nicht leer sein.")
            return 1
        results = filter_users_by_name(users, name)
    elif choice == "2":
        raw_age = input("Alter: ").strip()
        try:
            age = int(raw_age)
            if age < 0:
                raise ValueError
        except ValueError:
            print("Fehler: Bitte gib ein gültiges, nicht negatives ganzzahliges Alter ein.")
            return 1
        results = filter_users_by_age(users, age)
    elif choice == "3":
        email = input("E-Mail oder Teil der E-Mail: ")
        if not email.strip():
            print("Fehler: Die E-Mail darf nicht leer sein.")
            return 1
        results = filter_users_by_email(users, email)
    else:
        print("Fehler: Ungültige Filteroption. Bitte wähle 1, 2 oder 3.")
        return 1

    _print_results(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
