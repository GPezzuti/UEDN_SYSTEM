import getpass
import sqlite3
import time
import bcrypt
from rich.console import Console
from src.config import DB_PATH
from src.utils.helpers import clear_console

console = Console()


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def verify_password(password, hashed):
    # Ensure both password and hashed are byte strings
    password_bytes = password.encode()
    hashed_bytes = hashed.encode() if isinstance(hashed, str) else hashed
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def login():
    while True:
        clear_console()
        console.print("\nInicio de sesión\n", style="bold magenta")
        choice = str(input("Ingrese 1 para usuario existente, 2 para registrar usuario, 0 para salir: ").strip().lower())
        if choice == "1":
            clear_console()
            username = input("Usuario: ")
            password = getpass.getpass("Clave: ")  # Password will not be echoed

            # Verify user credentials. This is a placeholder function.
            if verify_user_credentials(username, password):
                break
            else:
                console.print("Credenciales inválidas, intente de nuevo.", style="bold red")
                time.sleep(1)

        elif choice == "2":
            while True:
                console.print("\nIngrese un usuario administrador", style="cyan")
                username = input("Usuario: ")
                password = getpass.getpass("Clave: ")  # Password will not be echoed

                if verify_user_credentials(username, password) and (get_user_role(username) == "admin"):
                    console.print("\nRegistro de usuario:", style="green")
                    register_user()
                    time.sleep(1)
                    break
                elif verify_user_credentials(username, password) is False:
                    console.print("Credenciales Inválidas", style="bold red")
                else:
                    console.print("Usuario con pocos privilegios", style="bold red")
        elif choice == "0":
            clear_console()
            print("OK")
            exit()
        else:
            console.print("Opción Incorrecta\n", style="bold red", justify="center")
            time.sleep(1)


def verify_user_credentials(username, password):
    # Fetch user's hashed password from the database
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hashed_password FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        return verify_password(password, hashed_password)
    return False


def get_user_role(username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()

    if result:
        return result[0]  # Return the role


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
