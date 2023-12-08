import sqlite3
import bcrypt
from src.database.models import User


def register_user():
    while True:
        username = input("Ingrese el nombre de usuario: ").strip().lower()
        password = input("Ingrese la clave: ")
        role = input("Ingrese el rol: (admin/user): ").strip().lower()

        # Ensure the role is valid
        if role not in ["admin", "user"]:
            print("Entrada inválida. Por favor, ingrese 'admin' o 'user'.")
            continue

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Try to insert the new user into the database
        try:
            conn = sqlite3.connect('../src/database/school_management_system.db')
            cursor = conn.cursor()
            insert_query = "INSERT INTO Users (username, hashed_password, role) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (username, hashed_password, role))
            conn.commit()
            user_id = cursor.lastrowid  # Get the ID of the newly created user
            conn.close()

            # Create a User object
            user = User(user_id=user_id, username=username, hashed_password=hashed_password, role=role)
            print("Usuario creado exitosamente.")
            break

        except sqlite3.IntegrityError:
            print("El nombre de usuario ya está en uso. Por favor, elija uno diferente.")
            continue


# Example usage
register_user()
