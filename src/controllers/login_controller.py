import getpass
import sqlite3
import time
import bcrypt
from rich.console import Console
from src.config import DB_PATH
from src.database.models import User
from src.utils.helpers import clear_console

console = Console()


def login():
    while True:
        clear_console()
        console.print("\nInicio de sesión\n", style="bold magenta")
        choice = str(input("Ingrese 1 para usuario existente, 2 para registrar usuario, 0 para salir: ").strip().lower())

        if choice == "1":
            clear_console()
            username = input("Usuario: ")
            password = getpass.getpass("Clave: ")  # Password will not be echoed

            # Verify user credentials.
            if verify_user_credentials(username, password):
                console.print("Login exitoso!", style="bold green")
                return get_user_data(username)
                time.sleep(1)
                break
            else:
                console.print("Credenciales Inválidas", style="bold red")
                time.sleep(1)

        elif choice == "2":
            while True:
                console.print("\nIngrese un usuario administrador", style="cyan")
                username = input("Usuario: ")
                password = getpass.getpass("Clave: ")  # Password will not be echoed

                if verify_user_credentials(username, password) and get_user_data(username).is_admin():
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

    else:
        console.print("Error al obtener los datos del usuario.", style="bold red")
        return False


def verify_password(password, hashed):
    # Ensure both password and hashed are byte strings
    password_bytes = password.encode()
    hashed_bytes = hashed.encode() if isinstance(hashed, str) else hashed
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_user_data(username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username, hashed_password, role FROM Users WHERE username = ?", (username,))
        user_data = cursor.fetchone()

    if user_data:
        # Create an User instance
        return User(user_id=user_data[0], username=user_data[1],
                    hashed_password=user_data[2], role=user_data[3])
    else:
        console.print("Error al obtener los datos del usuario.", style="bold red")


def register_user():
    while True:
        username = input("Ingrese el nombre de usuario: ").strip().lower()
        password = getpass.getpass("Ingrese la clave: ")  # Password will not be echoed
        role = input("Ingrese el rol: (admin/user): ").strip().lower()

        # Ensure the role is valid
        if role not in ["admin", "user"]:
            console.print("\nEntrada inválida. Por favor, ingrese 'admin' o 'user'.\n", style="bold red")
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

                console.print(f"Usuario creado exitosamente.\n", style="cyan")
                break

        except sqlite3.IntegrityError:
            console.print("El nombre de usuario ya está en uso. Por favor, elija uno diferente.\n", style="bold yellow")
            continue
