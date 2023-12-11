import getpass
import sqlite3
import bcrypt
from src.config import DB_PATH


def register_user():
    while True:
        username = input("Ingrese el nombre de usuario: ").strip().lower()
        password = getpass.getpass("Ingrese la clave: ")  # Password will not be echoed
        role = input("Ingrese el rol: (admin/user): ").strip().lower()

        # Ensure the role is valid
        if role not in ["admin", "user"]:
            print("Entrada inválida. Por favor, ingrese 'admin' o 'user'.")
            continue

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Try to insert the new user into the database
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                insert_query = "INSERT INTO Users (username, hashed_password, role) VALUES (?, ?, ?)"
                cursor.execute(insert_query, (username, hashed_password, role))
                conn.commit()

                print(f"Usuario creado exitosamente.\n")
                break

        except sqlite3.IntegrityError:
            print("El nombre de usuario ya está en uso. Por favor, elija uno diferente.\n")
            continue
